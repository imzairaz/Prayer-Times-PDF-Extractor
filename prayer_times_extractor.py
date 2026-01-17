import PyPDF2
import pandas as pd
import re
import sys
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def parse_prayer_times(text):
    """Parse prayer times from extracted text"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Find the header row
    header_index = -1
    for i, line in enumerate(lines):
        if 'DATE' in line and 'FAJR' in line and 'SUNRISE' in line:
            header_index = i
            break

    if header_index == -1:
        print("Could not find prayer times table in PDF")
        return None

    # Extract data rows
    prayer_data = []

    for i in range(header_index + 1, len(lines)):
        line = lines[i]

        # Stop at footer content
        if any(keyword in line for keyword in [
            'Prayer Time Differences', 'Height in', 'Stories',
            'ACJU', 'Note:', 'Fwpg;G:', 'www.', '@'
        ]):
            break

        # Match date pattern like "1-Jun" or "30-Jun"
        date_match = re.match(r'^\d{1,2}-[A-Za-z]{3}', line)
        if not date_match:
            continue

        # Split the line by whitespace
        parts = line.split()

        # Need at least 13 parts (date + 6 times with AM/PM)
        if len(parts) >= 13:
            try:
                prayer_data.append({
                    'DATE': parts[0],
                    'FAJR': f"{parts[1]} {parts[2]}",
                    'SUNRISE': f"{parts[3]} {parts[4]}",
                    'LUHR': f"{parts[5]} {parts[6]}",
                    'ASR': f"{parts[7]} {parts[8]}",
                    'MAGRIB': f"{parts[9]} {parts[10]}",
                    'ISHA': f"{parts[11]} {parts[12]}"
                })
            except IndexError:
                continue

    return prayer_data

def export_to_excel(data, output_path):
    """Export prayer times to Excel file"""
    try:
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"  ✅ Successfully exported to: {output_path}")
        print(f"  📊 Total rows: {len(data)}")
        return True
    except Exception as e:
        print(f"  ❌ Error exporting to Excel: {e}")
        return False

def export_to_csv(data, output_path):
    """Export prayer times to CSV file"""
    try:
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        print(f"  ✅ Successfully exported to: {output_path}")
        print(f"  📊 Total rows: {len(data)}")
        return True
    except Exception as e:
        print(f"  ❌ Error exporting to CSV: {e}")
        return False

def list_pdf_files():
    """List all PDF files in current directory"""
    current_dir = Path.cwd()
    pdf_files = list(current_dir.glob("*.pdf"))
    return sorted(pdf_files)

def process_single_pdf(pdf_path, export_format):
    """Process a single PDF file"""
    print(f"\n{'='*80}")
    print(f"📄 Processing: {pdf_path.name}")
    print('='*80)

    # Extract text from PDF
    print("📖 Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)

    if not text:
        print("❌ Failed to extract text from PDF")
        return False

    # Parse prayer times
    print("🔍 Parsing prayer times...")
    prayer_data = parse_prayer_times(text)

    if not prayer_data:
        print("❌ No prayer times found in PDF")
        return False

    print(f"✅ Found {len(prayer_data)} days of prayer times")

    # Show preview
    print("\n📋 Preview (first 3 rows):")
    print("-" * 80)
    df_preview = pd.DataFrame(prayer_data[:3])
    print(df_preview.to_string(index=False))
    print("-" * 80)

    # Generate output filename
    pdf_name = pdf_path.stem

    # Export based on format
    success = False
    if export_format in ['1', '3']:
        excel_output = f"{pdf_name}_Prayer_Times.xlsx"
        success = export_to_excel(prayer_data, excel_output)

    if export_format in ['2', '3']:
        csv_output = f"{pdf_name}_Prayer_Times.csv"
        success = export_to_csv(prayer_data, csv_output) or success

    return success

def main():
    print("=" * 80)
    print(" " * 25 + "Prayer Times PDF to Excel Converter")
    print("=" * 80)

    # List PDF files in current directory
    pdf_files = list_pdf_files()

    # --- CHANGED SECTION START ---
    # Instead of quitting, we just notify the user and continue
    if not pdf_files:
        print("\n⚠️  No PDF files found in the current directory.")
        print("   (Don't worry, you can enter the full file path below manually)")
    else:
        print(f"\n📁 Found {len(pdf_files)} PDF file(s) in current directory:\n")
        # Display numbered list of PDFs
        for idx, pdf in enumerate(pdf_files, 1):
            file_size = pdf.stat().st_size / 1024  # Size in KB
            print(f"  {idx}. {pdf.name} ({file_size:.1f} KB)")
    # --- CHANGED SECTION END ---

    print("\n" + "-" * 80)

    # Get user selection
    print("\n📌 Select files to process:")
    if pdf_files:
        print("  • Enter a single number (e.g., 1)")
        print("  • Enter multiple numbers separated by comma (e.g., 1,2,3)")
        print("  • Enter 'all' or 'a' to process all files")
    print("  • Enter a file path (e.g., C:/Documents/prayer.pdf)")
    print("  • Enter 'q' to quit")

    selection = input("\nYour choice: ").strip()

    if selection.lower() in ['q', 'quit', 'exit']:
        print("👋 Goodbye!")
        return

    # Parse selection
    selected_files = []

    # 1. Check if it's a direct file path (The "Inbuilt" or Manual path)
    # We check this FIRST to allow manual paths to work even if the list is empty
    possible_path = Path(selection.strip().strip('"').strip("'"))

    # Check if the user entered a path that looks like a file
    if possible_path.suffix.lower() == '.pdf' or '/' in selection or '\\' in selection:
        if not possible_path.exists():
            print(f"❌ File not found: {possible_path}")
            print("   Make sure the path is correct and use forward slashes (/) if possible.")
            return

        selected_files = [possible_path]
        print(f"\n✅ Selected file from path: {possible_path.name}")

    # 2. Check if it's a number selection (Only works if we found files automatically)
    elif pdf_files:
        if selection.lower() in ['all', 'a']:
            selected_files = pdf_files
        else:
            try:
                numbers = [int(x.strip()) for x in selection.split(',')]
                # Filter valid numbers
                valid_indices = [n - 1 for n in numbers if 1 <= n <= len(pdf_files)]
                if not valid_indices:
                    print("❌ Invalid number selection!")
                    return
                selected_files = [pdf_files[i] for i in valid_indices]
            except ValueError:
                print("❌ Invalid input! Please enter a valid path or number.")
                return
    else:
        # No files found automatically AND user didn't enter a valid path
        print("❌ No files found locally and invalid path entered.")
        return

    print(f"\n✅ Selected {len(selected_files)} file(s) to process")

    # Get export format
    print("\n📦 Choose export format:")
    print("  1. Excel (.xlsx)")
    print("  2. CSV (.csv)")
    print("  3. Both")

    export_format = input("\nEnter choice (1/2/3) [default: 1]: ").strip() or "1"

    if export_format not in ['1', '2', '3']:
        print("❌ Invalid choice! Using Excel format.")
        export_format = '1'

    # Process selected files
    print("\n" + "=" * 80)
    print("🚀 Starting processing...")
    print("=" * 80)

    success_count = 0
    fail_count = 0

    for pdf_path in selected_files:
        if process_single_pdf(pdf_path, export_format):
            success_count += 1
        else:
            fail_count += 1

    # Summary
    print("\n" + "=" * 80)
    print("📊 PROCESSING SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully processed: {success_count} file(s)")
    if fail_count > 0:
        print(f"❌ Failed: {fail_count} file(s)")
    print("\n✨ Done!")

if __name__ == "__main__":
    main()
