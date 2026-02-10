# Suggested / Follow-up Questions Only

## Q1

Wat is Synthetic data in model training,
Explain with USB pd domain agent model training example

---

- Q1.1 Can you define synthetic data and its characteristics of being domain-faithful, statistically realistic, and behaviorally meaningful for a model's learning task?
- Q1.2 Can you explain how synthetic data solves issues with limited, expensive, or proprietary real data in USB-PD engineering domains?
- Q1.3 Can you elaborate on the types of training data specific to a USB-PD agent model, including protocol message sequences, state machine transitions, electrical measurements, timing constraints, and error cases?
- Q1.4 Can you provide an example of synthetic protocol traces for a USB-PD model training, detailing how they can include valid and invalid PD message sequences programmatically generated?
- Q1.5 Can you discuss the challenges in capturing certain variations of synthetic protocol traces, such as missing `Accept`, delayed `PS_RDY`, requesting unsupported PDOs, repeated Source_Capabilities, and protocol version mismatches, which are difficult to reproduce with real data?
- Q1.6 Can you suggest a next step for generating more comprehensive synthetic data sets that cover all combinations relevant to USB-PD agent model training?

## Q2

Design a USB-PD synthetic data schema

---

- Q2.1 Can you define the structure of your synthetic USB-PD schema?
- Q2.2 Can you design a schema that aligns with the specified intents for protocol, electrical, timing, and state context?
- Q2.3 Can you ensure the schema supports fault injection and outcome labeling?
- Q2.4 Can you incorporate the layers: Metadata, Topology, Policy & Capabilities, Protocol_Trace, Electrical_Trace, Timing_Profile, Fault_Injection, State_Transitions, Expected_Outcome?
- Q2.5 Can you consider each layer's independence for evolution in your synthetic USB-PD schema design?
- Q2.6 Can you provide an example of a metadata entry that includes versioning and generation details?
- Q2.7 Can you illustrate how the topology section would look with AC-DC adapter as source, mobile device as sink, and specified current capability and length?
- Q2.8 Can you elaborate on why policy & capabilities are essential for your synthetic USB-PD schema design?

## Q3

Add PD 3.1 / EPR extensions

---

- Q3.1 Can you define a schema extension strategy that includes optional blocks?
- Q3.2 Can you describe the new components added in PD 3.1 / EPR as per the schema perspective?
- Q3.3 Can you explain how to declare Source and sink EPR capabilities using JSON format?
- Q3.4 Can you provide the agent rule for validating EPR messages based on cable extensions?
- Q3.5 Can you suggest a method to handle invalid EPR reasoning within the schema?
- Q3.6 Can you rephrase why it is important to prevent invalid EPR reasoning in the schema?
- Q3.7 Can you list out all the new concepts introduced by PD 3.1 / EPR and their implications on the schema?
- Q3.8 Can you describe how to extend the schema without breaking compatibility with legacy PD agents?
- Q3.9 Can you create a JSON format for declaring Source and sink EPR capabilities in the schema?
- Q3.10 Can you provide an example of what the 'epr_capabilities' object should look like within a JSON file?
- Q3.11 Can you detail the process of defining the cable extensions necessary for PD 3.1 within the schema?
- Q3.12 Can you explain how to validate EPR messages based on the presence of specific components, such as voltage rating and e-marker?
- Q3.13 Can you outline the process of adding new capabilities like 'epr_supported' in the schema documentation?
- Q3.14 Can you provide examples or explanations for why EPR-specific fault classes are necessary within the schema?
- Q3.15 Can you describe how to handle expected outcome validation related to EPR compliance within the schema?

## Q4

Design an EPR scenario generator

---

