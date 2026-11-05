# Email Triage

AI triage for an insurance company inbox. Reads a folder of `.eml` emails
(Hebrew, Russian, English) and produces a CSV for the support team:
category, urgency, policy number, language and a one-line summary.

## What it does
- Classifies each email into 8 business categories and 2 urgency levels
- Extracts the policy number, ignoring claim numbers
- Applies business rules in code (a driver under 21 means high urgency)
- Ignores instructions hidden inside emails (prompt injection)
- Skips a broken email instead of stopping the whole run

## How it works
`.eml` → `reader.py` (decode headers and body) → `triage.py` (Claude fills a
Pydantic schema via structured outputs) → `cli.py` (CSV for Excel)

## Run
    cp .env.example .env    # add your Anthropic API key
    uv sync
    uv run python -m email_triage.cli samples/inbox triage.csv

## Quality
On 18 test emails (`samples/`): category 18/18, urgency 18/18, policy number 18/18.
Check with `uv run python evaluate.py`. Cost of a full run: about $0.004.

## Stack
Python, Anthropic API (Claude Haiku 5.5, structured outputs), Pydantic