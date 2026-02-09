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
    r"^##\s*User",
    r"^##\s*You",
]

ASSISTANT_PATTERNS = [
    r"^\*\*ChatGPT:\*\*",
    r"^\*\*Assistant:\*\*",
    r"^Assistant:",
    r"^ChatGPT:",
    r"^##\s*Assistant",
    r"^##\s*ChatGPT",
]

USER_RE = re.compile("|".join(USER_PATTERNS), re.IGNORECASE)
ASSISTANT_RE = re.compile("|".join(ASSISTANT_PATTERNS), re.IGNORECASE)

# ---------- Split conversation ----------

def split_conversation(md_text: str) -> List[Tuple[str, str]]:
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

    flush()
    return [(u, a) for u, a in blocks if u.strip() or a.strip()]

# ---------- AI Extraction (with caching) ----------

def extract_suggestions_with_ai(answer_text: str, cache: Dict[str, List[str]]) -> List[str]:
    key = answer_text.strip()
    if not key:
        return []

    if key in cache:
        return cache[key]

    text = key
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    prompt = (
        "Extract all follow-up or suggested questions from the text below.\n"
        "Return ONLY a JSON array of strings.\n"
        "If none, return [].\n\n"
        "Text:\n"
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

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        out = data.get("response", "").strip()
    except Exception as e:
        print("⚠️ Ollama request failed:", e)
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
        suggestions = []

    cache[key] = suggestions
    return suggestions

# ---------- Write outputs ----------

def write_outputs(pairs: List[Tuple[str, str]], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    cache: Dict[str, List[str]] = {}

    # Precompute suggestions
    all_suggestions = []
    for q, a in pairs:
        sugg = extract_suggestions_with_ai(a, cache)
        all_suggestions.append(sugg)

    # questions_only.md
    questions_only = output_dir / "questions_only.md"
    with questions_only.open("w", encoding="utf-8") as f:
        f.write("# Suggested / Follow-up Questions (AI Extracted)\n\n")

        for i, ((q, a), suggestions) in enumerate(zip(pairs, all_suggestions), 1):
            if not suggestions:
                continue

            f.write(f"## Q{i}\n\n")
            f.write(q.strip() + "\n\n")

            for j, s in enumerate(suggestions, 1):
                f.write(f"- Q{i}.{j} {s}\n")

            f.write("\n")

    # Individual Q&A files
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

# ---------- Main ----------

def main():
    input_path = input("Enter path to conversation .md file: ").strip().strip('"')
    file_path = Path(input_path)

    if not file_path.exists():
        print("❌ File not found!")
        return

    text = file_path.read_text(encoding="utf-8", errors="ignore")
    pairs = split_conversation(text)

    if not pairs:
        print("⚠️ No conversation blocks detected.")
        return

    base_dir = Path("AI_OUTPUT")
    run_name = datetime.now().strftime("output_%Y%m%d_%H%M%S")
    output_dir = base_dir / run_name


    write_outputs(pairs, output_dir)

    print("✅ Done!")
    print(f"📄 Processed {len(pairs)} Q&A pairs")
    print(f"📁 Output folder: {output_dir}")

if __name__ == "__main__":
    main()
