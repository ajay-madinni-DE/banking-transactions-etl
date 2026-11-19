
import shutil
import csv
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).parent

# Source banking transactions
source_file = project_folder / "data" / "bank_transactions.csv"

# Bronze layer destination
bronze_folder = project_folder / "bronze"
bronze_folder.mkdir(exist_ok=True)

bronze_file = bronze_folder / "raw_transactions.csv"

print("BRONZE LAYER PROCESSING")
print("-----------------------")

# Check that source data exists
if not source_file.exists():
    raise FileNotFoundError(
        "Source CSV missing. Run generate_data.py first."
    )

# Copy raw data without modifying it
shutil.copy2(source_file, bronze_file)

# Count raw transactions
with open(bronze_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    total_records = sum(1 for row in reader)

print(f"Raw transactions ingested: {total_records}")
print(f"Bronze file saved to: {bronze_file}")
print("BRONZE LAYER COMPLETED SUCCESSFULLY!")
