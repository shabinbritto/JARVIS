
import unittest

from ai.llm import AIGateway


class TestAIGateway(unittest.TestCase):

    def setUp(self):
        self.gateway = AIGateway()

    def test_no_model_is_connected(self):
        result = self.gateway.ask("Explain Python")

        self.assertFalse(result.success)
        self.assertIn(
            "No AI model is connected",
            result.reason,
        )

    def test_empty_prompt_is_blocked(self):
        result = self.gateway.ask("   ")

        self.assertFalse(result.success)
        self.assertEqual(result.text, "")

    def test_personal_data_without_permission_is_blocked(self):
        result = self.gateway.ask(
            "Create a study plan",
            contains_personal_data=True,
        )

        self.assertFalse(result.success)
        self.assertEqual(result.text, "")
        self.assertIn(
            "explicit permission required",
            result.reason,
        )

    def test_denied_personal_data_is_blocked(self):
        class FakePermissionResult:
            allowed = False
            text = "My private information"

        result = self.gateway.ask(
            "Help me",
            contains_personal_data=True,
            personal_data_result=FakePermissionResult(),
        )

        self.assertFalse(result.success)
        self.assertEqual(result.text, "")
        self.assertIn(
            "permission was not granted",
            result.reason,
        )

    def test_approved_data_still_is_not_sent_without_model(self):
        class FakePermissionResult:
            allowed = True
            text = "My exam is Monday"

        result = self.gateway.ask(
            "Create a study plan",
            contains_personal_data=True,
            personal_data_result=FakePermissionResult(),
        )

        self.assertFalse(result.success)
        self.assertIn(
            "No AI model is connected",
            result.reason,
        )


if __name__ == "__main__":
    unittest.main()

