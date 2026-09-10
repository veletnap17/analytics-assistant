import json
from src.llm import client
from src.services.fleet_service import get_latest_fleet, get_fleet_by_model

def handle_fleet_question(question: str):
    fleet = get_latest_fleet()
    models = get_fleet_by_model()

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You analyze questions about a vehicle fleet. "
                    "Return JSON only with fields: action, include, exclude. "
                    "Allowed actions: total, breakdown, count_matching. "
                    "Use total for total fleet size. "
                    "Use breakdown for fleet composition by model. "
                    "Use count_matching when the user asks for specific brands/models or exclusions. "
                    "include and exclude must be arrays of lowercase search terms."
                ),
            },
            {"role": "user", "content": question},
        ],
    )

    plan = json.loads(response.choices[0].message.content)
    action = plan.get("action")
    include = plan.get("include", [])
    exclude = plan.get("exclude", [])

    if action == "total":
        return f"Current fleet size is {fleet['Total Fleet']} vehicles as of {fleet['Date']}.", None

    if action == "breakdown":
        data = [{"model": model, "vehicles": count} for model, count in models.items()]
        return f"Fleet breakdown as of {fleet['Date']}.", data

    filtered = {
        model: count for model, count in models.items()
        if (not include or any(x in model.lower() for x in include))
        and not any(x in model.lower() for x in exclude)
    }

    total = sum(filtered.values())
    return f"Matching fleet size is {total} vehicles as of {fleet['Date']}.", filtered