import json
import random

# Define the base companies, email types, and user actions
companies = [
    "MegaCorp",
    "ShopFast", 
    "DealHunter",
    "BargainMart",
    "QuickBuy",
    "SpamCorp",
    "ClickBait Inc",
    "SalesMaster"
]

email_types = [
    "promotional",
    "newsletter", 
    "sale_alert",
    "survey",
    "welcome_email"
]

user_actions = [
    "unsubscribed",
    "marked_spam",
    "ignored", 
    "clicked",
    "unsubscribed"  # Adding extra unsubscribed entries to increase violation chances
]

# Generate 100 random email monitoring entries
email_data = [
    {
        "company": random.choice(companies), 
        "email_type": random.choice(email_types),
        "user_action": random.choice(user_actions)
    }
    for _ in range(100)
]

# Save to a JSON file
output_file = "email_monitor.json"
with open(output_file, "w") as file:
    json.dump(email_data, file, indent=4)

print(f"Generated {len(email_data)} email monitoring entries in {output_file}")