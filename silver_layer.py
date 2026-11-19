
import csv
from datetime import datetime
from pathlib import Path

# Project locations
project_folder = Path(__file__).parent
bronze_file = project_folder / "bronze" / "raw_transactions.csv"

silver_folder = project_folder / "silver"
silver_folder.mkdir(exist_ok=True)

silver_file = silver_folder / "clean_transactions.csv"
rejected_file = silver_folder / "rejected_transactions.csv"

print("SILVER LAYER PROCESSING")
print("-----------------------")

valid_transactions = []
rejected_transactions = []
seen_ids = set()

# Read Bronze data
with open(bronze_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames

    for row in reader:
        transaction_id = row["transaction_id"].strip()
        customer_id = row["customer_id"].strip()
        status = row["status"].strip()

        try:
            amount = float(row["amount"])
            datetime.strptime(
                row["transaction_date"], "%Y-%m-%d"
            )

            if (
                not transaction_id
                or not customer_id
                or amount <= 0
                or transaction_id in seen_ids
                or status not in ("Success", "Failed", "Pending")
            ):
                raise ValueError("Invalid transaction")

            row["amount"] = f"{amount:.2f}"
            seen_ids.add(transaction_id)
            valid_transactions.append(row)

        except (ValueError, TypeError):
            rejected_transactions.append(row)

# Save clean transactions
with open(silver_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(valid_transactions)

# Save rejected transactions
with open(rejected_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rejected_transactions)

print(f"Valid transactions: {len(valid_transactions)}")
print(f"Rejected transactions: {len(rejected_transactions)}")
print(f"Silver file saved to: {silver_file}")
print("SILVER LAYER COMPLETED SUCCESSFULLY!")
