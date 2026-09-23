"""Secure database gateway.

Only allowlisted structured query objects are translated into SQL. The gateway
never executes raw SQL supplied by a caller.
"""

from typing import Any, Dict, Iterable, Tuple

from database.connection import get_connection
from security.authorization import authorize_query


class DatabaseGateway:
    """Authorize structured requests before executing parameterized SQL."""

    def execute(self, user: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        decision = authorize_query(user, query)
        if decision["decision"] != "ALLOW":
            return decision

        sql, params = build_parameterized_select(query)
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return {
                "decision": "ALLOW",
                "reason": "AUTHORIZED",
                "rows": rows,
            }
        finally:
            cursor.close()
            connection.close()


def build_parameterized_select(query: Dict[str, Any]) -> Tuple[str, Tuple[Any, ...]]:
    """Build a SELECT statement from an already-authorized structured query.

    Identifiers come only from internal allowlists; values are always bound as
    parameters. This function intentionally supports SELECT only.
    """
    table = query["table"]
    columns = query["columns"]
    conditions = query["row_conditions"]

    allowed_tables = {"attendance", "marks", "students", "courses"}
    allowed_columns = {
        "attendance": {"attendance_date", "status", "student_id", "course_id"},
        "marks": {"course_id", "exam_type", "marks", "student_id"},
        "students": {"student_id", "name", "department", "semester"},
        "courses": {"course_id", "course_name", "faculty_id"},
    }

    if table not in allowed_tables:
        raise ValueError("TABLE_NOT_SUPPORTED")
    if not columns or any(column not in allowed_columns[table] for column in columns):
        raise ValueError("COLUMN_NOT_SUPPORTED")
    if not conditions:
        raise ValueError("ROW_RESTRICTION_REQUIRED")

    quoted_columns = ", ".join(f"`{column}`" for column in columns)
    predicates = []
    params = []

    for key, value in conditions.items():
        if key not in allowed_columns[table]:
            raise ValueError("CONDITION_COLUMN_NOT_SUPPORTED")
        predicates.append(f"`{key}` = %s")
        params.append(value)

    sql = f"SELECT {quoted_columns} FROM `{table}` WHERE " + " AND ".join(predicates)
    return sql, tuple(params)
