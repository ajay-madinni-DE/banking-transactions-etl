
import csv
from collections import defaultdict
from pathlib import Path

# Project folders
project_folder = Path(__file__).parent

silver_file = (
    project_folder / "silver" / "clean_transactions.csv"
)

gold_folder = project_folder / "gold"
gold_folder.mkdir(exist_ok=True)

gold_file = gold_folder / "transaction_summary.csv"

print("GOLD LAYER PROCESSING")
print("---------------------")

# Read cleaned Silver transactions
with open(silver_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    transactions = list(reader)

# Group transactions by status
summary = defaultdict(
    lambda: {"count": 0, "total_amount": 0.0}
)

for transaction in transactions:
    status = transaction["status"]
    amount = float(transaction["amount"])

    summary[status]["count"] += 1
    summary[status]["total_amount"] += amount

# Save analytics-ready Gold dataset
with open(gold_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "status",
        "transaction_count",
        "total_amount"
    ])

    for status, values in sorted(summary.items()):
        writer.writerow([
            status,
            values["count"],
            f"{values['total_amount']:.2f}"
        ])

print(f"Transactions processed: {len(transactions)}")
print(f"Gold summary saved to: {gold_file}")

print("\nGOLD LAYER SUMMARY")
print("---------------------")

for status, values in sorted(summary.items()):
    print(
        f"{status}: {values['count']} transactions, "
        f"${values['total_amount']:,.2f}"
    )

print("\nGOLD LAYER COMPLETED SUCCESSFULLY!")
