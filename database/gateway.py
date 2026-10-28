"""Secure database gateway.

Only allowlisted structured query objects are translated into SQL. The gateway
never executes raw SQL supplied by a caller.
"""

from typing import Any, Dict, Tuple

from security.risk_scoring import calculate_risk_score

from streamlit import user

from database.connection import get_connection
from security.authorization import authorize_query
from security.audit import log_event


class DatabaseGateway:
    """Authorize structured requests before executing parameterized SQL."""
    def execute(self, user: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(user, dict) or not isinstance(query, dict):
            return {
                "decision": "BLOCK",
                "reason": "AUTHENTICATION_CONTEXT_MISSING",
            }

        decision = authorize_query(user, query)
        table = query.get("table")
        operation = query.get("operation")

        if decision["decision"] != "ALLOW":
            risk_score = calculate_risk_score(
                decision["decision"], decision["reason"]
            )
            log_event(
                user,
                decision["decision"],
                decision["reason"],
                table,
                operation,
                risk_score,
            )
            return {**decision, "risk_score": risk_score}

        try:
            sql, params = build_parameterized_select(query, user)
        except ValueError as exc:
            reason = str(exc)
            risk_score = calculate_risk_score("BLOCK", reason)
            log_event(user, "BLOCK", reason, table, operation, risk_score)
            return {
                "decision": "BLOCK",
                "reason": reason,
                "risk_score": risk_score,
            }

        risk_score = calculate_risk_score("ALLOW", "AUTHORIZED")
        log_event(user, "ALLOW", "AUTHORIZED", table, operation, risk_score)

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return {
                "decision": "ALLOW",
                "reason": "AUTHORIZED",
                "rows": rows,
                "risk_score": risk_score,
            }
        finally:
            cursor.close()
            connection.close()



def build_parameterized_select(query: Dict[str, Any], user: Dict[str, Any],) -> Tuple[str, Tuple[Any, ...]]:
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
    if table == "courses" and query.get("subject") == "self" and user.get("role") == "Faculty":
        if user.get("role") != "Faculty" or user.get("faculty_id") is None:
            raise ValueError("FACULTY_COURSE_SCOPE_REQUIRED")

        allowed_course_columns = {"course_id", "course_name", "faculty_id"}
        if not columns or any(
            column not in allowed_course_columns for column in columns
        ):
            raise ValueError("COLUMN_NOT_SUPPORTED")

        quoted_columns = ", ".join(f"`courses`.`{column}`" for column in columns)
        sql = (
            f"SELECT {quoted_columns} "
            "FROM `courses` "
            "JOIN `faculty_course_access` "
            "ON `courses`.`course_id` = `faculty_course_access`.`course_id` "
            "WHERE `faculty_course_access`.`faculty_id` = %s"
        )
        return sql, (user["faculty_id"],) 
        
    if not conditions and user.get("role") != "Admin":
        raise ValueError("ROW_RESTRICTION_REQUIRED")

    quoted_columns = ", ".join(f"`{column}`" for column in columns)
    predicates = []
    params = []

    if table == "students" and "course_id" in conditions:
        for key in conditions:
            if key != "course_id" and key not in allowed_columns[table]:
                raise ValueError("CONDITION_COLUMN_NOT_SUPPORTED")

        predicates.append("`student_course`.`course_id` = %s")
        params.append(conditions["course_id"])

        for key, value in conditions.items():
            if key == "course_id":
                continue
            predicates.append(f"`students`.`{key}` = %s")
            params.append(value)

        sql = (
            f"SELECT" + ", ".join(f"`students`.`{column}`" for column in columns) + " " # FLAGGED FOR LATER REVIEW
            f"FROM `students` "
            f"JOIN `student_course` "
            f"ON `students`.`student_id` = `student_course`.`student_id` "
            f"WHERE " + " AND ".join(predicates)
        )

        return sql, tuple(params)
 

    for key, value in conditions.items():
        if key not in allowed_columns[table]:
            raise ValueError("CONDITION_COLUMN_NOT_SUPPORTED")
        predicates.append(f"`{key}` = %s")
        params.append(value)

    if predicates:
        sql = (f"SELECT {quoted_columns} FROM `{table}` WHERE " + " AND ".join(predicates))
    else:
        sql = f"SELECT {quoted_columns} FROM `{table}`"
     #sql = f"SELECT {quoted_columns} FROM `{table}` WHERE " + " AND ".join(predicates)
    return sql, tuple(params)
