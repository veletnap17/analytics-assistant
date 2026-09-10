from src.llm import client

def detect_source(question: str) -> str:
    q = question.lower()

    fleet_keywords = [
        "fleet",
        "fleet size",
        "number of cars",
        "how many cars",
        "how many vehicles",
        "vehicle mix",
        "car mix",
    ]

    if any(x in q for x in fleet_keywords):
        return "fleet"

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify the user's analytics question by data source. "
                    "Return only one word: fleet or sql. "
                    "Use fleet for questions about current fleet size, current vehicle counts, "
                    "fleet composition, vehicle mix, or current counts by model. "
                    "Use sql for rides, users, revenue, payments, historical analytics, "
                    "customer behavior, and database analysis."
                ),
            },
            {"role": "user", "content": question},
        ],
    )

    source = response.choices[0].message.content.strip().lower()
    return source if source in {"fleet", "sql"} else "sql"