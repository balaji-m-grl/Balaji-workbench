from pathlib import Path
import re
import json
import requests
from typing import List, Tuple, Dict
from datetime import datetime

# ---------- Ollama Config ----------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"  # fast & light
MAX_CHARS = 3000  # limit text sent to model

# ---------- Role markers ----------
# Improved patterns to match more variations of Chat history exports
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
    """A robust logger that creates a unique log file for each run."""
    def __init__(self, project_name: str, output_dir: Path):
        self.project_name = project_name
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.output_dir / f"DEBUG_LOG_{timestamp}.txt"
        
        self.log("INIT", f"Logger started for {project_name}")
        self.log("ENV", f"Output Dir: {self.output_dir.resolve()}")

    def log(self, category: str, message: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        line = f"[{now}] [{category:10}] {message}"
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

# ---------- Data Validation ----------

def validate_input_file(file_path: Path, logger: DebugLogger) -> bool:
    """Basic validation of the input file."""
    if not file_path.exists():
        logger.log("VAL_FAIL", f"File not found: {file_path}")
        return False
    if file_path.stat().st_size == 0:
        logger.log("VAL_FAIL", f"File is empty: {file_path}")
        return False
    return True

# ---------- Conversation Parsing ----------

def split_conversation(md_text: str, logger: DebugLogger) -> List[Tuple[str, str]]:
    logger.log("PARSING", "Starting markdown split...")
    lines = md_text.splitlines()

    blocks = []
    current_role = None
    current_user_lines = []
    current_assistant_lines = []

    def flush():
        if current_user_lines or current_assistant_lines:
            u_text = "\n".join(current_user_lines).strip()
            a_text = "\n".join(current_assistant_lines).strip()
            if u_text or a_text:
                blocks.append((u_text, a_text))

    for line in lines:
        s = line.strip()

        if USER_RE.match(s):
            if current_role == "assistant":
                flush()
                current_user_lines = []
                current_assistant_lines = []
            current_role = "user"
            continue

        if ASSISTANT_RE.match(s):
            current_role = "assistant"
            continue

        if current_role == "user":
            current_user_lines.append(line)
        elif current_role == "assistant":
            current_assistant_lines.append(line)

    flush()
    
    # Cleaning function to remove noise
    def clean_block(text: str) -> str:
        # Remove repeated chunks and artifacts
        text = re.sub(r'^\s*\*+\s*\*+\s*\*+\s*$', '', text, flags=re.MULTILINE)
        return text.strip()

    result = [(clean_block(u), clean_block(a)) for u, a in blocks if u or a]
    logger.log("PARSING", f"Extracted {len(result)} Q&A pairs.")
    return result

# ---------- AI Extraction ----------

def extract_suggestions_from_ai(answer_text: str, cache: Dict[str, List[str]], logger: DebugLogger) -> List[str]:
    """Uses Ollama to extract suggested/follow-up questions from the assistant's answer."""
    # 1. Strip existing artifacts from the answer to prevent confusion
    # This removes previous validation reports that might be in the file
    clean_answer = re.split(r'--- AI EXTRACTION VALIDATION REPORT ---', answer_text, flags=re.IGNORECASE)[0]
    key = clean_answer.strip()
    
    if not key:
        return []

    if key in cache:
        logger.log("AI_CACHE", "Using cached suggestions.")
        return cache[key]

    # Focus strictly on the end of the response
    MAX_AI_CHARS = 4000
    if len(key) > MAX_AI_CHARS:
        text = "[...] " + key[-MAX_AI_CHARS:]
    else:
        text = key

    # Simpler, more direct prompt for small models (Qwen 3B)
    prompt = (
        "Instructions: Find the 'If you want next' or 'Suggested follow-up' list at the END of the text below.\n"
        "Extract the exact text of each suggestion into a JSON list of strings.\n\n"
        "Rules:\n"
        "1. Only look at the final section (ignore the main explanation).\n"
        "2. Keep the original wording (e.g., 'Draft a mock change note').\n"
        "3. If there are no suggestions at the end, return [].\n\n"
        "Text:\n"
        f"{text}\n\n"
        "Output JSON (e.g. [\"Suggestion 1\", \"Suggestion 2\"]):"
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0}
    }

    logger.log("AI_CALL", f"Requesting suggestions (length: {len(text)})")
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=90)
        resp.raise_for_status()
        data = resp.json()
        raw_response = data.get("response", "").strip()
        
        # Log the raw response for debugging if needed
        logger.log("AI_RAW", f"Raw response: {raw_response}")
        
        # Parse JSON
        parsed = json.loads(raw_response)
        if isinstance(parsed, dict) and "suggestions" in parsed:
            suggestions = parsed["suggestions"]
        elif isinstance(parsed, list):
            suggestions = parsed
        else:
            suggestions = []
            
        # Clean suggestions
        suggestions = [str(s).strip() for s in suggestions if s]
        
    except Exception as e:
        logger.log("AI_ERROR", f"Failed to extract suggestions: {e}")
        suggestions = []

    cache[key] = suggestions
    logger.log("AI_RESULT", f"Found {len(suggestions)} suggestions.")
    return suggestions

