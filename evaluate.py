"""Check triage quality on the sample emails.

Runs triage on every email in samples/inbox and compares the result
with the correct answers in samples/expected.json.

Run from the project root:
    uv run python evaluate.py
"""

import json
from pathlib import Path

from email_triage.llm import estimate_cost, get_client
from email_triage.reader import read_email
from email_triage.triage import triage_email

SAMPLES = Path(__file__).parent / "samples"


def main() -> None:
    client = get_client()
    expected = json.loads((SAMPLES / "expected.json").read_text(encoding="utf-8"))

    fields = ["category", "urgency", "policy_number"]
    correct = {field: 0 for field in fields}
    cost = 0.0

    for path in sorted((SAMPLES / "inbox").glob("*.eml")):
        email = read_email(path)
        info, usage = triage_email(client, email)
        cost += estimate_cost(usage)

        right = expected[path.name]
        ok = {field: getattr(info, field) == right[field] for field in fields}
        for field in fields:
            correct[field] += ok[field]

        mark = "✓" if all(ok.values()) else "✗"
        print(f"{path.name}  {info.category:<14}{info.urgency:<8}{str(info.policy_number):<10}{mark}")

    total = len(expected)
    print("  ".join(f"{field} {correct[field]}/{total}" for field in fields))
    print(f"cost: ${cost:.4f}")


if __name__ == "__main__":
    main()
