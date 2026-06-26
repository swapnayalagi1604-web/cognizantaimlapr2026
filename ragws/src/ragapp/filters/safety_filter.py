from better_profanity import profanity

profanity.load_censor_words()

BLOCKED_TOPICS = [
    "caller id",
    "personal phone number",
    "home address",
    "bank account",
    "pin",
    "password",
    "confidential"
]

def input_safety_check(question: str):
    q = question.lower()

    if profanity.contains_profanity(q):
        return False, "Your question contains inappropriate language."

    for topic in BLOCKED_TOPICS:
        if topic in q:
            return False, "I cannot answer questions about private or confidential employee information."

    return True, ""


def output_safety_check(answer: str):
    blocked_patterns = [
        "password",
        "bank account",
        "pin",
        "aadhaar",
        "pan number",
         "personal phone"
    ]

    ans = answer.lower()

    for pattern in blocked_patterns:
        if pattern in ans:
            return "The answer may contain sensitive information and cannot be displayed."

    return answer