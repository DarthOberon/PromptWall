""" Basic audit logging for PromptWall"""
from typing import Any, Dict
from database.connection import get_connection

def log_event(
        user: Dict[str,Any],
        decision: str,
        reason: str,
        table_name: str | None = None,
        operation: str | None = None,
) -> None:
    """"Record an authorizartion decision in the audit log"""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO audit_logs (user_id, decision, reason, table_name, operation)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user.get("user_id"), 
                decision, 
                reason, 
                table_name, 
                operation
            ),
        )
        connection.commit()

    finally:
        cursor.close()
        connection.close()