
import sqlite3
from pathlib import Path

# Connect to our banking database
project_folder = Path(__file__).parent
database_file = project_folder / "banking.db"

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

print("BANKING TRANSACTION ANALYTICS")
print("-----------------------------")

# SQL query: Count transactions by status
cursor.execute("""
SELECT
    status,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_amount
FROM transactions
GROUP BY status
ORDER BY total_transactions DESC
""")

results = cursor.fetchall()

# Display SQL results
for row in results:
    status, count, amount = row

    print(f"\nStatus: {status}")
    print(f"Transactions: {count}")
    print(f"Total Amount: ${amount:,.2f}")

connection.close()

print("\nAnalytics completed successfully!")