# ---------- Write Outputs ----------

def write_outputs(pairs: List[Tuple[str, str]], all_suggestions: List[List[str]], output_dir: Path, logger: DebugLogger):
    """Generates the requested individual and combined files."""
    logger.section("File Generation")
    
    # 1. Single file with all Questions and Follow-ups
    combined_file = output_dir / "All_Questions_and_Followups.md"
    logger.log("IO", f"Creating combined questions file: {combined_file.name}")
    
    with combined_file.open("w", encoding="utf-8") as f:
        f.write("# Questions and AI Recommendations\n\n")
        f.write("Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        
        for i, ((user_q, _), suggestions) in enumerate(zip(pairs, all_suggestions), 1):
            f.write(f"### Q{i}: {user_q}\n\n")
            if suggestions:
                for j, s in enumerate(suggestions, 1):
                    # Use original phrasing
                    f.write(f"**Q{i}.{j}**: {s}\n\n")
            else:
                f.write("*No follow-up suggestions for this question.*\n\n")
            f.write("---\n\n")

    # 2. Individual Q&A files
    logger.log("IO", f"Creating {len(pairs)} separate Q&A files...")
    for i, ((user_q, assistant_a), suggestions) in enumerate(zip(pairs, all_suggestions), 1):
        qa_file = output_dir / f"Q{i:03d}_Full.md"
        with qa_file.open("w", encoding="utf-8") as f:
            f.write(f"# Question {i}\n\n")
            f.write("## 👤 User Question\n\n")
            f.write(user_q + "\n\n")
            f.write("## 🤖 Assistant Answer\n\n")
            f.write(assistant_a + "\n\n")
            
            if suggestions:
                f.write("## 💡 Recommended Follow-ups\n\n")
                for j, s in enumerate(suggestions, 1):
                    f.write(f"- **Q{i}.{j}**: {s}\n")

# ---------- Validation Module ----------

def run_validation(input_text: str, pairs: List[Tuple[str, str]], all_suggestions: List[List[str]], output_dir: Path, logger: DebugLogger) -> Dict:
    """
    Performs validation checks to verify output integrity against the input.
    Checks for coverage, extraction accuracy, and suggestion validity.
    """
    logger.section("Validation & Quality Check")
    
    report_file = output_dir / "VALIDATION_REPORT.md"
    logger.log("VAL", f"Generating validation report: {report_file.name}")

    total_q = len(pairs)
    total_suggestions = sum(len(s) for s in all_suggestions)
    
    # 1. Integrity Check: Do the extracted parts exist in the input?
    integrity_issues = []
    total_extracted_chars = 0
    for i, (u, a) in enumerate(pairs, 1):
        total_extracted_chars += len(u) + len(a)
        u_snippet = u[:100] if len(u) > 100 else u
        a_snippet = a[:100] if len(a) > 100 else a
        
        # Check if the start of the extracted block is in the original text
        if u_snippet and u_snippet.splitlines()[0] not in input_text:
            integrity_issues.append(f"Q{i} user question header/start mismatch.")
        if a_snippet and a_snippet.splitlines()[0] not in input_text:
            integrity_issues.append(f"Q{i} assistant answer header/start mismatch.")

    # 2. Coverage Check
    input_chars = len(input_text)
    coverage = (total_extracted_chars / input_chars) * 100 if input_chars > 0 else 0
    
    # Determine Status
    status = "PASSED"
    if coverage < 30:
        status = "WARNING (Low Coverage)"
    if integrity_issues:
        status = "WARNING (Integrity Issues)"
    if total_q == 0:
        status = "FAILED (No Content)"

    report = [
        "# Extraction Validation Report\n",
        f"**Final Status: {status}**\n",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
        "## Metrics\n",
        f"- Total Q&A Pairs: {total_q}\n",
        f"- Total Suggestions Found: {total_suggestions}\n",
        f"- Input Length: {input_chars} characters\n",
        f"- Extracted Length: {total_extracted_chars} characters\n",
        f"- **Coverage: {coverage:.1f}%**\n",
        "\n## Detailed Checks\n"
    ]

    if integrity_issues:
        report.append("### ⚠️ Integrity Issues\n")
        for issue in integrity_issues:
            report.append(f"- {issue}\n")
        report.append("\n")

    for i, ((u, a), suggestions) in enumerate(zip(pairs, all_suggestions), 1):
        report.append(f"### Q{i} Suggestion Verification\n")
        if not suggestions:
            report.append("- Info: No suggestions extracted.\n")
        else:
            for s in suggestions:
                clean_s = re.sub(r'[^\w\s]', '', s).lower()
                clean_a = re.sub(r'[^\w\s]', '', a).lower()
                words = [w for w in clean_s.split() if len(w) > 3]
                match_count = sum(1 for w in words if w in clean_a)
                is_valid = match_count >= min(len(words), 1) if words else True
                icon = "✅" if is_valid else "❓"
                report.append(f"- {icon} Suggestion: {s}\n")
        report.append("\n")

    with report_file.open("w", encoding="utf-8") as f:
        f.writelines(report)
    
    summary = f"Validation {status}. Coverage: {coverage:.1f}%. Q&A Pairs: {total_q}."
    logger.log("VAL", summary)
    return {"status": status, "summary": summary}


# ---------- Main Execution ----------

def main():
    # Setup directories
    base_output = Path("AI_OUTPUT")
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = base_output / f"run_{run_timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Init Logger
    logger = DebugLogger("AI Summarizer v3", output_dir)
    logger.section("Process Start")

    # Input handling
    print("\n--- AI Conversation Summarizer ---")
    input_str = input("Enter the path to your conversation .md file: ").strip().strip('"')
    input_path = Path(input_str)

    if not validate_input_file(input_path, logger):
        print(f"❌ Error: Invalid input file. Check logs at {logger.log_file}")
        return

    # 1. Parse
    logger.log("STEP", "Reading and parsing conversation...")
    text = input_path.read_text(encoding="utf-8", errors="ignore")
    pairs = split_conversation(text, logger)

    if not pairs:
        logger.log("ERROR", "No conversation blocks found.")
        print("❌ No conversation blocks found. Check role markers in the script.")
        return

    # 2. Extract Suggestions (with Cache)
    logger.log("STEP", "Extracting suggestions via AI...")
    cache: Dict[str, List[str]] = {}
    all_suggestions = []
    for _, a in pairs:
        all_suggestions.append(extract_suggestions_from_ai(a, cache, logger))

    # 3. Write Outputs
    logger.log("STEP", "Writing output files...")
    write_outputs(pairs, all_suggestions, output_dir, logger)

    # 4. Validate
    logger.log("STEP", "Running validation...")
    val_results = run_validation(text, pairs, all_suggestions, output_dir, logger)

    logger.section("Process Complete")
    final_status = f"FINAL STATUS: {val_results['status']} - {val_results['summary']}"
    logger.log("EXIT", final_status)
    
    print(f"\n✅ {final_status}")
    print(f"📁 Results saved to: {output_dir.resolve()}")
    print(f"📄 Main log: {logger.log_file.name}")
    print(f"📄 Validation report: VALIDATION_REPORT.md")

if __name__ == "__main__":
    main()
