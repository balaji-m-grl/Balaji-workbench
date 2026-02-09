# Suggested / Follow-up Questions (AI Extracted)

## Q1

Wat is Synthetic data in model training,   
Explain with USB pd domain agent model training example

* * *


Wat is Synthetic data in model training,
Explain with USB pd domain agent model training example

* * *

### AI Suggested Questions

- (No AI follow-up questions found)

## Q2

Design a USB-PD synthetic data schema

* * *

### AI Suggested Questions

- (No AI follow-up questions found)

## Q3

Add PD 3.1 / EPR extensions

* * *

### AI Suggested Questions

- Q3.1 What are the new voltage levels introduced by PD 3.1 / EPR?
- Q3.2 Why does the schema need to explicitly encode 'Is EPR even allowed here?'
- Q3.3 How do legacy PD agents handle these optional blocks for schema extension?
- Q3.4 Why is it important that agent can immediately answer: ‘EPR negotiation should not have happened’ when checking source and sink capabilities?
- Q3.5 What are the critical requirements for cables in the context of PD 3.1?

## Q4

Design an EPR scenario generator

* * *

### AI Suggested Questions

- Q4.1 What types of failures can the EPR scenario generator generate?
- Q4.2 What are the key constraints that need to be respected by the EPR scenario generator?
- Q4.3 How will the EPR scenario generator handle scale issues, especially for millions of variants?
- Q4.4 Why is it important for the EPR scenario generator to be deterministic in certain scenarios?
- Q4.5 How can the EPR scenario generator produce ground-truth labels?
- Q4.6 Can you elaborate on the architecture of the EPRScenarioGenerator?
- Q4.7 Which blocks are independently testable within the high-level architecture of the EPR scenario generator?
- Q4.8 What is the role of the spec model and how does it differ from being text-based in your description?
- Q4.9 How does the spec model validate itself and label outcomes automatically?
- Q4.10 Can you provide an example of a specification rule for the cable component?
- Q4.11 What do the safety constraints include according to your taxonomy?
- Q4.12 What is the purpose of categorizing scenarios into core classes like EPR_HAPPY_PATH, EPR_POLICY_REJECT, EPR_CABLE_INVAL?

## Q5

spec-rule DSL

* * *

### AI Suggested Questions

- Q5.1 What is the purpose of the spec-rule DSL in your design?
- Q5.2 How does the spec-rule DSL differ from a programming language and a textual copy of the USB-IF spec?
- Q5.3 Can you elaborate on how the spec-rule DSL can be evaluated by machines?
- Q5.4 Why do you say it evaluates to true / false / violation?
- Q5.5 What makes the spec-rule DSL evolvable?
- Q5.6 How does the spec-rule DSL explain itself when violated?
- Q5.7 Can you provide an example of a rule in YAML-like syntax for future PD 3.2?
- Q5.8 What is the significance of structured like a schema in your design principles?
- Q5.9 Why are timing rules parametric and not hard-coded in the spec-rule DSL?
- Q5.10 How does the specification-layer reasoning layer interface with the agent reasoning layer?

## Q6

Map DSL rules to USB-IF test cases

* * *

### AI Suggested Questions

- Q6.1 What specific examples are included in the 'Concrete examples' section?
- Q6.2 How does the mapping block help traceability and certification workflows?
- Q6.3 Can you provide more details on how to compose and reuse DSL rules effectively?
- Q6.4 Could you elaborate on the difference between procedural and observable behavior-based test cases for USB-IF?
- Q6.5 What are some best practices for extending DSL rules with certification mapping blocks?
- Q6.6 How can we ensure that our DSL rules align properly with both the intention of the specification and the needs of the certification process?

## Q7

How to connect synthetic data fir real time scenario like having 2 drp connected with emarker cable and communication flow during pr swap and drswap and possible pkt collision if any one drp or eMarker design don't align with spec

* * *

### AI Suggested Questions

- (No AI follow-up questions found)

## Q8

How to find gaps in the pd spec using synthetic data simulation and make chage proposal for spec

* * *

### AI Suggested Questions

- (No AI follow-up questions found)

## Q9

real PR_SWAP/DR_SWAP ambiguity example as a mock spec gap

* * *

### AI Suggested Questions

- Q9.1 What are some specific technical details you would include in your mock spec gap case?
- Q9.2 Could you elaborate on how the mutual exclusion rules between PR_SWAP and DR_SWAP could be clarified further in the spec?
- Q9.3 Is there any precedent or industry practice that suggests which interpretation is more commonly implemented?
- Q9.4 How can the ambiguity regarding arbitration priority during overlapping swaps be addressed in future updates of the spec?
- Q9.5 What kind of impact might the 'quiet ownership' windows have on real-world implementations, and should they be explicitly defined?

