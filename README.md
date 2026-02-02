
# Rule-Based Expert System (Forward Chaining)

Rule-Based Expert System

---

## Simple Forward-Chaining Rule Engine

An implementation of a classic **Expert System** using **Forward Chaining** logic.  
This engine accepts a base of facts (symptoms) and infers conclusions based on a predefined ruleset.

---

## How it Works

The engine uses **Forward Chaining**, which starts with known data and moves forward through the rules to see what else can be proven.

---
## Features

-Multi-step Inference: Can chain rules (A -> B, B -> C).
-Reasoning Logs: Prints exactly why a conclusion was reached.
-Easy Rule Definition: Add new rules by simply adding a Rule object to the list.

## How to Run

1. Open terminal in that folder.
2. Run: python expert_system.py
3. Enter facts one by one.
4. Type 'run' to start inference.

The system will:
- Apply forward chaining
- Show reasoning trace
- Display final diagnosis and advice
