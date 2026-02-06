import os
import sys
import datetime
import re

# Configuration
DAILY_FILE = 'Daily_Time_Box.md'
HL_BL_FILE = 'HL-BL.md'

def get_date_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]

def add_new_day():
    if not os.path.exists(DAILY_FILE):
        print(f"Error: {DAILY_FILE} not found.")
        return

    now = datetime.datetime.now()
    # Format: 05/Feb
    date_str = now.strftime("%d/%b")
    
    with open(DAILY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for duplicate
    if f"## 📅 [{date_str}]" in content:
        print(f"Entry for {date_str} already exists.")
        return

    # Template for new day
    new_entry = f"""
## 📅 [{date_str}]

| No. | Task | Dependency / POC | Status | Inputs | Steps | Output | ETA | Actual ETA |
| :-: | :--- | :--------------- | :----- | :----- | :---- | :----- | :-: | :--------: |
|  1  |      |                  |        |        |       |        |     |            |
|  2  |      |                  |        |        |       |        |     |            |
|  3  |      |                  |        |        |       |        |     |            |
|     |      |                  |        |        |       |        |     |            |
"""
    
    # Insert after the first header or at the top if no header
    lines = content.splitlines()
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("# "): # Skip title
             continue
        if line.strip().startswith("[➕"): # Skip the button itself
             continue
        if line.strip() == "": # Skip initial empty lines
            continue
        # Found the start of content
        insert_idx = i
        break
    
    # We want to insert it right after the interactive button/title
    # Let's find the header line "## 📅" to insert before, or just append if empty
    
    # Find the "Add Button" line to insert after it
    # We look for the line containing "[➕"
    button_line_idx = -1
    for i, line in enumerate(lines):
        if "[➕" in line:
            button_line_idx = i
            break
            
    if button_line_idx != -1:
        # Insert after the button line (and potentially an empty line)
        insert_idx = button_line_idx + 1
        # Check if next line is empty, if so, insert after that
        if insert_idx < len(lines) and lines[insert_idx].strip() == "":
            insert_idx += 1
            
        new_content = "\n".join(lines[:insert_idx]) + "\n" + new_entry.strip() + "\n\n" + "\n".join(lines[insert_idx:])
    else:
        # Fallback: Prepend if no button found (or insert at top)
        new_content = new_entry.strip() + "\n\n" + content

    with open(DAILY_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Successfully added new entry for {date_str}")

def add_hl_bl_task():
    if not os.path.exists(HL_BL_FILE):
        print(f"Error: {HL_BL_FILE} not found.")
        return

    with open(HL_BL_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the last ID
    last_id = 0
    table_start_idx = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and "---" in line:
            table_start_idx = i
            continue
        
        if table_start_idx != -1 and line.strip().startswith("|"):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 1 and parts[1].isdigit():
                last_id = int(parts[1])

    new_id = last_id + 1
    new_id_str = f"{new_id:02d}" # Pad with zero, e.g., 01, 02

    # Template for new row
    # | ID | Task | Priority | Status | Comment | Link | Dependency | ETA | Teams/Err Review |
    new_row = f"| {new_id_str} | | | | | | | | |\n"

    # Append to the end of the table
    # We need to find the end of the file or the end of the table
    # Assuming the table is at the end of the file for now based on previous file content
    
    # Check if file ends with newline
    if lines and not lines[-1].endswith('\n'):
        lines[-1] += '\n'
        
    lines.append(new_row)

    with open(HL_BL_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"Successfully added new HL-BL task with ID {new_id_str}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python time_box_manager.py [new_day|new_task]")
        sys.exit(1)

    command = sys.argv[1]
    
    # Calculate paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir) # Switch to script dir to find md files

    if command == "new_day":
        add_new_day()
    elif command == "new_task":
        add_hl_bl_task()
    else:
        print(f"Unknown command: {command}")
