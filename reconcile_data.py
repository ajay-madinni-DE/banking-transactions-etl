
import csv
import sqlite3
from pathlib import Path

project_folder = Path(__file__).parent

database_file = project_folder / "banking.db"
bronze_file = project_folder / "bronze" / "raw_transactions.csv"
silver_file = project_folder / "silver" / "clean_transactions.csv"
gold_file = project_folder / "gold" / "transaction_summary.csv"

print("BANKING DATA RECONCILIATION")
print("---------------------------")

# Count records in CSV files
def count_csv_records(file_path):
    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return sum(1 for _ in csv.DictReader(file))

# Count records in SQLite
with sqlite3.connect(database_file) as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    database_count = cursor.fetchone()[0]

bronze_count = count_csv_records(bronze_file)
silver_count = count_csv_records(silver_file)
gold_count = count_csv_records(gold_file)

print(f"Bronze records: {bronze_count}")
print(f"Silver records: {silver_count}")
print(f"Gold summary rows: {gold_count}")
print(f"SQLite records: {database_count}")

print("\nRECONCILIATION RESULTS")
print("----------------------")

if bronze_count == silver_count == database_count:
    print("PASS: Bronze, Silver and SQLite counts match.")
else:
    print("WARNING: Record counts do not match.")
    print("The pipeline layers need synchronization.")

print(
    "\nNote: Gold contains aggregated summary rows, "
    "so its row count is not expected to match "
    "the transaction-level datasets."
)
