from src.services.database_service import execute_query
from src.services.fleet_service import get_fleet_change

def change(current, previous):
    return round((current - previous) / previous * 100, 1) if previous else 0

def get_kpis():
    revenue_sql = """
        SELECT
            COALESCE(SUM(amountfromcardinkops + amountfromcashinkops)
                FILTER (WHERE withdrawaldatetime >= CURRENT_DATE - INTERVAL '30 days'), 0)::numeric / 100,
            COALESCE(SUM(amountfromcardinkops + amountfromcashinkops)
                FILTER (WHERE withdrawaldatetime >= CURRENT_DATE - INTERVAL '60 days'
                    AND withdrawaldatetime < CURRENT_DATE - INTERVAL '30 days'), 0)::numeric / 100
        FROM withdrawal
        WHERE cancelled = false AND ispaid = true;
    """

    activity_sql = """
        SELECT
            COUNT(*) FILTER (WHERE enddatetime >= CURRENT_DATE - INTERVAL '30 days'),
            COUNT(*) FILTER (WHERE enddatetime >= CURRENT_DATE - INTERVAL '60 days'
                AND enddatetime < CURRENT_DATE - INTERVAL '30 days'),
            COUNT(DISTINCT customerid) FILTER (WHERE enddatetime >= CURRENT_DATE - INTERVAL '30 days'),
            COUNT(DISTINCT customerid) FILTER (WHERE enddatetime >= CURRENT_DATE - INTERVAL '60 days'
                AND enddatetime < CURRENT_DATE - INTERVAL '30 days')
        FROM "Order"
        WHERE totalcostincops > 0 AND enddatetime IS NOT NULL;
    """

    _, rev = execute_query(revenue_sql)
    _, act = execute_query(activity_sql)

    revenue, revenue_prev = map(float, rev[0])
    rides, rides_prev, users, users_prev = map(int, act[0])
    fleet = get_fleet_change()

    return {
        "revenue": round(revenue),
        "rides": rides,
        "paying_users": users,
        "fleet_size": fleet["current"],
        "fleet_change": fleet["change"],
        "revenue_change": change(revenue, revenue_prev),
        "rides_change": change(rides, rides_prev),
        "paying_users_change": change(users, users_prev)
    }