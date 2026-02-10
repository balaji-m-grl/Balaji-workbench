# Question 5

## 👤 User Question

spec-rule DSL

## 🤖 Assistant Answer

Nice choice. A **spec-rule DSL** is the right abstraction layer here — it separates _USB-PD knowledge_ from _code_ and from _models_. I’ll design this as something:

* Domain engineers can read & review
    
* Machines can evaluate deterministically
    
* Agents can reason _with_, not just _over_
    

I’ll keep it **clean, declarative, and evolvable**.

## 1. What the spec-rule DSL is (and is not)

**It is:**

* A declarative language to encode **PD 3.1 / EPR rules**
    
* Deterministic and auditable
    
* Executable by:
    
    * Scenario generator
        
    * Compliance checker
        
    * Labeler
        
    * Agent reasoning layer
        

**It is not:**

* A programming language
    
* A simulator
    
* A textual copy of the USB-IF spec
    

Think of it as **“PD laws in machine-readable form.”**

## 2. Core design principles

1. **Readable like a spec**
    
2. **Structured like a schema**
    
3. **Evaluates to true / false / violation**
    
4. **Explains itself when violated**
    
5. **Composable** (SPR + EPR + future PD 3.2)

## 3. DSL building blocks

### 3.1 Rule anatomy

Every rule has:

```
RULE
├── id
├── scope
├── condition
├── constraint
├── severity
├── violation
└── recommendation
```

## 4. DSL syntax (YAML-like, intentionally)

### 4.1 Cable eligibility for EPR

```yaml
rule:
  id: EPR_CABLE_ELIGIBILITY
  scope: EPR_ENTRY
  condition:
    all:
      - topology.cable.e_marker == true
      - topology.cable.current_capability_a >= 5
      - topology.cable.voltage_rating_v >= 50
  constraint: REQUIRED
  severity: CRITICAL
  violation:
    code: EPR_UNSUPPORTED_CABLE
    message: "Cable does not meet EPR electrical requirements"
  recommendation:
    - "Use 5A, 50V EPR-certified cable"
```

Readable by:

* Engineers
    
* Agents
    
* Compliance tools

## 5. Timing rules (parametric, not hard-coded)

```yaml
rule:
  id: EPR_ENTRY_TIMING
  scope: EPR_MODE_ENTRY
  condition:
    timing.t_epr_entry_ms <= spec.t_epr_entry_max_ms
  severity: HIGH
  violation:
    code: EPR_ENTRY_TIMEOUT
    message: "EPR entry exceeded allowed timing"
  recommendation:
    - "Optimize EPR handshake timing"
```

Spec values come from a **separate constants file**.

## 6. AVS electrical regulation rules

```yaml
rule:
  id: AVS_OVERVOLTAGE_PROTECTION
  scope: EPR_AVS_REGULATION
  condition:
    electrical.epr_vbus.actual_voltage_v
      <= electrical.epr_vbus.requested_voltage_v * 1.05
  severity: CRITICAL
  violation:
    code: EPR_OVERVOLTAGE
    message: "VBUS exceeds AVS safety margin"
  recommendation:
    - "Tighten AVS control loop"
    - "Verify voltage feedback calibration"
```

Key point:

> This rule **binds protocol intent to physics**

## 7. Policy & capability mismatch rules

```yaml
rule:
  id: EPR_SINK_CAPABILITY_LIMIT
  scope: EPR_NEGOTIATION
  condition:
    request.voltage_v <= capabilities.sink.max_voltage_v
  severity: MEDIUM
  violation:
    code: EPR_POLICY_REJECT
    message: "Sink requested voltage beyond declared capability"
  recommendation:
    - "Adjust sink EPR policy"
```

This teaches agents _why_ negotiations fail.

## 8. Stateful rules (this is important)

Some rules depend on **sequence**, not values.

```yaml
rule:
  id: EPR_ENTRY_SEQUENCE
  scope: PROTOCOL_SEQUENCE
  condition:
    sequence.contains_in_order:
      - SOURCE_CAPABILITIES
      - REQUEST
      - ACCEPT
      - EPR_MODE_ENTRY
      - EPR_MODE_ACK
  severity: HIGH
  violation:
    code: EPR_INVALID_SEQUENCE
    message: "EPR handshake sequence violated"
  recommendation:
    - "Fix PD state machine ordering"
```

This is where **agents beat regex log parsers**.

## 9. Safety shutdown rules

```yaml
rule:
  id: EPR_SAFETY_SHUTDOWN
  scope: EPR_RUNTIME
  condition:
    any:
      - electrical.epr_vbus.overshoot_percent > 5
      - electrical.epr_vbus.ripple_mv > spec.avs.max_ripple_mv
  action:
    expect: HARD_RESET
  severity: CRITICAL
  violation:
    code: EPR_SAFETY_NOT_TRIGGERED
    message: "Safety condition violated without shutdown"
```

Now the rule checks **system reaction**, not just fault presence.

## 10. Rule grouping (for agents & tooling)

```yaml
rule_group:
  name: EPR_SAFETY_RULES
  applies_to: PD_3_1
  rules:
    - EPR_CABLE_ELIGIBILITY
    - AVS_OVERVOLTAGE_PROTECTION
    - EPR_SAFETY_SHUTDOWN
```

Agents can reason:

> “This failure is safety-critical, not negotiable.”

## 11. How the DSL is executed

### Evaluation pipeline

```
Scenario JSON
   ↓
Rule Loader
   ↓
Rule Evaluator
   ↓
Violation Set
   ↓
Root Cause Mapper
   ↓
Expected Outcome
```

Each violation carries:

* Rule ID
    
* Severity
    
* Explanation
    
* Recommendation
    

Perfect for **explainable AI**.

## 12. DSL → Agent reasoning bridge

You can feed the agent:

* Violated rule IDs
    
* Natural-language messages
    
* Severity levels
    
* Suggested fixes
    

Instead of raw logs, the agent sees:

> “Rule EPR_CABLE_ELIGIBILITY violated (CRITICAL)”

This massively reduces hallucination risk.

## 13. Extensibility path

Later you can add:

* PD 3.2
    
* Vendor-specific deviations
    
* Certification test mapping
    
* Risk scoring rules
    

Without retraining everything.

### My opinion

This DSL is the **most valuable asset** in the whole system. Models will change. Agents will change. Specs will evolve. But a clean, auditable rule DSL becomes your **institutional PD brain** — readable by humans, enforceable by machines, and teachable to AI.

If you want next, we can:

* Define a **formal grammar (EBNF)**
    
* Design a **fast rule evaluator**
    
* Map DSL rules to **USB-IF test cases**
    
* Or show how to plug this into your **C++ / .NET / agent loop**

## 💡 Recommended Follow-ups

- **Q5.1**: Define a formal grammar (EBNF)
- **Q5.2**: Design a fast rule evaluator
- **Q5.3**: Map DSL rules to USB-IF test cases
- **Q5.4**: Or show how to plug this into your C++ / .NET / agent loop
