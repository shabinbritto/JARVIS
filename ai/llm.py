
from dataclasses import dataclass


@dataclass
class AIResult:
    success: bool
    text: str
    reason: str


class AIGateway:
    """
    Central entry point for future AI requests.

    No model is connected. This gateway sends no data anywhere.
    Personal data requires an approved, one-time permission result.
    """

    def __init__(self):
        self.model_connected = False

    def ask(
        self,
        prompt,
        contains_personal_data=False,
        personal_data_result=None,
    ):
        if not isinstance(prompt, str) or not prompt.strip():
            return AIResult(
                False,
                "",
                "Blocked: empty prompt.",
            )

        if contains_personal_data:
            if personal_data_result is None:
                return AIResult(
                    False,
                    "",
                    "Blocked: explicit permission required.",
                )

            if not getattr(
                personal_data_result,
                "allowed",
                False,
            ):
                return AIResult(
                    False,
                    "",
                    "Blocked: personal-data permission was not granted.",
                )

            approved_text = getattr(
                personal_data_result,
                "text",
                None,
            )

            if not isinstance(approved_text, str):
                return AIResult(
                    False,
                    "",
                    "Blocked: invalid approved data.",
                )

        if not self.model_connected:
            return AIResult(
                False,
                "",
                "No AI model is connected. No data was sent.",
            )

        return AIResult(
            False,
            "",
            "AI requests remain disabled until a guarded "
            "model connection is implemented.",
        )

