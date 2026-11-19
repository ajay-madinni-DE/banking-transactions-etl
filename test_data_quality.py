
import sqlite3
from pathlib import Path

# Connect to the banking database
project_folder = Path(__file__).parent
database_file = project_folder / "banking.db"

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

print("BANKING DATA QUALITY TESTS")
print("--------------------------")

# Test 1: Check total transactions
cursor.execute("SELECT COUNT(*) FROM transactions")
total = cursor.fetchone()[0]

assert total == 10000, "Transaction count is incorrect"
print("PASS: Transaction count is 10,000")

# Test 2: Check for missing customer IDs
cursor.execute("""
SELECT COUNT(*) FROM transactions
WHERE customer_id IS NULL OR TRIM(customer_id) = ''
""")

missing_customers = cursor.fetchone()[0]

assert missing_customers == 0, "Missing customer IDs found"
print("PASS: No missing customer IDs")

# Test 3: Check invalid amounts
cursor.execute("""
SELECT COUNT(*) FROM transactions
WHERE amount IS NULL OR amount <= 0
""")

invalid_amounts = cursor.fetchone()[0]

assert invalid_amounts == 0, "Invalid amounts found"
print("PASS: All transaction amounts are positive")

# Test 4: Check duplicate transaction IDs
cursor.execute("""
SELECT COUNT(*) FROM (
    SELECT transaction_id
    FROM transactions
    GROUP BY transaction_id
    HAVING COUNT(*) > 1
)
""")

duplicates = cursor.fetchone()[0]

assert duplicates == 0, "Duplicate transaction IDs found"
print("PASS: No duplicate transaction IDs")

# Test 5: Check transaction statuses
cursor.execute("""
SELECT COUNT(*) FROM transactions
WHERE status IS NULL
   OR status NOT IN ('Success', 'Failed', 'Pending')
""")

invalid_statuses = cursor.fetchone()[0]

assert invalid_statuses == 0, "Invalid transaction statuses found"
print("PASS: All transaction statuses are valid")

connection.close()

print("\nALL 5 DATA QUALITY TESTS PASSED!")
