
from dataclasses import dataclass


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


def main():
    sample = Lead(
        name="Alex Morgan",
        email="alex@example.com",
        message="Urgent: I need a price quote for your automation service.",
    )

    result = classify_lead(sample)

    print("AI Lead Assistant")
    print("-" * 30)

    for key, value in result.items():
        print(f"{key.title()}: {value}")


if __name__ == "__main__":
    main()
