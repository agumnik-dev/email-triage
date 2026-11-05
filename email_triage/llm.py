"""Helpers for calling Claude: client creation and cost estimate."""

import os
import sys

import anthropic
from anthropic.types import Usage
from dotenv import load_dotenv

MODEL = "claude-haiku-5-5"

# USD per 1M tokens: (input, output). Check https://claude.com/pricing before use.
PRICES: dict[str, tuple[float, float]] = {
    "claude-haiku-5-5": (0.10, 0.50),
}


def get_client() -> anthropic.Anthropic:
    """Create an API client. Exits with a clear message if the key is missing."""
    load_dotenv()
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY not found. Copy .env.example to .env and add your key.")
    # The SDK retries connection errors, 429 and 5xx automatically.
    return anthropic.Anthropic(max_retries=2, timeout=60.0)


def estimate_cost(usage: Usage, model: str = MODEL) -> float:
    """Return the cost of one API call in USD."""
    price_in, price_out = PRICES[model]
    return (usage.input_tokens * price_in + usage.output_tokens * price_out) / 1_000_000
