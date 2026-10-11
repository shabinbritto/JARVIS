import re
import secrets
from dataclasses import dataclass


ALLOWED_CATEGORIES = {
    "study",
    "schedule",
    "finance",
    "personal",
    "public",
}

NEVER_SHARE_CATEGORIES = {
    "passwords",
    "private_keys",
    "authentication_tokens",
    "credentials",
}


@dataclass(frozen=True)
class PrivacyRequest:
    request_id: str
    purpose: str
    category: str
    content: str


@dataclass(frozen=True)
class ApprovalToken:
    request_id: str
    value: str


@dataclass
class PrivacyResult:
    allowed: bool
    text: str
    reason: str


class PrivacyShield:
    def __init__(self):
        self._pending = {}
        self._tokens = {}

    def create_request(self, purpose, category, content):
        if category in NEVER_SHARE_CATEGORIES:
            return PrivacyResult(
                False, "", "Blocked: credentials cannot be shared."
            )

        if category not in ALLOWED_CATEGORIES:
            return PrivacyResult(
                False, "", "Blocked: unknown category."
            )

        if not isinstance(content, str) or not content.strip():
            return PrivacyResult(
                False, "", "Blocked: invalid content."
            )

        if self.redact_credentials(content) != content:
            return PrivacyResult(
                False,
                "",
                "Blocked: possible credentials detected. Remove secrets before creating this request.",
            )

        request = PrivacyRequest(
            request_id=secrets.token_urlsafe(24),
            purpose=purpose,
            category=category,
            content=content,
        )
        self._pending[request.request_id] = request
        return request

    def _approve_once(self, request):
        if not isinstance(request, PrivacyRequest):
            return None

        if self._pending.get(request.request_id) is not request:
            return None

        token = ApprovalToken(
            request_id=request.request_id,
            value=secrets.token_urlsafe(32),
        )
        self._tokens[request.request_id] = token
        return token

    def prepare_for_ai(self, request, token=None):
        if not isinstance(request, PrivacyRequest):
            return PrivacyResult(
                False, "", "Blocked: invalid request."
            )

        request_id = request.request_id

        if self._pending.get(request_id) is not request:
            return PrivacyResult(
                False, "", "Blocked: request is no longer valid."
            )

        if token is None or self._tokens.get(request_id) is not token:
            return PrivacyResult(
                False, "", "Blocked: explicit permission required."
            )

        del self._pending[request_id]
        self._tokens.pop(request_id, None)

        return PrivacyResult(
            True, request.content, "Approved once for this request."
        )

    def cancel_request(self, request):
        if not isinstance(request, PrivacyRequest):
            return

        request_id = request.request_id
        self._pending.pop(request_id, None)
        self._tokens.pop(request_id, None)

    @staticmethod
    def redact_credentials(text):
        patterns = [
            (
                r"""(?i)\b(password|passwd|passcode|secret|client_secret|api[_-]?key|access[_-]?token|refresh[_-]?token|auth[_-]?token|token|authorization)\s*[:=]\s*(?:Bearer\s+)?["']?[^\s,;"'<>]+["']?""",
                r"\1=[REDACTED]",
            ),
            (
                r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+",
                "Bearer [REDACTED]",
            ),
            (
                r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----",
                "[PRIVATE KEY REDACTED]",
            ),
            (
                r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b",
                "[GITHUB TOKEN REDACTED]",
            ),
            (
                r"\bAKIA[0-9A-Z]{16}\b",
                "[AWS ACCESS KEY REDACTED]",
            ),
            (
                r"\bAIza[0-9A-Za-z_-]{30,}\b",
                "[GOOGLE API KEY REDACTED]",
            ),
            (
                r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b",
                "[SLACK TOKEN REDACTED]",
            ),
            (
                r"\beyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b",
                "[JWT TOKEN REDACTED]",
            ),
        ]

        result = text
        for pattern, replacement in patterns:
            result = re.sub(
                pattern,
                replacement,
                result,
                flags=re.DOTALL,
            )
        return result
