"""
AI fallback layer.

If a medicine or a medicine-pair interaction isn't found in the local
SQLite database, we ask Claude to generate a structured, best-effort
answer. This is clearly labeled in the UI as AI-generated (not a
verified medical source) and is saved back to the database (source="ai")
so the same question doesn't need to hit the API twice.

Requires the ANTHROPIC_API_KEY environment variable to be set.
If it isn't set, callers should treat the AI layer as unavailable
and show a "no data available, consult a professional" message instead.
"""
import json
import os

import anthropic

MODEL = "claude-sonnet-4-6"


def _client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


def ai_available():
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def _extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def generate_medicine_info(name):
    """Ask Claude for what a medicine is used for + its side effects."""
    client = _client()
    if client is None:
        return None

    system = (
        "You are a careful medical-information assistant embedded in a demo app. "
        "Given a medicine name, respond ONLY with a JSON object (no markdown, no preamble) "
        "with exactly these keys: "
        '"category" (short string), "used_for" (2-3 sentences), '
        '"common_side_effects" (comma-separated list), '
        '"serious_side_effects" (comma-separated list of effects needing urgent care), '
        '"requires_prescription" (true/false). '
        "If the name is not a recognizable medicine, set used_for to "
        '"Not recognized as a known medicine name." and leave the other text fields empty, '
        "requires_prescription false."
    )

    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=600,
            system=system,
            messages=[{"role": "user", "content": f"Medicine name: {name}"}],
        )
        text = "".join(b.text for b in resp.content if b.type == "text")
        return _extract_json(text)
    except Exception:
        return None


def generate_interaction_info(name1, name2):
    """Ask Claude what happens if two medicines are taken together."""
    client = _client()
    if client is None:
        return None

    system = (
        "You are a careful medical-information assistant embedded in a demo app. "
        "Given two medicine names, respond ONLY with a JSON object (no markdown, no preamble) "
        "with exactly these keys: "
        '"severity" (one of "safe", "caution", "avoid"), '
        '"combined_effects" (2-3 sentences on what happens if both are taken together), '
        '"explanation" (2-3 sentences on the pharmacological reason why), '
        '"advice" (2-3 sentences of practical, cautious advice — always include a recommendation '
        "to consult a doctor or pharmacist before combining medicines, especially for anything "
        'above "safe"). '
        "Be conservative: if you are not confident, use severity \"caution\" rather than \"safe\"."
    )

    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=700,
            system=system,
            messages=[{"role": "user", "content": f"Medicine 1: {name1}\nMedicine 2: {name2}"}],
        )
        text = "".join(b.text for b in resp.content if b.type == "text")
        return _extract_json(text)
    except Exception:
        return None
