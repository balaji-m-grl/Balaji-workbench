# Suggested / Follow-up Questions (AI Extracted)

## Q3

Add PD 3.1 / EPR extensions

* * *

- Q3.1 What specific cable requirements are there for PD 3.1?
- Q3.2 How do the new timing and safety constraints in EPR differ from previous versions?
- Q3.3 Why is it important to explicitly encode 'Is EPR even allowed here?' in the schema?
- Q3.4 What does `epr_supported` mean in the `epr_capabilities` JSON structure?
- Q3.5 Could you explain why preventing invalid EPR reasoning with the provided JSON structure is crucial?
- Q3.6 Are there any other new fault classes introduced by PD 3.1's EPR mode?

## Q4

Design an EPR scenario generator

* * *

- Q4.1 What specific criteria or checks should be included for the EPR scenarios to ensure they cover all valid, invalid but realistic failures, and respect both spec constraints and ground truth labels?
- Q4.2 How can the deterministic aspect of the generator be implemented efficiently without significantly impacting performance when scaling to millions of variants?
- Q4.3 Are there any specific design patterns or best practices that should be considered for each block in the high-level architecture diagram?
- Q4.4 How do you plan to handle edge cases and unexpected input scenarios, especially those outside the typical 'happy path' logic?
- Q4.5 Do you foresee any challenges in automating the labeling process based on spec violations, compliance checks, and root cause mappings? How would you address these challenges?
- Q4.6 In your view, what is the most crucial aspect to focus on during the design of the EPR scenario generator—architecture, algorithmic flow, control knobs, or something else?

## Q5

spec-rule DSL

* * *

- Q5.1 What are the core design principles of the spec-rule DSL?
- Q5.2 How do agents reason with the spec-rule DSL?
- Q5.3 Is the spec-rule DSL executable or does it need to be executed by something else?
- Q5.4 Can you provide an example of a rule in the spec-rule DSL syntax (YAML-like)?
- Q5.5 What are the timing rules implemented parametrically and not hardcoded?
- Q5.6 Are there any specific examples of violations explained by the spec-rule DSL?
- Q5.7 How does the spec-rule DSL allow for composition with future standards like PD 3.2?

## Q6

Map DSL rules to USB-IF test cases

* * *

- Q6.1 What specific capabilities and policies are being addressed in the capability & policy rules?
- Q6.2 Can you provide more concrete examples of how these capability & policy rules are applied in the DSL?
- Q6.3 How does the mapping model ensure traceability of USB-IF test cases to DSL rules?

