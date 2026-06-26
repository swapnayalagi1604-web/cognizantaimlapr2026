# guardrails.py

import re

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "forget all instructions",
    "act as",
    "system prompt",
    "jailbreak"
]

SENSITIVE_PATTERNS = [
    "password",
    "bank account",
    "aadhaar",
    "pan number",
    "medical record"
]


def validate_input(question):

    q = question.lower()

    for pattern in INJECTION_PATTERNS:
        if pattern in q:
            return False, "Prompt injection attempt detected."

    for pattern in SENSITIVE_PATTERNS:
        if pattern in q:
            return False, "Access to confidential information is restricted."

    return True, ""


def validate_output(answer):

    ans = answer.lower()

    for pattern in SENSITIVE_PATTERNS:
        if pattern in ans:
            return "Response blocked due to sensitive information."

    return answer


def mask_pii(text):

    text = re.sub(
        r'\S+@\S+',
        '[EMAIL]',
        text
    )

    text = re.sub(
        r'\b\d{10}\b',
        '[PHONE]',
        text
    )

    return text