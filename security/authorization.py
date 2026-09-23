"""Central fail-closed authorization engine."""

from typing import Any, Dict

from security.permissions import can_access_columns
from security.rbac import can_access_table, can_perform_operation
from security.row_security import check_row_access, requires_row_restriction


def block(reason: str) -> Dict[str, str]:
    return {"decision": "BLOCK", "reason": reason}


def authorize_query(user: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, str]:
    """Authorize in order: operation, table, columns, row-level access."""
    if not user or not query:
        return block("AUTHENTICATION_CONTEXT_MISSING")

    role = user.get("role")
    operation = str(query.get("operation", "")).upper()
    table = query.get("table")
    columns = query.get("columns", [])

    if not can_perform_operation(role, operation):
        return block("OPERATION_NOT_ALLOWED")

    if not can_access_table(role, table):
        return block("TABLE_ACCESS_DENIED")

    if not can_access_columns(role, table, columns):
        return block("COLUMN_ACCESS_DENIED")

    if requires_row_restriction(role, table):
        result = check_row_access(user, query)
        if result != "ALLOW":
            return block(result)

    return {"decision": "ALLOW", "reason": "AUTHORIZED"}
