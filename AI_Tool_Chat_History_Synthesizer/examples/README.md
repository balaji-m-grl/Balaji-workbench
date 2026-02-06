# Sample Files for Testing

This folder contains example markdown files to test the Chat History Synthesizer tool.

## Files

### sample_chatgpt_generated.md
Example output from ChatGPT using the extraction prompt. Uses:
- H2 (##) for main questions
- H3 (###) for follow-ups
- "Response:" prefix for answers

### sample_extension_export.md
Example output from the Chrome extension export. Uses:
- H2 (##) for main questions
- H3 (###) for follow-ups
- "**Response:**" with bold formatting
- Horizontal rules (---) between sections
- Contains one additional question not in ChatGPT version

## Testing the Tool

### Using Python Script

```bash
cd d:\Balaji-workbench\AI_Tool_Chat_History_Synthesizer

python chat_history_synthesizer.py --chatgpt examples/sample_chatgpt_generated.md --extension examples/sample_extension_export.md --output examples/test_report.txt
```

### Using Jupyter Notebook

1. Open `chat-history.ipynb`
2. Update file paths in Cell 1:
   ```python
   CHATGPT_FILE = 'examples/sample_chatgpt_generated.md'
   EXTENSION_FILE = 'examples/sample_extension_export.md'
   ```
3. Run all cells

## Expected Results

The comparison should find:
- **1 missing question** in ChatGPT file: "What about performance with large strings?"
- **High similarity score** (>90%)
- **No order mismatches** (questions are in same order)

This demonstrates how the tool identifies gaps between the two export methods.
