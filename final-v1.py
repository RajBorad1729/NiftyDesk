import pandas as pd
import os
import requests
import zipfile
import io
import shutil
from datetime import datetime

# Step 1: Ask user for date input
date_code = input("Enter date code in format PRDDMMYY (e.g., PR250425): ").strip().upper()
if not date_code.startswith("PR") or len(date_code) != 8 or not date_code[2:].isdigit():
    print("❌ Invalid format. Please enter like PR250425.")
    exit()

# Detect date details
day = int(date_code[2:4])
month = int(date_code[4:6])
year_suffix = int(date_code[6:])
year_full = 2000 + year_suffix if year_suffix <= 99 else 1900 + year_suffix

input_date = datetime(year_full, month, day)
is_friday = input_date.weekday() == 4  # Monday=0, Friday=4

# Show Friday message
if is_friday:
    print("\n────────────────────────────────────────")
    print("🌟 A New Week is Coming! 🌟")
    print("Recharge, Refocus, and get ready to achieve more!")
    print("────────────────────────────────────────\n")

csv_filename = f"{date_code}.csv"
zip_url = f"https://nsearchives.nseindia.com/archives/equities/bhavcopy/pr/{date_code}.zip"

# Step 2: Download and unzip
print(f"📥 Downloading ZIP from {zip_url} ...")
try:
    response = requests.get(zip_url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        os.makedirs("tmp_data/unzipped", exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall("tmp_data/unzipped")
        print("✅ File downloaded and extracted to 'tmp_data/unzipped'")
    else:
        print("❌ ZIP not found or not available for the entered date.")
        exit()
except Exception as e:
    print(f"❌ Error downloading ZIP: {e}")
    exit()

# Step 3: Load CSV
csv_path = os.path.join("tmp_data/unzipped", csv_filename)
if not os.path.exists(csv_path):
    print(f"❌ Could not find extracted CSV at: {csv_path}")
    exit()

try:
    bhav_df = pd.read_csv(
        csv_path,
        engine="python",
        skip_blank_lines=True,
        skipinitialspace=True,
        on_bad_lines='skip'
    )
except Exception as e:
    print(f"❌ Error reading CSV: {e}")
    exit()

# Step 4: Write all columns to tmp_data/available_columns.txt
all_columns = bhav_df.columns.tolist()
os.makedirs("input", exist_ok=True)
with open("tmp_data/available_columns.txt", "w", encoding="utf-8") as f:
    for col in all_columns:
        f.write(col + "\n")

print("✅ All column names written to 'tmp_data/available_columns.txt'")
print("👉 Please write the desired columns into 'input/my_columns.txt' (one per line).")

proceed = input("Have you updated 'input/my_columns.txt' and placed 'input/fno_security_mapping.csv'? (yes/no): ").strip().lower()
if proceed != "yes":
    print("❌ Process terminated by user.")
    exit()

# Step 5: Read user's selected columns
try:
    with open("input/my_columns.txt", "r", encoding="utf-8") as f:
        selected_columns = [line.strip() for line in f if line.strip()]
except Exception:
    print("❌ Could not read 'input/my_columns.txt'.")
    exit()

# Step 6: Read corrected fno_security_mapping.csv
try:
    fno_mapping = pd.read_csv("input/fno_security_mapping.csv")
except Exception:
    print("❌ Could not read 'input/fno_security_mapping.csv'.")
    exit()

# Step 7: Prepare final data
final_records = []
date_ddmmyy = f"{date_code[2:4]}/{date_code[4:6]}/{date_code[6:]}"  # e.g., 25/04/25

# Find index where indexes start (after stocks)
index_start_idx = fno_mapping[fno_mapping['Symbol'].str.upper() == "NIFTY"].index
if len(index_start_idx) > 0:
    index_start_idx = index_start_idx[0]
else:
    index_start_idx = len(fno_mapping)  # If NIFTY not found, treat all as stocks

# Stocks part
for idx, row in fno_mapping.iloc[:index_start_idx].iterrows():
    symbol = row['Symbol']
    stock_name = row['Stock Name']
    matched_security = row['Matched SECURITY']

    bhav_row = bhav_df[bhav_df['SECURITY'].str.strip().str.upper() == matched_security.strip().upper()]

    if not bhav_row.empty:
        bhav_row = bhav_row.iloc[0]
        record = {
            "DATE": date_ddmmyy,
            "Symbol": symbol,
            "Stock Name": stock_name
        }
        for col in selected_columns:
            record[col] = bhav_row.get(col, "")
    else:
        record = {
            "DATE": date_ddmmyy,
            "Symbol": symbol,
            "Stock Name": stock_name,
        }
        for col in selected_columns:
            record[col] = ""

    final_records.append(record)

# Insert separator between stocks and indexes
if index_start_idx < len(fno_mapping):
    sep_arrow = {col: "🔽🔽🔽" for col in ["DATE", "Symbol", "Stock Name"] + selected_columns}
    final_records.append(sep_arrow)

# Indexes part
for idx, row in fno_mapping.iloc[index_start_idx:].iterrows():
    symbol = row['Symbol']
    stock_name = row['Stock Name']
    matched_security = row['Matched SECURITY']

    bhav_row = bhav_df[bhav_df['SECURITY'].str.strip().str.upper() == matched_security.strip().upper()]

    if not bhav_row.empty:
        bhav_row = bhav_row.iloc[0]
        record = {
            "DATE": date_ddmmyy,
            "Symbol": symbol,
            "Stock Name": stock_name
        }
        for col in selected_columns:
            record[col] = bhav_row.get(col, "")
    else:
        record = {
            "DATE": date_ddmmyy,
            "Symbol": symbol,
            "Stock Name": stock_name,
        }
        for col in selected_columns:
            record[col] = ""

    final_records.append(record)

# Step 8: Prepare paths
base_output_dir = os.path.join("output", str(year_full))
csv_output_dir = os.path.join(base_output_dir, "csv")
excel_output_dir = os.path.join(base_output_dir, "excel")

os.makedirs(csv_output_dir, exist_ok=True)
os.makedirs(excel_output_dir, exist_ok=True)

month_code = f"{date_code[4:6]}{date_code[6:]}"  # MMYY
csv_file_path = os.path.join(csv_output_dir, f"{month_code}.csv")
excel_file_path = os.path.join(excel_output_dir, f"{month_code}.xlsx")

# Step 9: Load existing monthly file if exists
try:
    existing_df = pd.read_csv(csv_file_path)
except:
    existing_df = pd.DataFrame()

# Step 10: Merge with new daily data
final_df = pd.DataFrame(final_records)

# Prepare 3 rows separator
separator = pd.DataFrame([["" for _ in final_df.columns], 
                          ["✨🌟🔅" for _ in final_df.columns], 
                          ["" for _ in final_df.columns]],
                          columns=final_df.columns)

# Append to existing
combined_df = pd.concat([existing_df, separator, final_df], ignore_index=True)

# Save updated files
combined_df.to_csv(csv_file_path, index=False)

# For Excel
try:
    existing_excel_df = pd.read_excel(excel_file_path)
except:
    existing_excel_df = pd.DataFrame()

combined_excel_df = pd.concat([existing_excel_df, separator, final_df], ignore_index=True)
combined_excel_df.to_excel(excel_file_path, index=False)

print(f"\n✅ Successfully updated monthly files:\n - {csv_file_path}\n - {excel_file_path}")

# Step 11: Ask user if they want to delete tmp_data
cleanup = input("🧹 Do you want to delete 'tmp_data' folder? (yes/no): ").strip().lower()
if cleanup == "yes":
    try:
        shutil.rmtree("tmp_data")
        print("✅ 'tmp_data' folder deleted.")
    except Exception as e:
        print(f"⚠️ Could not delete 'tmp_data': {e}")
else:
    print("ℹ️ 'tmp_data' folder retained.")
