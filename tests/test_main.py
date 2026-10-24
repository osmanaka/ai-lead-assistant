
import json
import tempfile
import unittest
from pathlib import Path

from src.main import Lead, classify_lead, process_leads


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
        lead = Lead(name="Sam", message="I have a problem with the service.")
        result = classify_lead(lead)

        self.assertEqual(result["category"], "support")
        self.assertEqual(result["priority"], "normal")

    def test_general_question(self):
        lead = Lead(name="Taylor", message="Tell me about your company.")
        result = classify_lead(lead)

        self.assertEqual(result["category"], "general")
        self.assertEqual(result["priority"], "normal")

    def test_empty_name_is_rejected(self):
        with self.assertRaises(ValueError):
            classify_lead(Lead(name="   ", message="I need help."))

    def test_empty_message_is_rejected(self):
        with self.assertRaises(ValueError):
            classify_lead(Lead(name="Jordan", message="   "))

    def test_whitespace_is_removed(self):
        lead = Lead(
            name="  Alex  ",
            message="  Tell me about your company.  ",
            email="  alex@example.com  ",
        )
        result = classify_lead(lead)

        self.assertEqual(result["name"], "Alex")
        self.assertEqual(result["summary"], "Tell me about your company.")
        self.assertEqual(result["email"], "alex@example.com")

    def test_process_leads_writes_json_results(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "leads.json"
            output_path = Path(temp_dir) / "output" / "results.json"

            input_path.write_text(
                json.dumps([
                    {
                        "name": "Alex",
                        "email": "alex@example.com",
                        "message": "Urgent price quote needed.",
                    }
                ]),
                encoding="utf-8",
            )

            count = process_leads(input_path, output_path)

            self.assertEqual(count, 1)
            self.assertTrue(output_path.exists())

            results = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(results[0]["category"], "sales")
            self.assertEqual(results[0]["priority"], "high")

    def test_non_list_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "leads.json"
            output_path = Path(temp_dir) / "results.json"
            input_path.write_text('{"name": "Alex"}', encoding="utf-8")

            with self.assertRaises(ValueError):
                process_leads(input_path, output_path)


if __name__ == "__main__":
    unittest.main()
