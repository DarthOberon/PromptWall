from security.authorization import authorize_query
from temporary.test_queries import (
    SAFE_ATTENDANCE_QUERY,
    SAFE_MARKS_QUERY,
    OTHER_STUDENT_ATTENDANCE,
    MISSING_ROW_RESTRICTION,
    UNAUTHORIZED_TABLE,
    UNAUTHORIZED_COLUMN,
    DELETE_QUERY,
    UPDATE_QUERY,
    DROP_QUERY,
    FACULTY_ALLOWED,
    FACULTY_OUTSIDE_COURSE,
)
from temporary.test_users import TEST_USERS


def test_student_own_attendance_allowed():
    result = authorize_query(TEST_USERS["student_101"], SAFE_ATTENDANCE_QUERY)
    assert result == {"decision": "ALLOW", "reason": "AUTHORIZED"}


def test_student_own_marks_allowed():
    result = authorize_query(TEST_USERS["student_101"], SAFE_MARKS_QUERY)
    assert result == {"decision": "ALLOW", "reason": "AUTHORIZED"}


def test_student_other_attendance_blocked():
    result = authorize_query(TEST_USERS["student_101"], OTHER_STUDENT_ATTENDANCE)
    assert result["decision"] == "BLOCK"
    assert result["reason"] == "ROW_ACCESS_DENIED"


def test_missing_row_restriction_blocked():
    result = authorize_query(TEST_USERS["student_101"], MISSING_ROW_RESTRICTION)
    assert result["reason"] == "ROW_RESTRICTION_MISSING"


def test_unauthorized_table_blocked():
    result = authorize_query(TEST_USERS["student_101"], UNAUTHORIZED_TABLE)
    assert result["reason"] == "TABLE_ACCESS_DENIED"


def test_unauthorized_column_blocked():
    result = authorize_query(TEST_USERS["student_101"], UNAUTHORIZED_COLUMN)
    assert result["reason"] == "COLUMN_ACCESS_DENIED"


def test_delete_blocked():
    result = authorize_query(TEST_USERS["student_101"], DELETE_QUERY)
    assert result["reason"] == "OPERATION_NOT_ALLOWED"


def test_update_blocked():
    result = authorize_query(TEST_USERS["student_101"], UPDATE_QUERY)
    assert result["reason"] == "OPERATION_NOT_ALLOWED"


def test_drop_blocked():
    result = authorize_query(TEST_USERS["student_101"], DROP_QUERY)
    assert result["reason"] == "OPERATION_NOT_ALLOWED"


def test_faculty_permitted_course_allowed():
    result = authorize_query(TEST_USERS["faculty_201"], FACULTY_ALLOWED)
    assert result == {"decision": "ALLOW", "reason": "AUTHORIZED"}


def test_faculty_outside_course_blocked():
    result = authorize_query(TEST_USERS["faculty_201"], FACULTY_OUTSIDE_COURSE)
    assert result["reason"] == "ROW_ACCESS_DENIED"


def test_admin_access_allowed():
    query = {
        "operation": "SELECT",
        "table": "audit_logs",
        "columns": ["log_id", "decision"],
        "row_conditions": {},
    }
    result = authorize_query(TEST_USERS["admin_001"], query)
    assert result == {"decision": "ALLOW", "reason": "AUTHORIZED"}


def test_unknown_role_blocked():
    user = {"user_id": 999, "role": "Unknown"}
    result = authorize_query(user, SAFE_ATTENDANCE_QUERY)
    assert result["decision"] == "BLOCK"


def test_parameterized_query_builder():
    from database.gateway import build_parameterized_select

    sql, params = build_parameterized_select(SAFE_ATTENDANCE_QUERY)
    assert "%s" in sql
    assert params == (101,)
    assert "101" not in sql


def test_gateway_rejects_unsupported_raw_query_shape():
    from database.gateway import build_parameterized_select

    raw = {"sql": "DROP TABLE attendance"}
    try:
        build_parameterized_select(raw)
        assert False, "Expected structured query validation to fail"
    except (KeyError, ValueError):
        pass
