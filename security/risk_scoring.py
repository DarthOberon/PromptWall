"""Rule-based risk scoring for PromptWall requests."""


def calculate_risk_score(decision: str, reason: str) -> int:
    """Return a heuristic risk score from 0 (low) to 100 (high)."""

    if decision == "ALLOW":
        return 5

    reason = (reason or "").upper()

    risk_scores = {
        "AUTHENTICATION_REQUIRED": 70,
        "ROW_ACCESS_DENIED": 85,
        "CROSS_STUDENT_ACCESS_DENIED": 85,
        "TABLE_ACCESS_DENIED": 85,
        "COLUMN_ACCESS_DENIED": 80,
        "OPERATION_NOT_ALLOWED": 95,
        "UNSUPPORTED_OPERATION": 95,
        "ROW_RESTRICTION_MISSING": 65,
        "REQUEST_REJECTED": 40,
        "INVALID_MODEL_RESPONSE": 50,
        "REQUEST_PROCESSING_FAILED": 50,
    }

    return risk_scores.get(reason, 50)
