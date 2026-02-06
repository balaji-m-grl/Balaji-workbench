# AI Tool Chat History Synthesizer

A comprehensive solution to extract, verify, and synthesize complete ChatGPT conversation history into structured Markdown format.

## 🎯 Purpose

When exporting ChatGPT conversations, some questions and responses can be missed or truncated. This tool provides a **multi-step verification approach** to ensure 100% completeness.

## ✨ Features

- **Automated Comparison**: Compare ChatGPT-generated and extension-exported markdown files
- **Gap Detection**: Identify missing questions, responses, and follow-ups
- **Smart Matching**: Fuzzy matching to handle slight formatting differences
- **Gap-Filling Prompts**: Auto-generate prompts to request missing content
- **Interactive Workflow**: Jupyter notebook for step-by-step processing
- **Verification**: Validate final output for completeness

## 📁 Project Structure

```
AI_Tool_Chat_History_Synthesizer/
├── chat_history_synthesizer.py    # Main Python script
├── chat-history.ipynb              # Interactive Jupyter notebook
├── prompts.md                      # Ready-to-use ChatGPT prompts
├── workflow_guide.md               # Complete user guide
├── AI_Tool_Chat_History_Synthesizer_Requirement.md  # Original requirements
├── examples/                       # Sample files for testing
│   ├── sample_chatgpt_generated.md
│   ├── sample_extension_export.md
│   └── README.md
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Chrome browser with [ChatGPT to Markdown extension](https://chromewebstore.google.com/detail/dloobgjjpoohngalnjepgdggjeempdec)
- (Optional) Jupyter Notebook for interactive workflow

### Installation

No installation required! Just clone or download this folder.

### The 4-Step Process

#### Step 1: Generate Markdown from ChatGPT

1. Open your ChatGPT conversation
2. Use the prompt from `prompts.md` (Section 1)
3. Save output as `chatgpt_generated.md`

#### Step 2: Export Using Chrome Extension

1. Open the same conversation in Chrome
2. Scroll through entire conversation
3. Click extension → Export to Markdown
4. Save as `extension_export.md`

#### Step 3: Compare Files

**Option A: Python Script**
```bash
python chat_history_synthesizer.py --chatgpt chatgpt_generated.md --extension extension_export.md
```

**Option B: Jupyter Notebook**
```bash
jupyter notebook chat-history.ipynb
# Run cells sequentially
```

#### Step 4: Fix Gaps (if any)

1. Review `comparison_report.txt`
2. Use `gap_filling_prompt.txt` in ChatGPT
3. Save result as `final_verified.md`

## 📖 Documentation

- **[workflow_guide.md](workflow_guide.md)** - Detailed step-by-step instructions
- **[prompts.md](prompts.md)** - All ChatGPT prompts you'll need
- **[examples/README.md](examples/README.md)** - How to test with sample files

## 🧪 Testing

Test the tool with provided sample files:

```bash
python chat_history_synthesizer.py --chatgpt examples/sample_chatgpt_generated.md --extension examples/sample_extension_export.md --output examples/test_report.txt
```

Expected result: Detects 1 missing question in ChatGPT file.

## 📊 Output Files

| File | Description |
|------|-------------|
| `comparison_report.txt` | Detailed gap analysis with statistics |
| `gap_filling_prompt.txt` | Ready-to-paste ChatGPT prompt |
| `final_verified.md` | Your complete, verified conversation |

## 🔍 How It Works

1. **Markdown Parser**: Extracts questions (H2), follow-ups (H3), and responses
2. **Fuzzy Matching**: Uses 80% similarity threshold to match questions
3. **Gap Detection**: Identifies missing content in either file
4. **Order Verification**: Checks chronological consistency
5. **Similarity Scoring**: Calculates overall completeness percentage

## 💡 Best Practices

- ✅ Always scroll to top of conversation before extraction
- ✅ Use both methods (ChatGPT + Extension) for redundancy
- ✅ Aim for >95% similarity score
- ✅ Verify technical accuracy of responses
- ✅ Keep original exports as backups

## 🛠️ Command Line Options

```bash
python chat_history_synthesizer.py --help

Options:
  --chatgpt PATH      Path to ChatGPT generated markdown
  --extension PATH    Path to extension exported markdown
  --output PATH       Output file for comparison report (default: comparison_report.txt)
  --test              Run with test files
```

## 📝 Example Workflow

```bash
# 1. Compare files
python chat_history_synthesizer.py --chatgpt my_chat.md --extension my_chat_ext.md

# 2. Review report
cat comparison_report.txt

# 3. If gaps found, use the generated prompt
cat gap_filling_prompt.txt
# Copy and paste into ChatGPT

# 4. Verify final output
python chat_history_synthesizer.py --chatgpt final_verified.md --extension my_chat_ext.md
```

## 🤝 Contributing

This is a personal tool, but feel free to adapt it for your needs!

## 📄 License

Free to use and modify.

## 🆘 Troubleshooting

**Q: ChatGPT truncates the output**
- A: Ask it to "continue" or break into smaller chunks

**Q: Extension misses messages**
- A: Scroll more slowly, refresh page and retry

**Q: Low similarity score (<80%)**
- A: Verify you're comparing the same conversation
- A: Check for encoding issues (ensure UTF-8)

**Q: Too many order mismatches**
- A: Usually cosmetic - verify content is present
- A: Use extension export order as canonical

For more help, see [workflow_guide.md](workflow_guide.md).

---

**Created**: February 2026  
**Purpose**: Ensure complete ChatGPT conversation exports without data loss
