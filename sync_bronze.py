
import csv
from pathlib import Path

project_folder = Path(__file__).parent

bronze_file = project_folder / "bronze" / "raw_transactions.csv"
new_file = project_folder / "data" / "new_transactions.csv"

if not bronze_file.exists() or not new_file.exists():
    raise FileNotFoundError("Required transaction files not found.")

# Read existing Bronze transactions
with open(bronze_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames
    transactions = list(reader)

if not fieldnames:
    raise ValueError("Bronze CSV has no column headers.")

# Track existing transaction IDs
existing_ids = {
    row["transaction_id"] for row in transactions
}

new_records = 0
skipped_records = 0

# Read incoming transactions
with open(new_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    if reader.fieldnames != fieldnames:
        raise ValueError("Incoming CSV columns do not match Bronze.")

    for row in reader:
        transaction_id = row["transaction_id"]

        if transaction_id in existing_ids:
            skipped_records += 1
            continue

        transactions.append(row)
        existing_ids.add(transaction_id)
        new_records += 1

# Save updated Bronze dataset
with open(bronze_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(transactions)

print("BRONZE SYNCHRONIZATION")
print("----------------------")
print(f"New transactions added: {new_records}")
print(f"Existing transactions skipped: {skipped_records}")
print(f"Total Bronze transactions: {len(transactions)}")
print("BRONZE SYNCHRONIZATION COMPLETED!")
