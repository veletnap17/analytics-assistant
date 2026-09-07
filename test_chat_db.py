from src.services.chat_history_service import get_chat_connection

conn = get_chat_connection()
print("Connected to chat DB")
conn.close()