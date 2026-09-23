"""Row-Level Security rules."""

from typing import Any, Dict, Set

RLS_TABLES = {"attendance", "marks", "students"}


def requires_row_restriction(role: str, table: str) -> bool:
    return role in {"Student", "Faculty"} and table in RLS_TABLES


def check_row_access(user: Dict[str, Any], query: Dict[str, Any]) -> str:
    role = user.get("role")
    table = query.get("table")
    conditions = query.get("row_conditions") or {}

    if role == "Admin":
        return "ALLOW"

    if role == "Student":
        student_id = user.get("student_id")
        if student_id is None:
            return "ROW_ACCESS_DENIED"
        if "student_id" not in conditions:
            return "ROW_RESTRICTION_MISSING"
        return "ALLOW" if conditions["student_id"] == student_id else "ROW_ACCESS_DENIED"

    if role == "Faculty":
        faculty_id = user.get("faculty_id")
        permitted_courses: Set[int] = set(user.get("permitted_course_ids", []))
        if faculty_id is None:
            return "ROW_ACCESS_DENIED"

        if table in {"attendance", "marks"}:
            if "course_id" not in conditions:
                return "ROW_RESTRICTION_MISSING"
            return "ALLOW" if conditions["course_id"] in permitted_courses else "ROW_ACCESS_DENIED"

        if table == "students":
            if "course_id" not in conditions:
                return "ROW_RESTRICTION_MISSING"
            return "ALLOW" if conditions["course_id"] in permitted_courses else "ROW_ACCESS_DENIED"

    return "ROW_ACCESS_DENIED"
