## 1. How to remove duplicates in a string?

I need to remove duplicate characters from a string in C#. What's the best approach?

Response:
Use a `HashSet<char>` to track seen characters while building a new string. Iterate through each character, add to HashSet if not present, and append to result. Time complexity: O(n).

### 1.1 Why use HashSet instead of Dictionary?

Response:
HashSet is simpler when you only need to track presence, not count. Dictionary is useful if you need character frequencies. For duplicate removal, HashSet is more efficient and cleaner.

## 2. Can you show a code example?

Please provide a complete C# implementation with the HashSet approach.

Response:

```csharp
public static string RemoveDuplicates(string input) {
    var seen = new HashSet<char>();
    var result = new StringBuilder();
    foreach (char c in input) {
        if (seen.Add(c)) result.Append(c);
    }
    return result.ToString();
}
```

### 2.1 What about case sensitivity?

Response:
Convert to lowercase before checking: `if (seen.Add(char.ToLower(c)))`. Store original character in result to preserve case.

## 3. How does this handle Unicode characters?

Will this work correctly with emojis and special Unicode characters?

Response:
Yes, C# char type handles Unicode BMP characters. For full Unicode support including emojis (surrogate pairs), use StringInfo class to iterate by grapheme clusters instead of individual chars.

### 3.1 Can you show the Unicode-safe version?

Response:

```csharp
var seen = new HashSet<string>();
var enumerator = StringInfo.GetTextElementEnumerator(input);
while (enumerator.MoveNext()) {
    string element = enumerator.GetTextElement();
    if (seen.Add(element)) result.Append(element);
}
```

## 4. What's the performance impact?

How does this compare to other approaches in terms of speed and memory?

Response:
HashSet approach: O(n) time, O(k) space where k is unique characters. Alternative LINQ `Distinct()`: same complexity but slightly slower due to overhead. Nested loop approach: O(n²) time - avoid for large strings.


## 5.What about performance with large strings?

Please regenerate a complete Markdown including everything without omission.
Use the following format:

- H2 (##) for each main question
- Normal text for question content
- Add the assistant response after 'Response:'
- Use H3 (###) for follow-up questions
- Ensure chronological order
