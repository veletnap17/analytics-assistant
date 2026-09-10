import json
from src.llm import client

def generate_followups(question: str, answer: str) -> list[str]:
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an analytics assistant for a carsharing company. "
                    "Suggest exactly 3 short follow-up analytics questions. "
                    "Each suggestion must be answerable using the currently available data: "
                    "PostgreSQL for rides, users, revenue, payments and car models; "
                    "Google Sheets for current fleet counts. "
                    "Do not suggest external data such as weather, events or market data. "
                    "Do not assume undocumented customer segments or columns. "
                    "Prefer comparisons, breakdowns and related KPIs. "
                    "Keep each suggestion under 8 words. "
                    "Do not start with 'Do you want' or 'Should I'. "
                    "Return only a JSON array of strings."
                    "Use only documented metrics: revenue, rides, FTR, NTR, MAU, paying users, "
                    "revenue per user, average revenue per ride, and current fleet. "
                    "Do not introduce undefined metrics such as new users unless explicitly documented. "
                )
            },
            {"role": "user", "content": f"Question: {question}\nAnswer: {answer}"}
        ]
    )

    try:
        return json.loads(response.choices[0].message.content)[:3]
    except Exception:
        return []