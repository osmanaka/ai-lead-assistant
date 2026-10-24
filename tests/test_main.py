
import unittest

from src.main import Lead, classify_lead


class TestLeadClassification(unittest.TestCase):
    def test_urgent_sales_lead(self):
        lead = Lead(
            name="Alex",
            message="Urgent: I need a price quote.",
            email="alex@example.com",
        )

        result = classify_lead(lead)

        self.assertEqual(result["category"], "sales")
        self.assertEqual(result["priority"], "high")

    def test_support_request(self):
        lead = Lead(
            name="Sam",
            message="I have a problem with the service.",
        )

        result = classify_lead(lead)

        self.assertEqual(result["category"], "support")
        self.assertEqual(result["priority"], "normal")

    def test_general_question(self):
        lead = Lead(
            name="Taylor",
            message="Tell me about your company.",
        )

        result = classify_lead(lead)

        self.assertEqual(result["category"], "general")
        self.assertEqual(result["priority"], "normal")

    def test_empty_name_is_rejected(self):
        lead = Lead(name="   ", message="I need help.")

        with self.assertRaises(ValueError):
            classify_lead(lead)

    def test_empty_message_is_rejected(self):
        lead = Lead(name="Jordan", message="   ")

        with self.assertRaises(ValueError):
            classify_lead(lead)

    def test_whitespace_is_removed(self):
        lead = Lead(
            name="  Alex  ",
            message="  Tell me about your company.  ",
            email="  alex@example.com  ",
        )

        result = classify_lead(lead)

        self.assertEqual(result["name"], "Alex")
        self.assertEqual(result["message"] if "message" in result else result["summary"],
                         "Tell me about your company.")
        self.assertEqual(result["email"], "alex@example.com")


if __name__ == "__main__":
    unittest.main()
