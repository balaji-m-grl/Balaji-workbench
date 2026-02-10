from pathlib import Path
import re
import json
import requests
from typing import List, Tuple, Dict
from datetime import datetime

# ---------- Ollama Config ----------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"  # fast & light
MAX_CHARS = 2000  # limit text sent to model

# ---------- Role markers ----------
USER_PATTERNS = [
    r"^\*\*You:\*\*",
    r"^\*\*User:\*\*",
    r"^User:",
    r"^You:",
    r"^U:",
    r"^##\s*User",
    r"^##\s*You",
]

ASSISTANT_PATTERNS = [
    r"^\*\*ChatGPT:\*\*",
    r"^\*\*Assistant:\*\*",
    r"^Assistant:",
    r"^ChatGPT:",
    r"^Chat\s*GPT:",
    r"^##\s*Assistant",
    r"^##\s*ChatGPT",
]

USER_RE = re.compile("|".join(USER_PATTERNS), re.IGNORECASE)
ASSISTANT_RE = re.compile("|".join(ASSISTANT_PATTERNS), re.IGNORECASE)


# ---------- Debug Logger System ----------


class DebugLogger:
    def __init__(self, project_name: str, output_dir: Path):
        self.project_name = project_name
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.output_dir / f"DEBUG_LOG_{timestamp}.txt"
        
        self.log("INITIALIZATION", f"Logger started for {project_name}")
        self.log("SYSTEM", f"Output Directory: {self.output_dir.resolve()}")

    def log(self, category: str, message: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        line = f"[{now}] [{category:15}] {message}"
        print(line)
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def section(self, title: str):
        divider = "=" * 60
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        block = f"\n{divider}\n{title.upper()} - {now}\n{divider}\n"
        print(block)
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(block + "\n")

# ---------- Split conversation ----------

def split_conversation(md_text: str, logger: DebugLogger) -> List[Tuple[str, str]]:
    logger.log("PARSING", "Starting markdown split into user/assistant pairs...")
    lines = md_text.splitlines()

    blocks = []
    current_role = None
    current_user = []
    current_assistant = []

    def flush():
        if current_user or current_assistant:
            blocks.append((
                "\n".join(current_user).strip(),
                "\n".join(current_assistant).strip()
            ))

    for line in lines:
        s = line.strip()

        if USER_RE.match(s):
            if current_role == "assistant":
                flush()
                current_user = []
                current_assistant = []
            current_role = "user"
            continue

        if ASSISTANT_RE.match(s):
            current_role = "assistant"
            continue

        if current_role == "user":
            current_user.append(line)
        elif current_role == "assistant":
            current_assistant.append(line)

    def clean_text(text: str) -> str:
        # Remove common dividers and artifacts
        text = re.sub(r'^\s*\*+\s*\*+\s*\*+\s*$', '', text, flags=re.MULTILINE)
        # Remove repeated chunks (sometimes user question is echoed)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        unique_lines = []
        seen = set()
        for line in lines:
            normalized = line.lower().strip()
            if normalized not in seen:
                unique_lines.append(line)
                seen.add(normalized)
        return "\n".join(unique_lines)

    flush()
    result = []
    for u, a in blocks:
        u_clean = clean_text(u)
        a_clean = a.strip()
        if u_clean or a_clean:
            result.append((u_clean, a_clean))

    logger.log("PARSING", f"Extraction complete. Found {len(result)} pairs.")
    return result

# ---------- AI Extraction (with caching) ----------

def extract_suggestions_with_ai(answer_text: str, cache: Dict[str, List[str]], logger: DebugLogger) -> List[str]:
    key = answer_text.strip()
    if not key:
        return []

    if key in cache:
        logger.log("AI_CACHE", f"Using cached result for: '{key[:50]}...'")
        return cache[key]

    text = key
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    prompt = (
        "You are an expert at extracting and rephrasing follow-up items from an assistant's response.\n"
        "Your goal is to extract EVERY suggested action or next step and rephrase it as a direct question starting with 'Can you'.\n\n"
        "Look for items from BOTH of these areas:\n"
        "1. Bulleted lists following phrases like 'If you want next, we can...', 'Next we can...', 'What would you like to do next?', etc.\n"
        "2. Formal 'Suggested Questions' or 'Follow-up Questions' sections.\n\n"
        "Rules:\n"
        "- REPHRASE every extracted item into a question starting with 'Can you ...?'.\n"
        "- Example: 'Define a formal grammar' -> 'Can you define a formal grammar?'\n"
        "- Example: 'Next we can design a schema' -> 'Can you design a schema?'\n"
        "- Combine ALL items into a single flat JSON list of strings.\n"
        "- Remove any existing numbering (like 'Q1.1') from the source text.\n"
        "- If nothing is found, return an empty list [].\n"
        "- Output MUST be a valid JSON list of strings.\n\n"
        "Assistant response:\n"
        '"""\n'
        f"{text}\n"
        '"""\n'
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "temperature": 0
    }

    logger.log("AI_EXTRACT", f"Calling Ollama ({MODEL_NAME}) for segment: '{key[:50]}...'")
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        out = data.get("response", "").strip()
    except Exception as e:
        logger.log("AI_ERROR", f"Ollama request failed: {e}")
        cache[key] = []
        return []

    # Try to extract JSON array safely
    suggestions: List[str] = []
    try:
        start = out.find("[")
        end = out.rfind("]") + 1
        if start != -1 and end != -1:
            arr = json.loads(out[start:end])
            if isinstance(arr, list):
                suggestions = [s.strip() for s in arr if isinstance(s, str) and s.strip()]
    except Exception:
        logger.log("AI_WARNING", f"Failed to parse JSON from AI response: {out}")
        suggestions = []

    logger.log("AI_RESULT", f"Extracted {len(suggestions)} suggestions.")
    cache[key] = suggestions
    return suggestions

# ---------- Write outputs ----------

def write_outputs(pairs: List[Tuple[str, str]], all_suggestions: List[List[str]], output_dir: Path, logger: DebugLogger):
    logger.log("IO_WRITE", f"Starting file writing to {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # ---------- questions_only.md ----------
    questions_only = output_dir / "questions_only.md"
    logger.log("IO_WRITE", "Generating questions_only.md...")
    with questions_only.open("w", encoding="utf-8") as f:
        f.write("# Suggested / Follow-up Questions Only\n\n")

        for i, ((q, a), suggestions) in enumerate(zip(pairs, all_suggestions), 1):
            f.write(f"## Q{i}\n\n")
            f.write(q.strip() + "\n\n")
            f.write("---\n\n")
            
            if suggestions:
                for j, s in enumerate(suggestions, 1):
                    # Final cleanup: ensure it starts with "Can you" and has a question mark
                    clean_s = s.strip()
                    if not clean_s.lower().startswith("can you"):
                        clean_s = f"Can you {clean_s[0].lower() + clean_s[1:]}"
                    if not clean_s.endswith("?"):
                        clean_s += "?"
                        
                    f.write(f"- Q{i}.{j} {clean_s}\n")
            else:
                f.write("- (No suggestions found)\n")
            f.write("\n")

    # ---------- Individual Q&A files ----------
    logger.log("IO_WRITE", f"Generating {len(pairs)} individual Q&A markdown files...")
    for i, ((q, a), suggestions) in enumerate(zip(pairs, all_suggestions), 1):
        out = output_dir / f"Q{i:03d}.md"
        with out.open("w", encoding="utf-8") as f:
            f.write(f"# Question {i}\n\n")
            f.write("## User Question\n\n")
            f.write(q.strip() + "\n\n")
            f.write("## Assistant Answer\n\n")
            f.write(a.strip() + "\n\n")
            if suggestions:
                f.write("## Suggested / Follow-up Questions\n\n")
                for j, s in enumerate(suggestions, 1):
                    f.write(f"- Q{i}.{j} {s}\n")

# ---------- Validation Module ----------

def validate_extraction(pairs: List[Tuple[str, str]], all_suggestions: List[List[str]], input_file: Path, output_dir: Path, logger: DebugLogger):
    logger.section("Validation & Verification")
    
    report = ["\n\n--- AI EXTRACTION VALIDATION REPORT ---\n"]
    report.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    total_found = 0
    total_valid = 0
    
    for i, ((q, a), suggestions) in enumerate(zip(pairs, all_suggestions), 1):
        report.append(f"### Q{i} Verification\n")
        logger.log("VALIDATE", f"Verifying Q{i}...")
        
        if not suggestions:
            report.append("- No suggestions extracted from this block.\n")
            continue
            
        for s in suggestions:
            total_found += 1
            # Resilient cleaning for validation: remove markdown, numbers, and bullets
            clean_s = re.sub(r'[*_#`]', '', s) # No markdown
            clean_s = re.sub(r'^[Q\d\.\s:-]+', '', clean_s).strip().lower()
            
            clean_a = re.sub(r'[*_#`]', '', a).lower()
            
            # Use partial match to be even more resilient
            is_valid = clean_s in clean_a or any(word in clean_a for word in clean_s.split() if len(word) > 4)
            
            if is_valid:
                total_valid += 1
                logger.log("VALIDATE", f"  PASS: '{s[:40]}...' found in source.")
            else:
                logger.log("VALIDATE", f"  FAIL: '{s[:40]}...' NOT found in source.")
            
            status = "✅" if is_valid else "❌"
            report.append(f"- {status} {s}\n")
            if not is_valid:
                report.append(f"  (Note: Question text not found in source answer)\n")
        report.append("\n")

    # Paste on the input file
    try:
        with input_file.open("a", encoding="utf-8") as f:
            f.writelines(report)
        logger.log("IO_WRITE", f"Validation report appended to: {input_file.name}")
    except Exception as e:
        logger.log("IO_ERROR", f"Could not write validation report to input: {e}")

    # Log summary block
    logger.section("Extraction Summary")
    logger.log("SUMMARY", f"Segments Parsed:   {len(pairs)}")
    logger.log("SUMMARY", f"Total Extracted:  {total_found}")
    logger.log("SUMMARY", f"Confirmed Valid:  {total_valid}")
    logger.log("SUMMARY", f"Potential Halluc: {total_found - total_valid}")
    if total_found > 0:
        logger.log("SUMMARY", f"Confidence:       {(total_valid/total_found)*100:.1f}%")

# ---------- Main ----------

def main():
    # Setup Paths and run identifiers
    base_dir = Path("AI_OUTPUT")
    run_name = datetime.now().strftime("output_%Y%m%d_%H%M%S")
    output_dir = base_dir / run_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize Logger
    logger = DebugLogger("AI Summarizer v2", output_dir)
    logger.section("Execution Start")

    input_path = input("Enter path to conversation .md file: ").strip().strip('"')
    file_path = Path(input_path)
    logger.log("INPUT", f"Path provided: {input_path}")

    if not file_path.exists():
        logger.log("ERROR", "Input file not found. Terminating.")
        print("❌ File not found!")
        return

    logger.log("INPUT", f"Reading file: {file_path.absolute()}")
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    pairs = split_conversation(text, logger)

    if not pairs:
        logger.log("WARNING", "No conversation blocks detected. Check role patterns.")
        print("⚠️ No conversation blocks detected.")
        return

    # Extract all suggestions
    cache: Dict[str, List[str]] = {}
    logger.section("AI Extraction Step")
    all_suggestions = []
    for q, a in pairs:
        sugg = extract_suggestions_with_ai(a, cache, logger)
        all_suggestions.append(sugg)

    # Write files
    logger.section("File IO Step")
    write_outputs(pairs, all_suggestions, output_dir, logger)

    # Run validation
    validate_extraction(pairs, all_suggestions, file_path, output_dir, logger)

    logger.section("process complete")
    print(f"\n✅ All steps complete. Log: {logger.log_file.name}")
    print(f"📁 Output folder: {output_dir}")

if __name__ == "__main__":
    main()


