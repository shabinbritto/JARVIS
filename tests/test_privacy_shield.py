
import unittest

from security.privacy_shield import (
    PrivacyShield,
    PrivacyRequest,
)


class TestPrivacyShield(unittest.TestCase):

    def setUp(self):
        self.shield = PrivacyShield()

    def create_study_request(self):
        request = self.shield.create_request(
            "study_plan",
            "study",
            "My exam is Monday",
        )

        self.assertIsInstance(request, PrivacyRequest)
        return request

    def test_blocks_without_token(self):
        request = self.create_study_request()

        result = self.shield.prepare_for_ai(request)

        self.assertFalse(result.allowed)
        self.assertEqual(result.text, "")

    def test_allows_one_approved_request(self):
        request = self.create_study_request()

        token = self.shield._approve_once(request)
        result = self.shield.prepare_for_ai(request, token)

        self.assertTrue(result.allowed)
        self.assertEqual(result.text, "My exam is Monday")

    def test_token_cannot_be_reused(self):
        request = self.create_study_request()
        token = self.shield._approve_once(request)

        first_result = self.shield.prepare_for_ai(request, token)
        second_result = self.shield.prepare_for_ai(request, token)

        self.assertTrue(first_result.allowed)
        self.assertFalse(second_result.allowed)

    def test_password_category_is_blocked(self):
        result = self.shield.create_request(
            "general",
            "passwords",
            "fake password",
        )

        self.assertFalse(result.allowed)
        self.assertEqual(result.text, "")

    def test_password_in_content_is_blocked(self):
        result = self.shield.create_request(
            "study_plan",
            "study",
            "My exam is Monday. password=example123",
        )

        self.assertFalse(result.allowed)
        self.assertEqual(result.text, "")
        self.assertIn("credentials detected", result.reason)

    def test_github_token_is_blocked(self):
        result = self.shield.create_request(
            "general",
            "study",
            "Token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
        )

        self.assertFalse(result.allowed)
        self.assertEqual(result.text, "")

    def test_aws_access_key_is_blocked(self):
        result = self.shield.create_request(
            "general",
            "study",
            "Key: AKIA1234567890ABCDEF",
        )

        self.assertFalse(result.allowed)
        self.assertEqual(result.text, "")

    def test_cancelled_request_cannot_be_used(self):
        request = self.create_study_request()
        token = self.shield._approve_once(request)

        self.shield.cancel_request(request)
        result = self.shield.prepare_for_ai(request, token)

        self.assertFalse(result.allowed)

    def test_new_request_works_after_previous_request_is_cancelled(self):
        first_request = self.create_study_request()
        self.shield.cancel_request(first_request)

        second_request = self.create_study_request()

        self.assertIsInstance(second_request, PrivacyRequest)

        token = self.shield._approve_once(second_request)
        result = self.shield.prepare_for_ai(
            second_request,
            token,
        )

        self.assertTrue(result.allowed)
        self.assertEqual(result.text, "My exam is Monday")


    def test_personal_message_is_classified(self):
        from security.message_classifier import MessageClassifier

        result = MessageClassifier().classify("My bank balance is 5000")
        self.assertEqual(result.category, "personal")
        self.assertTrue(result.needs_permission)

    def test_unknown_message_requires_permission(self):
        from security.message_classifier import MessageClassifier

        result = MessageClassifier().classify(
            "Explain how a Python loop works"
        )
        self.assertEqual(result.category, "unclassified")
        self.assertTrue(result.needs_permission)

    def test_password_message_is_flagged_as_credentials(self):
        from security.message_classifier import MessageClassifier

        result = MessageClassifier().classify("password=example123")
        self.assertEqual(result.category, "credentials")
        self.assertTrue(result.needs_permission)


if __name__ == "__main__":
    unittest.main()