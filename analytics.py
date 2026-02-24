from fastapi import APIRouter
from db_clickhouse import client
router = APIRouter()
@router.get("/summary")
def analytics_summary(days: int = None):

    try:
        query = """
        SELECT
            countIf(event_type = 'created') AS total_created,
            countIf(event_type = 'completed') AS total_completed
        FROM todo_events
        """

        if days:
            query = f"""
            SELECT
                countIf(event_type = 'created') AS total_created,
                countIf(event_type = 'completed') AS total_completed
            FROM todo_events
            WHERE event_time >= now() - INTERVAL {days} DAY
            """

        result = client.query(query)

        total_created = result.result_rows[0][0]
        total_completed = result.result_rows[0][1]

        completion_rate = (
            round((total_completed / total_created) * 100, 2)
            if total_created > 0
            else 0
        )

        return {
            "total_created": total_created,
            "total_completed": total_completed,
            "completion_rate": completion_rate
        }

    except Exception as e:
        print("Analytics Error:", e)

        return {
            "total_created": 0,
            "total_completed": 0,
            "completion_rate": 0
        }