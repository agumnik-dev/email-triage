from email import policy
from email.parser import BytesParser
from pathlib import Path


def read_email(path: Path) -> dict:
    """Read one .eml file and return its main parts as a dict."""
    with open(path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    body_part = msg.get_body(preferencelist=("plain",))
    body = body_part.get_content() if body_part else ""   # some emails have no plain text

    return {
        "file": path.name,
        "sender": str(msg["From"]),
        "subject": str(msg["Subject"]),
        "date": str(msg["Date"]),
        "body": body,
    }
