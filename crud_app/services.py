import time
from functools import wraps

from sqlalchemy import text


def request_timed(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        print(f'Выполнение запроса заняло {time.perf_counter() - start:.3f}')
        return result
    return wrapper


async def get_analytics_dict(session):
    query = text("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN completed THEN 1 ELSE 0 END) AS completed_true,
            SUM(CASE WHEN NOT completed THEN 1 ELSE 0 END) AS completed_false,
            ROUND(EXTRACT(EPOCH FROM AVG(completed_at - created_at)) / 3600, 1) AS avg_hours
        FROM todos
    """)
    row = await session.execute(query)
    row = row.mappings().first()

    by_days = await session.execute(text("""
        SELECT TO_CHAR(created_at, 'Day') AS weekday, COUNT(*) AS count
        FROM todos
        GROUP BY weekday
        ORDER BY MIN(created_at)
    """))

    weekday_distribution = {r['weekday'].strip(): r['count'] for r in by_days.mappings().all()}

    return {
        "total": row["total"],
        "completed_stats": {
            "true": row["completed_true"],
            "false": row["completed_false"]
        },
        "avg_completion_time_hours": row["avg_hours"],
        "weekday_distribution": weekday_distribution
    }
