from pathlib import Path
from email_triage.reader import read_email
from email_triage.llm import get_client
from email_triage.triage import triage_email

# for path in sorted(Path("samples/inbox").glob("*.eml")):    # every .eml file in the folder, in order
#     email = read_email(path)
#     print(email["file"], "|", email["sender"], "|", email["subject"])

client = get_client()
email = read_email(Path("samples/inbox/18.eml"))
info, usage = triage_email(client, email)
print(info)
