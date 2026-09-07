import streamlit as st
from src.sql_generator import generate_sql
from src.services.database_service import execute_query
from src.services.result_explainer import explain_result

st.set_page_config(page_title="Analytics Assistant", page_icon="📊", layout="wide")
st.title("📊 Analytics Assistant")

question = st.chat_input("Ask your analytics question...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            sql = generate_sql(question)

            if sql == "SQL validation failed.":
                st.error("I couldn't safely generate a query for this request.")
            else:
                columns, rows = execute_query(sql)
                summary = explain_result(question, columns, rows, sql)

                st.write(summary)
                st.dataframe([dict(zip(columns, row)) for row in rows], width="stretch")

                with st.expander("Technical details"):
                    st.code(sql, language="sql")

        except Exception as e:
            error_text = str(e)

            if "statement timeout" in error_text.lower():
                st.error("The query took too long to execute. Please try a more specific request.")
            else:
                st.error("Something went wrong while processing your request.")

            with st.expander("Technical error"):
                st.code(error_text)