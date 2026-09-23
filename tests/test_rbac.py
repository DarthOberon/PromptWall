from security.rbac import can_access_table, can_perform_operation


def test_student_select_allowed():
    assert can_perform_operation("Student", "SELECT")
    assert can_access_table("Student", "attendance")


def test_student_write_blocked():
    assert not can_perform_operation("Student", "DELETE")
    assert not can_perform_operation("Student", "UPDATE")


def test_unknown_role_blocked():
    assert not can_perform_operation("Unknown", "SELECT")
    assert not can_access_table("Unknown", "attendance")
