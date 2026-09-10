from src.llm import client

def explain_result(question: str, columns: list, rows: list, sql: str) -> str:
    preview = rows[:20]

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a data analyst for a carsharing company. "
                    "Answer the user's question directly and briefly. "
                    "Do not repeat all rows or values that are already visible in the table. "
                    "For time series or breakdowns with multiple rows, summarize the main trend or insight instead of listing every value. "
                    "Mention notable highs, lows or changes only when useful. "
                    "Do not mention database columns, preview rows or technical details. "
                    "If SQL contains LIMIT, do not treat returned rows as the total number of records. "
                    "Do not infer or mention currency unless explicitly provided. "
                    "Do not invent information. "
                    "Use 1-2 short sentences."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n"
                    f"SQL: {sql}\n"
                    f"Columns: {columns}\n"
                    f"Data: {preview}\n"
                    f"Returned rows: {len(rows)}"
                ),
            },
        ],
    )

    return response.choices[0].message.content