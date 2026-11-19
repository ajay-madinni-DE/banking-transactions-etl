
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Make our random data reproducible
random.seed(42)

# Locate the data folder
data_folder = Path(__file__).parent / "data"
data_folder.mkdir(exist_ok=True)

# Banking transaction categories
transaction_types = ["Deposit", "Withdrawal", "Transfer", "Payment"]
statuses = ["Success", "Failed", "Pending"]

# Generate 10,000 simulated transactions
transactions = []

for i in range(1, 10001):
    transaction = {
        "transaction_id": f"TXN{i:06d}",
        "customer_id": f"CUST{random.randint(1, 500):04d}",
        "transaction_date": (
            datetime(2026, 1, 1)
            + timedelta(days=random.randint(0, 300))
        ).strftime("%Y-%m-%d"),
        "transaction_type": random.choice(transaction_types),
        "amount": round(random.uniform(10, 10000), 2),
        "status": random.choice(statuses),
    }

    transactions.append(transaction)

# Save the transactions to a CSV file
output_file = data_folder / "bank_transactions.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=transactions[0].keys()
    )
    writer.writeheader()
    writer.writerows(transactions)

print("Successfully generated 10,000 banking transactions!")
print(f"File saved to: {output_file}")
