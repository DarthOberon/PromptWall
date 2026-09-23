from security.permissions import can_access_columns


def test_student_allowed_columns():
    assert can_access_columns("Student", "attendance", ["attendance_date", "status"])


def test_student_sensitive_column_blocked():
    assert not can_access_columns("Student", "attendance", ["attendance_date", "internal_secret"])


def test_admin_allowlist():
    assert can_access_columns("Admin", "audit_logs", ["log_id", "decision"])
