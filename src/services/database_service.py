import os
import psycopg2
from dotenv import load_dotenv
from src.services.sql_validator import validate_sql
import re

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def enforce_limit(sql: str, limit: int = 1000) -> str:
    clean = sql.strip().rstrip(";")
    lower = clean.lower()

    aggregates = ["count(", "sum(", "avg(", "min(", "max(", "group by"]

    if any(x in lower for x in aggregates):
        return clean + ";"

    if re.search(r"\blimit\s+\d+", lower):
        return clean + ";"

    return f"{clean}\nLIMIT {limit};"

def execute_query(sql: str):
    if not validate_sql(sql):
        raise ValueError("Unsafe SQL query blocked.")

    sql = enforce_limit(sql)
    conn = get_connection()

    try:
        conn.set_session(readonly=True)

        with conn.cursor() as cursor:
            cursor.execute("SET statement_timeout = '60s'")
            cursor.execute(sql)

            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

        return columns, rows

    finally:
        conn.close()