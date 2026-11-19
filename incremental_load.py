
import csv
import sqlite3
from datetime import datetime
from pathlib import Path
import time
from datetime import timezone

# Project locations
project_folder = Path(__file__).parent

source_file = project_folder / "data" / "new_transactions.csv"
database_file = project_folder / "banking.db"
pipeline_start_time = datetime.now(timezone.utc)
pipeline_start_clock = time.perf_counter()
print("INCREMENTAL DATA LOADING")

print("------------------------")

# Check files
if not source_file.exists():
    raise FileNotFoundError("New transactions file not found.")

if not database_file.exists():
    raise FileNotFoundError("Banking database not found.")

# Connect to SQLite
connection = sqlite3.connect(database_file)
cursor = connection.cursor()

# Get existing transaction IDs
cursor.execute("SELECT transaction_id FROM transactions")

existing_ids = {
    row[0] for row in cursor.fetchall()
}

new_records = 0
skipped_records = 0
invalid_records = 0

# Read new transactions
with open(source_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        transaction_id = row["transaction_id"].strip()

        # Validate transaction
        try:
            customer_id = row["customer_id"].strip()
            amount = float(row["amount"])

            datetime.strptime(
                row["transaction_date"], "%Y-%m-%d"
            )

            if (
                not transaction_id
                or not customer_id
                or amount <= 0
                or row["status"] not in
                ("Success", "Failed", "Pending")
                or row["transaction_type"] not in
                ("Deposit", "Withdrawal", "Transfer", "Payment")
            ):
                raise ValueError("Invalid transaction")

        except (ValueError, TypeError, KeyError):
            invalid_records += 1
            continue

        # Skip transactions already loaded
        if transaction_id in existing_ids:
            skipped_records += 1
            continue

        # Insert only new transactions
        cursor.execute("""
            INSERT INTO transactions (
                transaction_id,
                customer_id,
                transaction_date,
                transaction_type,
                amount,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            transaction_id,
            customer_id,
            row["transaction_date"],
            row["transaction_type"],
            amount,
            row["status"]
        ))

        existing_ids.add(transaction_id)
        new_records += 1

# Save changes
connection.commit()

cursor.execute("SELECT COUNT(*) FROM transactions")
total_records = cursor.fetchone()[0]

connection.close()

print(f"New transactions loaded: {new_records}")
print(f"Existing transactions skipped: {skipped_records}")
print(f"Invalid transactions: {invalid_records}")
print(f"Total transactions in database: {total_records}")

print("INCREMENTAL LOAD COMPLETED SUCCESSFULLY!")



# PIPELINE EXECUTION MONITORING

# Record the completed execution
end_time = datetime.now(timezone.utc)
duration_seconds = time.perf_counter() - pipeline_start_clock

monitor_connection = sqlite3.connect(database_file)
monitor_cursor = monitor_connection.cursor()

monitor_cursor.execute("""
    INSERT INTO pipeline_runs (
        pipeline_name,
        start_time,
        end_time,
        status,
        records_processed,
        records_inserted,
        records_skipped,
        records_rejected,
        duration_seconds,
        error_message
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Incremental Banking Load",
    pipeline_start_time.isoformat(),
    end_time.isoformat(),
    "Success",
    new_records + skipped_records + invalid_records,
    new_records,
    skipped_records,
    invalid_records,
    round(duration_seconds, 4),
    None
))

monitor_connection.commit()
monitor_connection.close()

print("Pipeline execution recorded successfully!")
print(f"Execution time: {duration_seconds:.4f} seconds")
