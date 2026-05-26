"""
Minimal prompts for the deriver module optimized for speed.

This module contains simplified prompt templates focused only on observation extraction.
NO peer card instructions, NO working representation - just extract observations.
"""

from functools import cache
from inspect import cleandoc as c

from src.utils.tokens import estimate_tokens


def minimal_deriver_prompt(
    peer_id: str,
    messages: str,
) -> str:
    """
    Generate minimal prompt for fast observation extraction.

    Args:
        peer_id: The ID of the user being analyzed.
        messages: All messages in the range (interleaving messages and new turns combined).

    Returns:
        Formatted prompt string for observation extraction.
    """
    return c(
        f"""
Analyze messages from {peer_id} to extract **explicit facts** stated directly in their messages.

[EXPLICIT] DEFINITION: Facts that {peer_id} directly states or clearly implies about themselves, their situation, or their preferences. Do NOT infer beyond what is directly supported.

RULES:
- Each fact must be self-contained and useful for understanding {peer_id} in future conversations.
- Use absolute dates/times when possible (e.g. "June 26, 2025" not "yesterday").
- Attribute correctly: if {peer_id} mentions someone or something else, make the subject clear.
- Only extract facts that are durable and likely true beyond this conversation. Skip momentary emotions, transient states, and in-progress actions.
- If a statement is uncertain or qualified ("might", "considering", "thinking about"), frame it as intent: "{peer_id} is considering [X]" — not as established fact.
- Do NOT over-infer. "I walked my dog in NYC" means "{peer_id} has a dog." It does NOT mean "{peer_id} lives in NYC."

EXAMPLES:
- "I just had my 25th birthday last Saturday" → "{peer_id} is 25 years old", "{peer_id}'s birthday is June 21, 2025"
- "I've been at Google for 3 years" → "{peer_id} works at Google (as of June 2025)", "{peer_id} started at Google around mid-2022"
- "I'm thinking about switching to a Mac" → "{peer_id} is considering switching to Mac" (NOT "{peer_id} uses a Mac")
- "My team handles the billing pipeline" → "{peer_id}'s team is responsible for the billing pipeline"

NON-EXAMPLES (do not extract):
- "lol that's hilarious" → no durable fact
- "I'm so tired today" → transient state, skip
- "brb" → no information content

Messages to analyze:
<messages>
{messages}
</messages>
"""
    )


@cache
def estimate_minimal_deriver_prompt_tokens() -> int:
    """Estimate base prompt tokens (cached)."""
    try:
        prompt = minimal_deriver_prompt(
            peer_id="",
            messages="",
        )
        return estimate_tokens(prompt)
    except Exception:
        return 300
