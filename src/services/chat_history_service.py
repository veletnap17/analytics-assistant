import os
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()

def get_chat_connection():
    return psycopg2.connect(
        host=os.getenv("CHAT_DB_HOST"),
        port=os.getenv("CHAT_DB_PORT"),
        database=os.getenv("CHAT_DB_NAME"),
        user=os.getenv("CHAT_DB_USER"),
        password=os.getenv("CHAT_DB_PASSWORD")
    )

def save_message(
    session_id: str,
    role: str,
    content: str,
    sql_text: str | None = None,
    data_json=None
):
    conn = get_chat_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO chat_history (
                    session_id,
                    role,
                    content,
                    sql_text,
                    data_json
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                session_id,
                role,
                content,
                sql_text,
                Json(data_json) if data_json is not None else None
            ))

        conn.commit()

    finally:
        conn.close()

def set_chat_title(session_id: str, title: str):
    conn = get_chat_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE chat_history
                SET chat_title = %s
                WHERE id = (
                    SELECT id
                    FROM chat_history
                    WHERE session_id = %s
                      AND role = 'user'
                    ORDER BY created_at
                    LIMIT 1
                )
            """, (title, session_id))

        conn.commit()

    finally:
        conn.close()

def get_sessions():
    conn = get_chat_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT ON (h.session_id)
                    h.session_id,
                    COALESCE(
                        (
                            SELECT t.chat_title
                            FROM chat_history t
                            WHERE t.session_id = h.session_id
                              AND t.chat_title IS NOT NULL
                            ORDER BY t.created_at
                            LIMIT 1
                        ),
                        h.content
                    ) AS title,
                    h.created_at
                FROM chat_history h
                WHERE h.role = 'user'
                ORDER BY h.session_id, h.created_at
            """)

            rows = cursor.fetchall()

            return sorted(
                rows,
                key=lambda x: x[2],
                reverse=True
            )

    finally:
        conn.close()

def load_session(session_id: str):
    conn = get_chat_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    role,
                    content,
                    sql_text,
                    data_json
                FROM chat_history
                WHERE session_id = %s
                ORDER BY created_at
            """, (session_id,))

            return [
                {
                    "role": role,
                    "content": content,
                    "sql": sql,
                    "data": data
                }
                for role, content, sql, data in cursor.fetchall()
            ]

    finally:
        conn.close()

def get_last_sql(session_id: str):
    conn = get_chat_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT sql_text
                FROM chat_history
                WHERE session_id = %s
                  AND sql_text IS NOT NULL
                ORDER BY created_at DESC
                LIMIT 1
            """, (session_id,))

            row = cursor.fetchone()

            return row[0] if row else None

    finally:
        conn.close()

def delete_session(session_id: str):
    conn = get_chat_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM chat_history
                WHERE session_id = %s
            """, (session_id,))

        conn.commit()

    finally:
        conn.close()