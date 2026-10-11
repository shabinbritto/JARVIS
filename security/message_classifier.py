import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MessageClassification:
    category: str
    needs_permission: bool
    reason: str


class MessageClassifier:
    SECRET_PATTERNS = [
        re.compile(
            r"(?i)\b(password|passwd|passcode|api[_-]?key|"
            r"access[_-]?token|refresh[_-]?token|"
            r"client_secret|authorization)\s*[:=]"
        ),
        re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
        re.compile(
            r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|"
            r"github_pat_[A-Za-z0-9_]{20,})\b"
        ),
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
        re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    ]

    PERSONAL_HINTS = [
        "my bank",
        "my balance",
        "my salary",
        "my address",
        "my phone number",
        "my birthday",
        "my medical",
        "my health",
        "my exam",
        "my schedule",
        "my personal",
        "my family",
        "my account",
        "my location",
    ]

    def classify(self, message):
        if not isinstance(message, str) or not message.strip():
            return MessageClassification(
                "unknown", True, "Empty or invalid message."
            )

        for pattern in self.SECRET_PATTERNS:
            if pattern.search(message):
                return MessageClassification(
                    "credentials",
                    True,
                    "Possible credentials detected. Never send these to an AI model.",
                )

        lowered = message.lower()

        if any(hint in lowered for hint in self.PERSONAL_HINTS):
            return MessageClassification(
                "personal",
                True,
                "The message may contain personal information.",
            )

        return MessageClassification(
            "unclassified",
            True,
            "The message has not been verified as safe to share.",
        )
