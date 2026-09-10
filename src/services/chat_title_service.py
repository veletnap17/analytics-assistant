from src.llm import client

def generate_chat_title(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Create a short title for an analytics chat. "
                    "Use 3-6 words. "
                    "Keep it clear and specific. "
                    "Do not use quotes, punctuation or filler words. "
                    "Examples: Monthly rides 2026, Revenue by car model, "
                    "Unpaid rides analysis, Current fleet size. "
                    "Return only the title."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content.strip()