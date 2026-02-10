import pandas as pd
import re
from pathlib import Path

def safe_filename(name: str) -> str:
    """
    Make a string safe to use as a filename:
    - Replace spaces with underscores
    - Remove invalid characters
    """
    name = name.strip()
    name = name.replace(" ", "_")
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name

def main():
    excel_file = r"C:\Users\GRL\Downloads\timesheet.xlsx"   # 🔁 Change this to your Excel file path
    output_dir = Path("output") # 📁 All files will be saved in this folder
    output_dir.mkdir(exist_ok=True)

    print(f"📂 Reading Excel file: {excel_file}")

    # Read ALL sheets
    sheets = pd.read_excel(excel_file, sheet_name=None)

    print(f"📊 Found {len(sheets)} sheets")

    for sheet_name, df in sheets.items():
        safe_name = safe_filename(sheet_name)

        csv_path = output_dir / f"{safe_name}.csv"
        md_path = output_dir / f"{safe_name}.md"

        # Save CSV
        df.to_csv(csv_path, index=False)

        # Save Markdown
        with md_path.open("w", encoding="utf-8") as f:
            f.write(f"# Sheet: {sheet_name}\n\n")
            f.write(df.to_markdown(index=False))

        print(f"✅ Exported: {csv_path} and {md_path}")

    print("🎉 Done! All sheets exported.")

if __name__ == "__main__":
    main()
