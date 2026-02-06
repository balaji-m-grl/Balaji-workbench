# ChatGPT Prompts for Chat History Extraction

This document contains ready-to-use prompts for extracting and verifying ChatGPT conversation history.

---

## 1. Initial Extraction Prompt

**Purpose**: Get structured markdown from ChatGPT with all questions and responses

**Prompt**:
```
List all the questions in this thread in chronological order.
Use:

- H2 (##) for each main question (first 2 lines bolded)
- Normal text for remaining question content
- Add the assistant response in 2–5 concise lines after "Response:"
- Use H3 (###) for follow-up questions with indexing (e.g., 1.1, 1.2)
- Ensure no question or response is skipped
- Include all clarifications and solution branches
- Maintain chronological order

Format example:

## 1. How to remove duplicates in string?

Explain the logic to remove duplicate characters from a string in C#.

Response:
Use Dictionary<char,int> or HashSet<char> approach to track seen characters and build result string with only unique characters.

### 1.1 Why use Dictionary?

Response:
Dictionary allows counting occurrences, while HashSet only tracks presence. Choose based on whether you need counts.
```

---

## 2. Gap-Filling Prompt Template

**Purpose**: Request missing content after comparison

**Prompt Template**:
```
These questions appear to be missing from the previous Markdown output:

1. [Question title 1]
2. [Question title 2]
3. [Question title 3]

Please regenerate a complete Markdown including everything without omission.
Use the following format:
- H2 (##) for each main question
- Normal text for question content
- Add the assistant response after 'Response:'
- Use H3 (###) for follow-up questions
- Ensure chronological order
- Include all previous questions plus these missing ones
```

**Note**: Replace the bracketed items with actual missing question titles from the comparison report.

---

## 3. Verification Prompt

**Purpose**: Final completeness check

**Prompt**:
```
Please verify that the generated Markdown includes:

1. All user questions from the beginning of this conversation
2. All assistant responses
3. All follow-up clarifications
4. All solution variations and branches
5. Proper header structure (H2 for main, H3 for follow-ups)
6. Chronological order maintained

If anything is missing, please regenerate the complete Markdown.
```

---

## 4. Specific Section Extraction

**Purpose**: Extract a specific portion of the conversation

**Prompt Template**:
```
Extract questions [START_INDEX] through [END_INDEX] from this conversation.

Use the same format:
- H2 (##) for main questions
- H3 (###) for follow-ups
- Include full responses
- Maintain chronological order
```

---

## 5. Response Expansion Prompt

**Purpose**: Get more detailed responses if initial ones are too brief

**Prompt**:
```
The responses in the previous Markdown are too brief. 
Please regenerate with:
- More detailed responses (3-5 lines minimum)
- Key technical details included
- Code examples where relevant
- Maintain the same structure (H2/H3 headers)
```

---

## Tips for Best Results

1. **Always scroll to the top** of the conversation before asking for extraction
2. **Be specific** about what you want included
3. **Request verification** after receiving the output
4. **Use the extension export** as a backup/comparison source
5. **Ask for regeneration** if you notice gaps rather than trying to patch manually
