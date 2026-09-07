import uuid
import streamlit as st
from src.sql_generator import generate_sql
from src.services.database_service import execute_query
from src.services.result_explainer import explain_result
from src.services.chat_history_service import save_message, get_sessions, load_session, get_last_sql

st.set_page_config(page_title="Analytics Assistant", page_icon="📊", layout="wide")
st.title("📊 Analytics Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "last_sql" not in st.session_state:
    st.session_state.last_sql = None

if st.sidebar.button("New chat"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.last_sql = None
    st.rerun()

sessions = get_sessions()

if sessions:
    st.sidebar.markdown("### Previous chats")

    for session_id, title, created_at in sessions[:10]:
        label = title[:35] + "..." if len(title) > 35 else title

        if st.sidebar.button(label, key=session_id):
            st.session_state.session_id = session_id
            st.session_state.messages = load_session(session_id)
            st.session_state.last_sql = get_last_sql(session_id)
            st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask your analytics question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    save_message(st.session_state.session_id, "user", question)

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            sql = generate_sql(
                question,
                st.session_state.messages[:-1],
                st.session_state.last_sql
            )

            if sql == "SQL validation failed.":
                answer = "I couldn't safely generate a query for this request."
                st.error(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                save_message(st.session_state.session_id, "assistant", answer)
            else:
                columns, rows = execute_query(sql)
                summary = explain_result(question, columns, rows, sql)

                st.write(summary)
                st.dataframe([dict(zip(columns, row)) for row in rows], width="stretch")

                with st.expander("Technical details"):
                    st.code(sql, language="sql")

                st.session_state.last_sql = sql
                st.session_state.messages.append({"role": "assistant", "content": summary})
                save_message(st.session_state.session_id, "assistant", summary, sql)

        except Exception as e:
            error_text = str(e)

            if "statement timeout" in error_text.lower():
                answer = "The query took too long to execute. Please try a more specific request."
            else:
                answer = "Something went wrong while processing your request."

            st.error(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            save_message(st.session_state.session_id, "assistant", answer)

            with st.expander("Technical error"):
                st.code(error_text)