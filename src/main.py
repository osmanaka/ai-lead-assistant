import argparse
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Lead:
    name: str
    message: str
    email: str = ""


def classify_lead(lead: Lead) -> dict:
    """Classify and validate an incoming customer request."""
    name = lead.name.strip()
    message = lead.message.strip()
    email = lead.email.strip()

    if not name:
        raise ValueError("Lead name cannot be empty.")

    if not message:
        raise ValueError("Lead message cannot be empty.")

    message_lower = message.lower()

    urgent_words = ["urgent", "asap", "immediately", "acil", "hemen"]
    sales_words = ["price", "pricing", "quote", "buy", "fiyat", "teklif"]
    support_words = ["error", "broken", "problem", "help", "hata", "sorun"]

    if any(word in message_lower for word in urgent_words):
        priority = "high"
    else:
        priority = "normal"

    if any(word in message_lower for word in support_words):
        category = "support"
    elif any(word in message_lower for word in sales_words):
        category = "sales"
    else:
        category = "general"

    return {
        "name": name,
        "email": email,
        "category": category,
        "priority": priority,
        "summary": message,
    }


def process_leads(input_path: Path, output_path: Path) -> int:
    """Read leads from JSON, classify them, and write results to JSON."""
    with input_path.open("r", encoding="utf-8") as file:
        leads_data = json.load(file)

    if not isinstance(leads_data, list):
        raise ValueError("Input JSON must contain a list of leads.")

    results = []

    for index, item in enumerate(leads_data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Lead #{index} must be a JSON object.")

        name = item.get("name", "")
        message = item.get("message", "")
        email = item.get("email", "")

        if not all(isinstance(value, str) for value in (name, message, email)):
            raise ValueError(f"Lead #{index}: name, message, and email must be strings.")

        lead = Lead(name=name, message=message, email=email)
        results.append(classify_lead(lead))

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    return len(results)



def main():
    project_root = Path(__file__).resolve().parent.parent

    parser = argparse.ArgumentParser(
        description="Classify customer leads from a JSON file."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=project_root / "examples" / "leads.json",
        help="Path to the input JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "examples" / "results.json",
        help="Path to save the classified results.",
    )
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    try:
        count = process_leads(input_path, output_path)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Error processing leads: {error}")
        raise SystemExit(1) from error

    print("AI Lead Assistant")
    print("-" * 30)
    print(f"Processed {count} leads.")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
