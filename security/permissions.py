"""Column-level allowlist permissions."""

from typing import Iterable, Dict, Set

COLUMN_ALLOWLIST: Dict[str, Dict[str, Set[str]]] = {
    "Student": {
        "attendance": {"attendance_date", "status", "course_id"},
        "marks": {"course_id", "exam_type", "marks"},
        "students": {"student_id", "name", "department", "semester"},
        "courses": {"course_id", "course_name"},
    },
    "Faculty": {
        "attendance": {"attendance_date", "status", "student_id", "course_id"},
        "marks": {"course_id", "exam_type", "marks", "student_id"},
        "students": {"student_id", "name", "department", "semester"},
        "courses": {"course_id", "course_name", "faculty_id"},
    },
    "Admin": {
        "attendance": {"attendance_date", "status", "student_id", "course_id"},
        "marks": {"course_id", "exam_type", "marks", "student_id"},
        "students": {"student_id", "name", "department", "semester", "user_id"},
        "courses": {"course_id", "course_name", "faculty_id"},
        "audit_logs": {"log_id", "user_id", "decision", "reason", "table_name", "operation", "created_at"},
        "security_policies": {"policy_id", "role_name", "table_name", "requires_row_restriction"},
    },
}


def can_access_columns(role: str, table: str, columns: Iterable[str]) -> bool:
    allowed = COLUMN_ALLOWLIST.get(role, {}).get(table, set())
    return set(columns).issubset(allowed)
