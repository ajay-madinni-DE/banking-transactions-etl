
import sqlite3
from pathlib import Path

project_folder = Path(__file__).parent
database_file = project_folder / "banking.db"

if not database_file.exists():
    raise FileNotFoundError("Banking database not found.")

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

# Create a table to track pipeline executions
cursor.execute("""
CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_name TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    status TEXT NOT NULL,
    records_processed INTEGER DEFAULT 0,
    records_inserted INTEGER DEFAULT 0,
    records_skipped INTEGER DEFAULT 0,
    records_rejected INTEGER DEFAULT 0,
    duration_seconds REAL DEFAULT 0,
    error_message TEXT
)
""")

connection.commit()
connection.close()

print("PIPELINE MONITORING SETUP")
print("-------------------------")
print("Monitoring table created successfully!")
print("Table name: pipeline_runs")
print("Database: banking.db")
