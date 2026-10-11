import unittest

from security.message_classifier import MessageClassifier

class TestMessageClassifier(unittest.TestCase):


    def setUp(self):
        self.classifier = MessageClassifier()
    def test_personal_message_is_detected(self):
        result = self.classifier.classify("My exam is on Monday")
        self.assertEqual(result.category, "personal")
        self.assertTrue(result.needs_permission)

    def test_bank_information_is_detected(self):
        result = self.classifier.classify("My bank balance is 5000")
        self.assertEqual(result.category, "personal")
        self.assertTrue(result.needs_permission)

    def test_password_is_flagged(self):
        result = self.classifier.classify("password=mySecret123")
        self.assertEqual(result.category, "credentials")
        self.assertTrue(result.needs_permission)

    def test_api_key_field_is_flagged(self):
        result = self.classifier.classify("api_key=example123")
        self.assertEqual(result.category, "credentials")
        self.assertTrue(result.needs_permission)

    def test_unknown_message_requires_permission(self):
        result = self.classifier.classify("Tell me about Python")
        self.assertEqual(result.category, "unclassified")
        self.assertTrue(result.needs_permission)

    def test_empty_message_is_rejected(self):
         result = self.classifier.classify("")
         self.assertEqual(result.category, "unknown")
         self.assertTrue(result.needs_permission)


if __name__ == "__main__":
    unittest.main()