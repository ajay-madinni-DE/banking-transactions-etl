
import csv
from pathlib import Path

# Find our banking CSV file
project_folder = Path(__file__).parent
input_file = project_folder / "data" / "bank_transactions.csv"

# EXTRACT: Read banking transactions
with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    transactions = list(reader)

# Display extraction results
print("ETL Pipeline Started")
print("--------------------")
print(f"Total transactions extracted: {len(transactions)}")

# Display the first transaction
print("\nFirst transaction:")
print(transactions[0])



# TRANSFORM: Validate banking transactions

valid_transactions = []
invalid_transactions = []
seen_ids = set()

for transaction in transactions:
    transaction_id = transaction["transaction_id"]
    customer_id = transaction["customer_id"]

    try:
        amount = float(transaction["amount"])
    except (ValueError, TypeError):
        invalid_transactions.append(transaction)
        continue

    # Check for invalid or duplicate records
    if (
        not transaction_id
        or not customer_id
        or amount <= 0
        or transaction_id in seen_ids
    ):
        invalid_transactions.append(transaction)
        continue

    # Convert amount from text to number
    transaction["amount"] = round(amount, 2)

    seen_ids.add(transaction_id)
    valid_transactions.append(transaction)

print("\nTRANSFORM Results")
print("--------------------")
print(f"Valid transactions: {len(valid_transactions)}")
print(f"Invalid transactions: {len(invalid_transactions)}")



# LOAD: Save validated transactions into SQLite

import sqlite3

# Create or connect to the database
database_file = project_folder / "banking.db"
connection = sqlite3.connect(database_file)

cursor = connection.cursor()

# Create a transactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    transaction_date TEXT,
    transaction_type TEXT,
    amount REAL,
    status TEXT
)
""")

# Load validated transactions
for transaction in valid_transactions:
    cursor.execute("""
    INSERT OR REPLACE INTO transactions
    (transaction_id, customer_id, transaction_date,
     transaction_type, amount, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        transaction["transaction_id"],
        transaction["customer_id"],
        transaction["transaction_date"],
        transaction["transaction_type"],
        transaction["amount"],
        transaction["status"]
    ))

# Save changes
connection.commit()

# Count records stored in the database
cursor.execute("SELECT COUNT(*) FROM transactions")
total_records = cursor.fetchone()[0]

print("\nLOAD Results")
print("--------------------")
print(f"Transactions loaded into database: {total_records}")
print(f"Database saved to: {database_file}")

connection.close()
