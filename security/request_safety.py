
"""Deterministic safety checks for natural-language requests."""

import re


# Existing checks for destructive database operations.
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
    r"\bempty\s+(?:the|all|every)\b.{0,50}\b(table|records|database|data)\b",
    r"\bmodify\b",
    r"\boverwrite\b",
    r"\bexecute\s+sql\b",
    r"\brun\s+sql\b",
]


# Basic prompt injection and instruction manipulation patterns.
PROMPT_INJECTION_PATTERNS = [
    # Instruction override attempts
    r"\bignore\s+(?:all\s+)?(?:previous|prior|above|system|developer)\s+instructions\b",
    r"\bdisregard\s+(?:all\s+)?(?:previous|prior|above|system|developer)\s+instructions\b",
    r"\bforget\s+(?:all\s+)?(?:previous|prior|system|developer)\s+instructions\b",
    r"\boverride\s+(?:the\s+)?(?:system|developer|security)\s+instructions\b",

    # Attempts to manipulate the assistant's identity or role
    r"\bact\s+as\s+(?:an?\s+)?(?:admin|administrator|root|unrestricted|unfiltered)\b",
    r"\bpretend\s+(?:to\s+be|you\s+are)\s+(?:an?\s+)?(?:admin|administrator|root)\b",
    r"\bdeveloper\s+mode\b",
    r"\b(?:enable|activate)\s+(?:unrestricted|unfiltered)\s+mode\b",

    # Attempts to bypass security
    r"\bbypass\s+(?:the\s+)?(?:security|authorization|permission|access|safety)\s+(?:checks|rules|restrictions|controls)\b",
    r"\bignore\s+(?:the\s+)?(?:security|authorization|permission|access)\s+(?:rules|checks|restrictions|controls)\b",
    r"\bdisable\s+(?:the\s+)?(?:security|authorization|permission)\s+(?:checks|rules|controls)\b",

    # Attempts to extract hidden instructions
    r"\breveal\s+(?:your\s+)?(?:system|developer)\s+prompt\b",
    r"\bshow\s+(?:me\s+)?(?:your\s+)?(?:system|developer)\s+prompt\b",
    r"\bprint\s+(?:your\s+)?(?:hidden|system|developer)\s+instructions\b",

    # Explicit jailbreak language
    r"\bjailbreak\b",
    r"\bbreak\s+out\s+of\s+(?:your\s+)?(?:restrictions|limitations|safety)\b",
]


def check_request_safety(message: str) -> tuple[bool, str]:
    """
    Return (safe_to_parse, reason).

    This is a basic rule-based filter, not a complete prompt injection
    detection system and not an authorization mechanism.
    """

    if not isinstance(message, str) or not message.strip():
        return False, "EMPTY_REQUEST"

    normalized = message.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, normalized):
            return False, "PROMPT_INJECTION_DETECTED"

    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, normalized):
            return False, "UNSUPPORTED_OR_UNSAFE_REQUEST"

    return True, "REQUEST_PASSED_BASIC_CHECKS"
