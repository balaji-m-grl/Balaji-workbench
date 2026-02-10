# Suggested / Follow-up Questions Only

## Q1

Wat is Synthetic data in model training,
Explain with USB pd domain agent model training example

---

- (No suggestions found)

## Q2

Design a USB-PD synthetic data schema

---

- Q2.1 Can you define the schema layers structure as JSON?
- Q2.2 Can you design the metadata layer for the USB-PD synthetic data schema?
- Q2.3 Can you create a topology layer with detailed specifications using JSON format?
- Q2.4 Can you outline the policy and capabilities layer in JSON format?
- Q2.5 Can you discuss how to implement fault injection and expected outcome labeling in the schema?
- Q2.6 Can you provide examples of future spec revisions support within the schema structure?
- Q2.7 Can you define what annotations (optional, for learning) would look like in this synthetic data schema?
- Q2.8 Can you suggest ways to make each layer independently evolvable in the schema design?
- Q2.9 Can you explain how to represent protocol, electrical, timing, and state context together using JSON format in the schema?

## Q3

Add PD 3.1 / EPR extensions

---

- Q3.1 Can you define the schema extension strategy using optional blocks?
- Q3.2 Can you identify and explain each of the new concepts introduced in PD 3.1 / EPR?
- Q3.3 Can you provide an example of how to declare Source and Sink EPR capabilities?
- Q3.4 Can you detail the agent rule for determining if a cable is EPR certified based on its specifications?
- Q3.5 Can you describe the process for handling protocol messages related to EPR entry?

## Q4

Design an EPR scenario generator

---

- Q4.1 Can you design a schema?
- Q4.2 Can you define what an EPR scenario generator must do?
- Q4.3 Can you outline the high-level architecture of the EPRScenarioGenerator system?
- Q4.4 Can you describe the spec model in detail?
- Q4.5 Can you explain how the spec model works as rules?
- Q4.6 Can you provide an example of the spec model in YAML format?
- Q4.7 Can you discuss each block's functionality within the ScenarioPlanner component?
- Q4.8 Can you elaborate on the TraceSynthesizer components for protocol, electrical, and timing traces?
- Q4.9 Can you describe the role of the Labeler component?
- Q4.10 Can you explain how the DatasetEmitter works with the rest of the system?
- Q4.11 Can you suggest a next step based on these architectural details?
- Q4.12 Can you create a follow-up question about scenario categorization?
- Q4.13 Can you suggest a core scenario class for testing?

## Q5

spec-rule DSL

---

- Q5.1 Can you design a schema?
- Q5.2 Can you define a spec-rule DSL and describe its characteristics and capabilities?
- Q5.3 Can you explain the core design principles of the spec-rule DSL?
- Q5.4 Can you provide an example of a rule's anatomy in the spec-rule DSL?
- Q5.5 Can you write the syntax for the DSL, especially focusing on the cable eligibility rule?
- Q5.6 Can you discuss the timing rules used in the spec-rule DSL and how they are implemented?
- Q5.7 Can you define what the DSL is not or how it differs from other languages or tools?

## Q6

Map DSL rules to USB-IF test cases

---

- Q6.1 Can you explain the importance of turning the DSL from an internal engineering tool into something certification-aware and audit-friendly?
- Q6.2 Can you define a formal grammar for your next step?
- Q6.3 Can you design a schema as mentioned in the response?
- Q6.4 Can you elaborate on how one DSL rule links to USB-IF tests, specifically the mapping model part?
- Q6.5 Can you provide concrete examples of how your DSL works with USB-IF test cases?
- Q6.6 Can you describe how this helps agents, validation, and certification workflows?
- Q6.7 Can you define a formal grammar for the next step?
- Q6.8 Can you explain why this is an intentional and powerful approach when mapping DSL rules to USB-IF test cases?
- Q6.9 Can you provide more details on how extending each DSL rule with a certification mapping block works?
- Q6.10 Can you give examples of the certification mapping blocks you mentioned in your response?
- Q6.11 Can you clarify what specific capability and policy rules are used by the pattern A: Capability & policy rules section?
- Q6.12 Can you describe the advertisement, negotiation acceptance, rejection behavior focus area for the pattern A: Capability & policy rules section?

## Q7

How to connect synthetic data fir real time scenario like having 2 drp connected with emarker cable and communication flow during pr swap and drswap and possible pkt collision if any one drp or eMarker design don't align with spec

---

- Q7.1 Can you explain how synthetic data connects to real-time in a structured manner for the given scenario?
- Q7.2 Can you describe the strategic points at which synthetic data plugs into the real-time flow of your system?
- Q7.3 Can you detail how synthetic scenarios are generated before runtime, including expected message order and silence windows?
- Q7.4 Can you provide an example of collision-free arbitration rules that would be included in a synthetic scenario for this setup?
- Q7.5 Can you create a schema to map synthetic data expectations against the observed real-time behavior of your system?

## Q8

How to find gaps in the pd spec using synthetic data simulation and make chage proposal for spec

---

- Q8.1 Can you generate 'multi-interpretation compliant' actors?
- Q8.2 Can you explain how to convert findings from synthetic simulation into a credible change proposal?
- Q8.3 Can you provide an example of encoding the spec as rules, not prose?
- Q8.4 Can you elaborate on why un-encodable prose indicates spec ambiguity?

## Q9

real PR_SWAP/DR_SWAP ambiguity example as a mock spec gap

---

- (No suggestions found)

