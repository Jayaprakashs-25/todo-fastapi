from fastapi import APIRouter
from datetime import datetime
from db_clickhouse import client
from ai.gemini_client import ask_gemini
router = APIRouter()
@router.get("/productivity-summary")
def productivity_summary():

    try:
        result = client.query("""
            SELECT
                countIf(event_type = 'created') AS total_created,
                countIf(event_type = 'completed') AS total_completed
            FROM todo_events
        """)

        total_created = result.result_rows[0][0]
        total_completed = result.result_rows[0][1]

        if total_created == 0:
            return {
                "message": "No productivity data available yet."
            }

        completion_rate = round(
            (total_completed / total_created) * 100, 2
        )

        prompt = f"""
You are a productivity assistant.

Here is user productivity data:
- Total Todos Created: {total_created}
- Total Todos Completed: {total_completed}
- Completion Rate: {completion_rate}%

Provide:
1. Short performance summary
2. One improvement suggestion
3. Motivational closing sentence

Keep response under 150 words.
"""

        ai_summary = ask_gemini(prompt)

        return {
            "total_created": total_created,
            "total_completed": total_completed,
            "completion_rate": completion_rate,
            "ai_summary": ai_summary
        }

    except Exception as e:
        return {"error": str(e)}