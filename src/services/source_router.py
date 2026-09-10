from src.llm import client

def detect_source(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify the analytics question by data source. "
                    "Return only: fleet or sql. "
                    "Use fleet ONLY for current fleet size, current vehicle counts, "
                    "or current fleet composition. This data comes from Google Sheets. "
                    "Use sql for revenue, rides, users, payments, customer behavior, "
                    "historical analysis, and any metric grouped by car model. "
                    "Car models for SQL analytics come from the car and carmodel tables. "
                    "Even if a question mentions fleet, vehicle, car, brand, or model, "
                    "use sql whenever it asks for revenue, rides, usage, customers, or historical metrics."
                )
            },
            {"role": "user", "content": question}
        ],
    )

    source = response.choices[0].message.content.strip().lower()
    return source if source in {"fleet", "sql"} else "sql"