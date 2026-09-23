"""Role-based access control."""

from typing import Dict, Set

ROLES = {"Student", "Faculty", "Admin"}

TABLE_ACCESS: Dict[str, Set[str]] = {
    "Student": {"attendance", "marks", "students", "courses"},
    "Faculty": {"attendance", "marks", "students", "courses"},
    "Admin": {"attendance", "marks", "students", "courses", "audit_logs", "security_policies"},
}

READ_OPERATIONS = {"SELECT"}


def is_valid_role(role: str) -> bool:
    return role in ROLES


def can_access_table(role: str, table: str) -> bool:
    return role in TABLE_ACCESS and table in TABLE_ACCESS[role]


def can_perform_operation(role: str, operation: str) -> bool:
    return role in ROLES and operation.upper() in READ_OPERATIONS
