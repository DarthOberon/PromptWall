"""Basic deterministic safety checks for natural-language requests."""

import re


UNSAFE_PATTERNS = [
    r"\bdelete\b",
    r"\bdrop\b",
    r"\btruncate\b",
    r"\bupdate\b",
    r"\binsert\b",
    r"\balter\b",
    r"\bcreate\b",
    r"\bremove\b",
    r"\bdestroy\b",
    r"\bwipe\b",
    r"\bmodify\b",
    r"\boverwrite\b",
    r"\bexecute\s+sql\b",
    r"\brun\s+sql\b",
]


def check_request_safety(message: str) -> tuple[bool, str]:
    """Return (safe_to_parse, reason); this does not authorize queries."""

    if not isinstance(message, str) or not message.strip():
        return False, "EMPTY_REQUEST"

    normalized = message.lower()

    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, normalized):
            return False, "UNSUPPORTED_OR_UNSAFE_REQUEST"

    return True, "REQUEST_PASSED_BASIC_CHECKS"
