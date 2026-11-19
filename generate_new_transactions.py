
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

project_folder = Path(__file__).parent
output_file = project_folder / "data" / "new_transactions.csv"

random.seed(42)

transaction_types = [
    "Deposit", "Withdrawal", "Transfer", "Payment"
]
statuses = ["Success", "Failed", "Pending"]

fieldnames = [
    "transaction_id",
    "customer_id",
    "transaction_date",
    "transaction_type",
    "amount",
    "status"
]

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(10001, 10501):
        writer.writerow({
            "transaction_id": f"TXN{i:06d}",
            "customer_id": f"CUST{random.randint(1, 500):04d}",
            "transaction_date": (
                datetime(2026, 11, 1)
                + timedelta(days=random.randint(0, 18))
            ).strftime("%Y-%m-%d"),
            "transaction_type": random.choice(transaction_types),
            "amount": round(random.uniform(10, 10000), 2),
            "status": random.choice(statuses)
        })

print("Generated 500 new banking transactions!")
print(f"Saved to: {output_file}")
