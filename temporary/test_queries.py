"""Structured temporary query objects for standalone demonstrations."""

SAFE_ATTENDANCE_QUERY = {
    "operation": "SELECT",
    "table": "attendance",
    "columns": ["attendance_date", "status"],
    "row_conditions": {"student_id": 101},
}

SAFE_MARKS_QUERY = {
    "operation": "SELECT",
    "table": "marks",
    "columns": ["course_id", "exam_type", "marks"],
    "row_conditions": {"student_id": 101},
}

OTHER_STUDENT_ATTENDANCE = {
    "operation": "SELECT",
    "table": "attendance",
    "columns": ["attendance_date", "status"],
    "row_conditions": {"student_id": 205},
}

MISSING_ROW_RESTRICTION = {
    "operation": "SELECT",
    "table": "attendance",
    "columns": ["attendance_date", "status"],
    "row_conditions": {},
}

UNAUTHORIZED_TABLE = {
    "operation": "SELECT",
    "table": "audit_logs",
    "columns": ["log_id"],
    "row_conditions": {"user_id": 1},
}

UNAUTHORIZED_COLUMN = {
    "operation": "SELECT",
    "table": "attendance",
    "columns": ["attendance_date", "status", "internal_secret"],
    "row_conditions": {"student_id": 101},
}

DELETE_QUERY = {
    "operation": "DELETE",
    "table": "attendance",
    "columns": [],
    "row_conditions": {"student_id": 101},
}

UPDATE_QUERY = {
    "operation": "UPDATE",
    "table": "attendance",
    "columns": ["status"],
    "row_conditions": {"student_id": 101},
}

DROP_QUERY = {
    "operation": "DROP",
    "table": "attendance",
    "columns": [],
    "row_conditions": {},
}

FACULTY_ALLOWED = {
    "operation": "SELECT",
    "table": "attendance",
    "columns": ["student_id", "attendance_date", "status"],
    "row_conditions": {"course_id": 301},
}

FACULTY_OUTSIDE_COURSE = {
    "operation": "SELECT",
    "table": "attendance",
    "columns": ["student_id", "attendance_date", "status"],
    "row_conditions": {"course_id": 401},
}
