from security.row_security import check_row_access


STUDENT_101 = {"user_id": 1, "student_id": 101, "role": "Student"}
FACULTY_201 = {"user_id": 6, "faculty_id": 201, "role": "Faculty", "permitted_course_ids": [301, 302]}
ADMIN = {"user_id": 8, "role": "Admin"}


def test_student_own_row_allowed():
    query = {"table": "attendance", "row_conditions": {"student_id": 101}}
    assert check_row_access(STUDENT_101, query) == "ALLOW"


def test_student_other_row_blocked():
    query = {"table": "attendance", "row_conditions": {"student_id": 205}}
    assert check_row_access(STUDENT_101, query) == "ROW_ACCESS_DENIED"


def test_student_missing_restriction_blocked():
    query = {"table": "attendance", "row_conditions": {}}
    assert check_row_access(STUDENT_101, query) == "ROW_RESTRICTION_MISSING"


def test_faculty_course_allowed():
    query = {"table": "attendance", "row_conditions": {"course_id": 301}}
    assert check_row_access(FACULTY_201, query) == "ALLOW"


def test_faculty_course_denied():
    query = {"table": "attendance", "row_conditions": {"course_id": 401}}
    assert check_row_access(FACULTY_201, query) == "ROW_ACCESS_DENIED"


def test_admin_broad_policy():
    query = {"table": "attendance", "row_conditions": {}}
    assert check_row_access(ADMIN, query) == "ALLOW"
