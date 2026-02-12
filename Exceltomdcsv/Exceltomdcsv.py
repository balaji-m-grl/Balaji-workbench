import pandas as pd
import re
from pathlib import Path
import logging
import sys

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(
    filename="debug.log",
    filemode="w",  # overwrite each run; use "a" to append
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# -----------------------------
# Helper: make safe filenames
# -----------------------------
def safe_filename(name: str) -> str:
    """
    Make a string safe to use as a filename:
    - Replace spaces with underscores
    - Remove invalid characters
    """
    logging.debug(f"Original sheet name: {name}")

    name = name.strip()
    name = name.replace(" ", "_")
    name = re.sub(r'[\\/*?:"<>|]', "", name)

    logging.debug(f"Safe filename: {name}")
    return name

# -----------------------------
# Main logic
# -----------------------------
def main():
    excel_file = Path(r"D:\Balaji-workbench\exceltomd\input\timesheet.xlsx")  # 🔁 Change if needed
    output_dir = Path("output")

    logging.info("Starting Excel to CSV/MD conversion")
    logging.debug(f"Excel file path: {excel_file}")
    logging.debug(f"Output directory: {output_dir}")

    # ---- Validation: check file exists ----
    if not excel_file.exists():
        logging.error(f"Excel file not found: {excel_file}")
        print(f"❌ Excel file not found: {excel_file}")
        sys.exit(1)

    # ---- Create output directory if needed ----
    try:
        output_dir.mkdir(exist_ok=True)
        logging.debug("Output directory ready")
    except Exception as e:
        logging.exception("Failed to create output directory")
        print("❌ Failed to create output directory. See debug.log")
        sys.exit(1)

    # ---- Read Excel file ----
    try:
        logging.info(f"Reading Excel file: {excel_file}")
        sheets = pd.read_excel(excel_file, sheet_name=None)
    except Exception as e:
        logging.exception("Failed to read Excel file")
        print("❌ Failed to read Excel file. See debug.log for details.")
        sys.exit(1)

    if not sheets:
        logging.warning("No sheets found in the Excel file")
        print("⚠️ No sheets found in the Excel file.")
        return

    logging.info(f"Found {len(sheets)} sheets")

    # ---- Process each sheet ----
    for sheet_name, df in sheets.items():
        logging.info(f"Processing sheet: {sheet_name}")

        safe_name = safe_filename(sheet_name)

        csv_path = output_dir / f"{safe_name}.csv"
        md_path = output_dir / f"{safe_name}.md"

        # ---- Validation: check if sheet is empty ----
        if df.empty:
            logging.warning(f"Sheet '{sheet_name}' is empty. Files will still be created.")
            print(f"⚠️ Sheet '{sheet_name}' is empty.")

        # ---- Save CSV ----
        try:
            df.to_csv(csv_path, index=False)
            logging.debug(f"CSV saved to: {csv_path}")
        except Exception:
            logging.exception(f"Failed to save CSV for sheet: {sheet_name}")
            print(f"❌ Failed to save CSV for sheet: {sheet_name}. See debug.log")
            continue

        # ---- Save Markdown ----
        try:
            with md_path.open("w", encoding="utf-8") as f:
                f.write(f"# Sheet: {sheet_name}\n\n")
                f.write(df.to_markdown(index=False))
            logging.debug(f"Markdown saved to: {md_path}")
        except Exception:
            logging.exception(f"Failed to save Markdown for sheet: {sheet_name}")
            print(f"❌ Failed to save Markdown for sheet: {sheet_name}. See debug.log")
            continue

        logging.info(f"Exported: {csv_path} and {md_path}")
        print(f"✅ Exported: {csv_path} and {md_path}")

    logging.info("All sheets processed")
    print("🎉 Done! All sheets exported.")
    print("📝 Check debug.log for detailed logs.")

# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Unexpected fatal error")
        print("❌ Unexpected error occurred. See debug.log for details.")
