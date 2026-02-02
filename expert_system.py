
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple


class ForwardChainer:
    def __init__(self, rules: List[Dict]):
        self.rules = rules
        self.known: Set[str] = set()
        self.trace: List[str] = []
        self.used: Set[str] = set()

    def add(self, fact: str) -> None:
        f = fact.strip().lower()
        if f:
            self.known.add(f)

    def run(self) -> None:
        changed = True
        while changed:
            changed = False

            for r in self.rules:
                rid = r["id"]
                conditions = set(x.lower() for x in r["if_all"])
                conclusion = r["then"].lower()

                if rid in self.used:
                    continue

                if conditions.issubset(self.known):
                    self.used.add(rid)

                    if conclusion not in self.known:
                        self.known.add(conclusion)
                        changed = True

                        self.trace.append(
                            f"[{rid}] IF {sorted(conditions)} THEN '{conclusion}' | {r.get('note','')}"
                        )


def prompt_user_facts() -> Set[str]:
    print("\n=== Rule-Based Expert System (Forward Chaining) ===")
    print("Enter facts/symptoms one by one.")
    print("Type 'run' to start inference.\n")

    facts = set()
    while True:
        s = input("Fact> ").strip().lower()
        if s == "run":
            return facts
        if s:
            facts.add(s)


def extract_results(facts: Set[str]) -> Tuple[List[str], List[str]]:
    diagnoses = sorted([f for f in facts if f.startswith("diagnosis:")])
    advice = sorted([f for f in facts if f.startswith("advice:")])
    return diagnoses, advice


def main():
    rules_path = Path("rules.json")
    if not rules_path.exists():
        print("ERROR: rules.json not found in the same folder.")
        return

    rules = json.loads(rules_path.read_text(encoding="utf-8"))

    engine = ForwardChainer(rules)

    user_facts = prompt_user_facts()
    for f in user_facts:
        engine.add(f)

    engine.run()

    print("\n--- TRACE (Reasoning Log) ---")
    if engine.trace:
        for i, line in enumerate(engine.trace, 1):
            print(f"{i}. {line}")
    else:
        print("No rule fired (not enough matching facts).")

    print("\n--- FINAL FACTS ---")
    for f in sorted(engine.known):
        print("-", f)

    diagnoses, advice = extract_results(engine.known)

    print("\n--- CONCLUSION ---")
    if diagnoses:
        print("Diagnosis:")
        for d in diagnoses:
            print("•", d.replace("diagnosis:", "").strip())
    else:
        print("Diagnosis: (none inferred)")

    if advice:
        print("\nAdvice:")
        for a in advice:
            print("•", a.replace("advice:", "").strip())
    else:
        print("\nAdvice: (none inferred)")


if __name__ == "__main__":
    main()
