```mermaid
sequenceDiagram
    participant U as User
    participant M as Main Program
    participant IH as Input Handler
    participant IV as Input Validator
    participant MR as Markdown Reader
    participant CP as Conversation Parser
    participant AE as AI Suggestion Extractor
    participant OA as Ollama API
    participant OW as Output Writer
    participant VM as Validation Module
    participant DL as Debug Logger
    participant PL as Performance Logger

    U->>M: Start script
    M->>IH: Provide file/folder path
    IH->>DL: Log input received

    IH->>IV: Validate path & files
    IV->>DL: Log validation result

    alt Invalid file
        IV-->>M: Invalid / Skip
        M->>DL: Log skip
    else Valid file
        IV-->>MR: Valid .md file
        MR->>DL: Log read start
        MR-->>CP: Raw markdown text

    CP->>DL: Log parsing start
        CP-->>M: Q&A pairs list

    loop For each Assistant Answer
            M->>AE: Send assistant answer
            AE->>PL: Log CPU/RAM (pre-call)
            AE->>OA: Send prompt
            OA-->>AE: JSON suggestions
            AE->>PL: Log CPU/RAM (post-call)
            AE->>DL: Log AI result
            AE-->>M: Suggestions list
        end

    M->>OW: Send pairs + suggestions
        OW->>DL: Log file writing
        OW-->>M: Generated markdown files

    M->>VM: Send input + pairs + suggestions
        VM->>DL: Log validation start
        VM-->>M: VALIDATION_REPORT.md + Status
    end

    M->>PL: Write final performance summary
    M->>DL: Write final debug summary
    M-->>U: Print final status & output paths