- Q4.1 Can you design a schema?
- Q4.2 Can you define what an EPR scenario generator must do?
- Q4.3 Can you explain the high-level architecture of the EPRScenarioGenerator system?
- Q4.4 Can you describe the SpecModel and how it works?
- Q4.5 Can you provide an example of the spec model rules in YAML format?
- Q4.6 Can you elaborate on the ScenarioPlanner components within the EPRScenarioGenerator system?
- Q4.7 Can you detail the TraceSynthesizer steps used to generate protocol, electrical, and timing profiles?
- Q4.8 Can you discuss the Labeler component's functions for compliance checking and root cause mapping?
- Q4.9 Can you describe how each block in the dataset emitter is independently testable?
- Q4.10 Can you categorize every scenario within the EPRScenarioGenerator system?
- Q4.11 Can you explain what Core scenario classes are and provide examples?
- Q4.12 Can you suggest any follow-up actions or next steps?

## Q5

spec-rule DSL

---

- Q5.1 Can you define what the spec-rule DSL is for encoding PD 3.1 / EPR rules?
- Q5.2 Can you ensure that the DSL design is clean, declarative, and evolvable as described?
- Q5.3 Can you describe the core design principles of the spec-rule DSL?
- Q5.4 Can you explain how the spec-rule DSL is readable like a specification?
- Q5.5 Can you clarify if the spec-rule DSL evaluates to true / false / violation?
- Q5.6 Can you specify which rules are composed using the spec-rule DSL and future PD 3.2?
- Q5.7 Can you detail the anatomy of each rule in the spec-rule DSL syntax?
- Q5.8 Can you provide an example of how a cable eligibility rule is defined in the spec-rule DSL syntax?
- Q5.9 Can you discuss how timing rules work within the spec-rule DSL and their parametric nature?
- Q5.10 Can you ask who can read and use the spec-rule DSL, including engineers and compliance tools?

## Q6

Map DSL rules to USB-IF test cases

---

- Q6.1 Can you explain the mapping from your DSL to USB-IF test cases?
- Q6.2 Can you describe how one DSL rule can map to multiple USB-IF test cases and vice versa?
- Q6.3 Can you provide an example of extending a DSL rule with a certification mapping block as shown in the YAML code snippet?
- Q6.4 Can you give me examples of how you would apply pattern A: Capability & policy rules to your DSL for EPR mode entry validation?
- Q6.5 Can you elaborate on the 'many-to-many' relationship between DSL rules and USB-IF test cases mentioned earlier?
- Q6.6 Can you design a schema that can represent both the DSL and the mappings to USB-IF test cases in a clear and understandable way?
- Q6.7 Can you create a step-by-step guide on how to design schemas for your DSL to ensure it is certification-aware and audit-friendly?

## Q7

How to connect synthetic data fir real time scenario like having 2 drp connected with emarker cable and communication flow during pr swap and drswap and possible pkt collision if any one drp or eMarker design don't align with spec

---

- Q7.1 Can you explain the connection between synthetic data and real-time operation in a parallel universe approach?
- Q7.2 Can you design a schema to map synthetic scenarios before runtime based on your example of cable traffic competition for CC line attention?
- Q7.3 Can you outline how synthetic data detects deviations from expected behavior during runtime using your scenario of eMarker traffic competing for CC line attention?
- Q7.4 Can you provide the code or structure for generating synthetic scenarios in C++ and .NET as an agent stack, similar to what you described for PD stack logic?
- Q7.5 Can you create a flowchart showing how synthetic data explains root cause analysis using spec rules after runtime failures occur, based on your explanation of three strategic points of connection?
- Q7.6 Can you explain the role that eMarker plays in the topology between DRP_A and DRP_B during PR_SWAP and DR_SWAP operations?
- Q7.7 Can you describe the layers of structure needed to map synthetic data’s connections to your existing C++ streamer + .NET analyzer + agent stack technology?
- Q7.8 Can you provide examples or a template for the expected message order, expected silence windows, timing tolerances, and collision-free arbitration rules used in synthetic scenarios?

## Q8

How to find gaps in the pd spec using synthetic data simulation and make chage proposal for spec

---

- (No suggestions found)

## Q9

real PR_SWAP/DR_SWAP ambiguity example as a mock spec gap

---

- (No suggestions found)

