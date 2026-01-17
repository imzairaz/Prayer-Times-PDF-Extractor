# 🕌 Prayer Times PDF Extractor

A Python utility designed to automatically extract prayer time schedules from PDF documents and convert them into structured Excel (`.xlsx`) or CSV formats.

## 🎯 Features

* **Precise Extraction:** Captures the exact table format: `DATE`, `FAJR`, `SUNRISE`, `LUHR`, `ASR`, `MAGRIB`, `ISHA`.
* **Smart Formatting:** Preserves date formats (e.g., `1-Jun`) and time formats (e.g., `4:21 AM`).
* **Flexible Export:** Options to save as Excel (`.xlsx`), CSV (`.csv`), or both.
* **User Friendly:** Includes a data preview in the terminal before exporting.
* **Auto-Naming:** Automatically generates output filenames based on the input PDF name.

---

## 📦 Installation

### 1. Prerequisites
Ensure you have Python installed. You will need to install the following dependencies:

```bash
pip install PyPDF2 pandas openpyxl

```

### 2. Setup

Save your python script as:
`prayer_times_extractor.py`

---

## 🚀 Usage

You can run the script in two ways:

### Option A: Command Line Argument

Pass the PDF filename directly when running the script.

```bash
python prayer_times_extractor.py June.pdf

```

### Option B: Interactive Mode

Run the script without arguments, and it will prompt you for the file path.

```bash
python prayer_times_extractor.py
# System will prompt: Enter the PDF path:

```

---

## 📝 Example Output

When you run the script, you will see a preview of the data and a prompt to choose your export format:

```text
$ python prayer_times_extractor.py 1768484286670_June.pdf

Processing: 1768484286670_June.pdf
Extracting text from PDF...
Parsing prayer times...
Found 30 days of prayer times

Preview (first 5 rows):
DATE      FAJR       SUNRISE    LUHR         ASR         MAGRIB      ISHA
1-Jun     4:21 AM    5:46 AM    12:05 PM     3:31 PM     6:24 PM     7:39 PM
2-Jun     4:21 AM    5:46 AM    12:05 PM     3:31 PM     6:24 PM     7:40 PM
...

Choose export format:
1. Excel (.xlsx)
2. CSV (.csv)
3. Both
Enter choice: 1

✅ Successfully exported to: June_Prayer_Times.xlsx
📊 Total rows: 30

```

---

## 📂 Project Structure

Your directory should look like this for the script to work best:

```text
/project-folder
│
├── prayer_times_extractor.py    # The script
├── June.pdf                     # Your source PDF
└── June_Prayer_Times.xlsx       # The generated output

```

## ⚠️ Requirements

* **Python 3.6+**
* **Libraries:** `PyPDF2`, `pandas`, `openpyxl`
