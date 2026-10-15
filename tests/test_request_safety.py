import pytest

from security.request_safety import check_request_safety


@pytest.mark.parametrize(
    "message",
    [
        "delete the database",
        "drop all tables",
        "wipe all student records from the database",
        "empty the attendance table completely so we can start fresh",
        "update all student records",
        "truncate the attendance table",
    ],
)
def test_destructive_requests_are_blocked(message):
    safe, reason = check_request_safety(message)

    assert safe is False
    assert reason == "UNSUPPORTED_OR_UNSAFE_REQUEST"


@pytest.mark.parametrize(
    "message",
    [
        "Show my attendance",
        "Show my marks",
        "What are my results?",
        "Are there any empty attendance records?",
    ],
)
def test_normal_read_requests_pass_basic_safety_check(message):
    safe, reason = check_request_safety(message)

    assert safe is True
    assert reason == "REQUEST_PASSED_BASIC_CHECKS"


@pytest.mark.parametrize("message", ["", "   ", "\n\t"])
def test_empty_requests_are_rejected(message):
    safe, reason = check_request_safety(message)

    assert safe is False
    assert reason == "EMPTY_REQUEST"
