# 📊 NiftyDesk — Intelligent NSE Bhavcopy Processor

NiftyDesk is a Python-based automation tool that helps traders, analysts, and researchers **download**, **extract**, and **process** daily market data from the **National Stock Exchange of India (NSE)** with ease.

It extracts and organizes key stock/index data from NSE's `PRddmmyy.csv` bhavcopy into a clean, user-defined format for further analysis or reporting.

this is use Web-Scrapping for fetch data from nse website.

---

## 🚀 Features

- 🔽 Auto-download & extract daily NSE bhavcopy files
- 📅 User input for any valid date in `PRDDMMYY` format
- 🔎 Select custom columns of interest
- 📄 Supports F&O symbol mapping to match NSE securities
- 📁 Appends processed data to monthly **CSV and Excel** output files
- 🧹 Optional cleanup of temporary files
- 💬 Friendly CLI prompts and emoji-powered UX

---
## Screenshots:
<img width="1011" height="443" alt="{DF8E1C46-4F45-4585-A9DB-81AC54A1353F}" src="https://github.com/user-attachments/assets/a1033f46-395f-428e-b6ae-db55b8758c74" />

<img width="1507" height="509" alt="{9CED16CA-BB1B-484E-9689-5245302DE3C3}" src="https://github.com/user-attachments/assets/f52d7a32-5caa-4e1f-a856-37f7d30d1bfb" />


---
## 🎯 Purpose

**NiftyDesk** is built to:
- Save time manually handling NSE bhavcopy data
- Enable consistent formatting across dates for easier analysis
- Allow customized reporting and archival for equities and indices
- Serve as a base for dashboarding or ML applications in finance

---

## 🧰 Requirements

Make sure Python 3.7+ is installed. Then install dependencies:
---
## 🗂️ Folder Structure

```bash
niftydesk/
├── input/
│   ├── my_columns.txt              # User-selected bhavcopy columns
│   └── fno_security_mapping.csv    # Mapping for F&O symbols to NSE securities
├── output/
│   └── YYYY/
│       ├── csv/
│       │   └── MMYY.csv
│       └── excel/
│           └── MMYY.xlsx
├── tmp_data/                       # Temporary unzipped files & metadata
│   └── available_columns.txt       # All columns from the downloaded CSV
├── niftydesk.py                    # Main script
└── README.md
```

## 📝 Required Input Files

| File                          | Purpose                                               |
|------------------------------|-------------------------------------------------------|
| `input/my_columns.txt`       | List of column names to extract from daily data       |
| `input/fno_security_mapping.csv` | Contains index mappings to filter required stocks  |

---

## 💻 Sample Run (Terminal)

```bash
PS E:\Project\PriceFetcher> python final-v1.py  
Enter date code in format PRDDMMYY (e.g., PR250425): PR220725

📥 Downloading ZIP from https://nsearchives.nseindia.com/archives/equities/bhavcopy/pr/PR220725.zip ...
✅ File downloaded and extracted to 'tmp_data/unzipped'
✅ All column names written to 'tmp_data/available_columns.txt'

👉 Please write the desired columns into 'input/my_columns.txt' (one per line).
Have you updated 'input/my_columns.txt' and placed 'input/fno_security_mapping.csv'? (yes/no): yes

✅ Successfully updated monthly files:
 - output\2025\csv\0725.csv
 - output\2025\excel\0725.xlsx

🧹 Do you want to delete 'tmp_data' folder? (yes/no): yes
✅ 'tmp_data' folder deleted.
```

---

## 📆 Smart Time Awareness
Automatically notifies when a new week or new month starts, helping you maintain and manage data schedules more effectively.
---

## 🔮 Future Scope
📅 Auto-fetch and combine monthly data into single sheets

🌐 Build a web interface for easier usability and visualization

📊 Add charts and trendlines for stock movement

🧠 Integrate ML models for price prediction

📦 Scheduled auto-updates via cron jobs or GitHub Actions
