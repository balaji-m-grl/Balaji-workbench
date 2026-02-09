import pandas as pd
import os
from pathlib import Path

def convert_excel_to_formats(excel_path, output_dir=None):
    excel_path = Path(excel_path)
    if not excel_path.exists():
        print(f"Error: File {excel_path} not found.")
        return

    if output_dir is None:
        output_dir = excel_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # Load Excel
    try:
        df = pd.read_excel(excel_path)
        
        # Define output paths
        base_name = excel_path.stem
        csv_path = output_dir / f"{base_name}.csv"
        md_path = output_dir / f"{base_name}.md"

        # Save as CSV
        df.to_csv(csv_path, index=False)
        print(f"Successfully saved CSV to: {csv_path}")

        # Save as Markdown
        md_content = df.to_markdown(index=False)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Successfully saved Markdown to: {md_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Create a sample Excel file for testing
    data = {\
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'London', 'Paris']
    }
    df_sample = pd.DataFrame(data)
    df_sample.to_excel('sample.xlsx', index=False)
    print("Created sample.xlsx for testing.")
    
    # Run conversion
    convert_excel_to_formats('sample.xlsx')
