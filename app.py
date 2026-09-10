import uuid
import streamlit as st
from src.sql_generator import generate_sql
from src.services.database_service import execute_query
from src.services.result_explainer import explain_result
from src.services.chat_history_service import save_message, get_sessions, load_session, get_last_sql
from src.services.source_router import detect_source
from src.agents.fleet_agent import handle_fleet_question
from src.ui.styles import apply_styles

st.set_page_config(page_title="Anytime Analytics", page_icon="📊", layout="wide")
apply_styles()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "last_sql" not in st.session_state:
    st.session_state.last_sql = None

st.sidebar.markdown("""
<div class="brand">
    <div class="brand-logo">any<br>time</div>
    <div class="brand-name">Anytime<br>Analytics</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("＋  New chat", use_container_width=True):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.last_sql = None
    st.rerun()

sessions = get_sessions()
if sessions:
    st.sidebar.markdown("#### Recent conversations")
    for session_id, title, created_at in sessions[:10]:
        label = title[:32] + "..." if len(title) > 32 else title
        if st.sidebar.button(label, key=session_id, use_container_width=True):
            st.session_state.session_id = session_id
            st.session_state.messages = load_session(session_id)
            st.session_state.last_sql = get_last_sql(session_id)
            st.rerun()

st.markdown('<div class="page-title">Anytime Analytics</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Ask questions about rides, customers, revenue and fleet.</div>',
    unsafe_allow_html=True
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("data"):
            st.dataframe(message["data"], width="stretch")

question = st.chat_input("Ask your analytics question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    save_message(st.session_state.session_id, "user", question)

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            source = detect_source(question)

            if source == "fleet":
                answer, data = handle_fleet_question(question)

                if isinstance(data, dict):
                    data = [{"model": model, "vehicles": count} for model, count in data.items()]

                st.write(answer)
                if data:
                    st.dataframe(data, width="stretch")

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "data": data}
                )
                save_message(
                    st.session_state.session_id,
                    "assistant",
                    answer,
                    data_json=data
                )

            else:
                sql = generate_sql(
                    question,
                    st.session_state.messages[:-1],
                    st.session_state.last_sql
                )

                if sql == "SQL validation failed.":
                    answer = "I couldn't safely generate a query for this request."
                    st.error(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                    save_message(st.session_state.session_id, "assistant", answer)

                else:
                    columns, rows = execute_query(sql)
                    summary = explain_result(question, columns, rows, sql)
                    data = [dict(zip(columns, row)) for row in rows]

                    st.write(summary)
                    st.dataframe(data, width="stretch")

                    with st.expander("Technical details"):
                        st.code(sql, language="sql")

                    st.session_state.last_sql = sql
                    st.session_state.messages.append(
                        {"role": "assistant", "content": summary}
                    )
                    save_message(
                        st.session_state.session_id,
                        "assistant",
                        summary,
                        sql
                    )

        except Exception as e:
            error_text = str(e)
            answer = (
                "The query took too long to execute. Please try a more specific request."
                if "statement timeout" in error_text.lower()
                else "Something went wrong while processing your request."
            )

            st.error(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
            save_message(st.session_state.session_id, "assistant", answer)

            with st.expander("Technical error"):
                st.code(error_text)