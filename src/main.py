
from dataclasses import dataclass


@dataclass
class Lead:
    name: str
    message: str
    email: str = ""


def classify_lead(lead: Lead) -> dict:
    """Classify an incoming customer request using simple rules."""
    message = lead.message.lower()

    urgent_words = ["urgent", "asap", "immediately", "acil", "hemen"]
    sales_words = ["price", "pricing", "quote", "buy", "fiyat", "teklif"]
    support_words = ["error", "broken", "problem", "help", "hata", "sorun"]

    if any(word in message for word in urgent_words):
        priority = "high"
    else:
        priority = "normal"

    if any(word in message for word in support_words):
        category = "support"
    elif any(word in message for word in sales_words):
        category = "sales"
    else:
        category = "general"

    return {
        "name": lead.name,
        "email": lead.email,
        "category": category,
        "priority": priority,
        "summary": lead.message.strip(),
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
