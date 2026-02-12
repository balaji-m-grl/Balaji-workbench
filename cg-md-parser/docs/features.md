| Entity     | Actions / Details                                                                                                                        | Tools / Tech Used      |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| Input      | Reads Markdown file(s) containing ChatGPT conversation (user + assistant)                                                                | Python, pathlib        |
| Output     | Generates:`<br>`• Individual Q&A MD files `<br>`• One combined questions MD file `<br>`• Validation report `<br>`• Debug log | Markdown, File I/O     |
| Feature 1  | Parser: Splits conversation into User Questions and Assistant Answers                                                                    | Regex, Python          |
| Feature 2  | Cleaner: Removes noise, duplicate sections, old validation blocks                                                                        | Regex, Python          |
| Feature 3  | AI Extractor: Extracts suggested / follow-up questions from answers                                                                      | Ollama API, Qwen2.5:3B |
| Feature 4  | Cache System: Avoids re-calling AI for same answers                                                                                      | Python dict            |
| Feature 5  | Output Generator: Writes per-question MD files and combined summary file                                                                 | Python, Markdown       |
| Feature 6  | Validation Engine: Checks coverage, integrity, and suggestion relevance                                                                  | Python, Regex          |
| Feature 7  | Debug Logger: Creates timestamped debug logs for each run                                                                                | datetime, File I/O     |
| Feature 8  | Batch Processor: Can process single file or entire folder of MD files                                                                    | pathlib                |
| Feature 9  | Run Isolation: Creates a new output folder per run with timestamp                                                                        | datetime, pathlib      |
| Feature 10 | Error Handling: Skips invalid files and logs failures                                                                                    | try/except, Logger     |
