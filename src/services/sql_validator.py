def validate_sql(sql: str) -> bool:
    sql_lower = sql.lower().strip()
    forbidden = ["insert ", "update ", "delete ", "drop ", "alter ", "truncate ", "create "]

    if not (sql_lower.startswith("select") or sql_lower.startswith("with")):
        return False

    return not any(word in sql_lower for word in forbidden)