"""Triage a folder of .eml emails into a CSV file.

Usage:
    uv run python -m email_triage.cli INBOX_FOLDER OUTPUT_CSV
Example:
    uv run python -m email_triage.cli samples/inbox triage.csv
"""

import csv
import sys
from pathlib import Path

from email_triage.llm import estimate_cost, get_client
from email_triage.reader import read_email
from email_triage.triage import EmailInfo, triage_email

EMAIL_FIELDS = ["file", "sender", "subject", "date"]   # columns from the email itself

def main() -> None:
    # 1. Read the two arguments: input folder and output file.
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    inbox, output = Path(sys.argv[1]), Path(sys.argv[2])

    client = get_client()
    rows = []
    cost = 0.0
    errors = 0

    # 2. Process every email; one bad email must not stop the rest.
    for path in sorted(inbox.glob("*.eml")):
        try:
            email = read_email(path)
            info, usage = triage_email(client, email)
        except Exception as e:
            print(f"{path.name}: skipped ({e})")
            errors += 1
            continue

        cost += estimate_cost(usage)
        rows.append({**{k: email[k] for k in EMAIL_FIELDS}, **info.model_dump()})
        print(f"{path.name}: {info.category} / {info.urgency}")

    # 3. Write all rows to CSV (utf-8-sig so Excel shows Hebrew and Russian correctly).
    with output.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[*EMAIL_FIELDS, *EmailInfo.model_fields])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n{len(rows)} emails saved to {output}, {errors} skipped, cost ${cost:.4f}")


if __name__ == "__main__":
    main()
