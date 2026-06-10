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
Analyze messages from {peer_id} to extract **explicit durable memory** stated directly in their messages.

[EXPLICIT] DEFINITION: Facts that {peer_id} directly states or clearly implies about themselves, their durable situation, their work, their projects, or their preferences. Do NOT infer beyond what is directly supported.

Memory should help a future assistant across later sessions. It is not a transcript summary, task tracker, todo list, form walkthrough, or record of what the assistant was asked to help with.

RULES:
- Prefer fewer, higher-value facts. If a candidate would not help a future assistant after this session is over, omit it.
- The message block may include multiple speakers. Only extract facts from messages authored by "{peer_id}:". Treat other speakers as context, not evidence about {peer_id}, unless {peer_id} explicitly confirms the fact in their own message.
- Use absolute dates/times when possible (e.g. "June 26, 2025" not "yesterday").
- Attribute correctly: if {peer_id} mentions someone or something else, make the subject clear.
- Extract durable project facts when they describe stable ownership, architecture, permissions, configuration, product behavior, customer expectations, policy constraints, or standing decisions.
- Extract durable user facts when they describe stable roles, skills, access, preferences, communication norms, decision criteria, or recurring constraints.
- Do not store dialogue state: skip facts whose main content is that {peer_id} asked a question, needed help, was unsure, wanted confirmation, was considering options, or was being guided through something.
- Do not store workflow state: skip current tasks, todos, deadlines, UI locations, form sections, review steps, temporary instructions, upload/screencast requirements, and other facts likely to go stale quickly.
- Do not store assistant advice as a fact about {peer_id}. Store it only if {peer_id} later confirms it as a decision, configuration, requirement, or standing preference.
- If a task reveals a durable outcome, store the outcome only after it is stated as true or decided. Skip the temporary process that led there.
- Avoid duplicates: if two candidate facts say the same thing, output the clearest single version.
- Do NOT over-infer. "I walked my dog in NYC" means "{peer_id} has a dog." It does NOT mean "{peer_id} lives in NYC."

EXAMPLES:
- "I just had my 25th birthday last Saturday" → "{peer_id} is 25 years old", "{peer_id}'s birthday is June 21, 2025"
- "I've been at Google for 3 years" → "{peer_id} works at Google (as of June 2025)", "{peer_id} started at Google around mid-2022"
- "My team handles the billing pipeline" → "{peer_id}'s team is responsible for the billing pipeline"
- "I prefer short, high-density answers without long preambles" → "{peer_id} prefers short, high-density answers without long preambles"
- "Our app lets customers connect their own ad accounts and manage campaigns from chat" → "The app lets customers connect their own ad accounts and manage campaigns from chat"
- "We decided the backend will use Postgres for audit logs" → "The backend uses Postgres for audit logs"
- "I have admin access for the production domain" → "{peer_id} has admin access for the production domain"

NON-EXAMPLES (do not extract):
- "lol that's hilarious" → no durable fact
- "I'm so tired today" → transient state, skip
- "Can you help me figure out this form?" → request for help, skip
- "I'm currently on the app review page" → UI/workflow state, skip
- "I need to upload a screencast for this permission" → temporary task/review requirement, skip
- "Maybe we should use a different database" → unresolved option, skip unless later decided
- "The assistant recommended using Provider A" → assistant advice, skip unless {peer_id} accepts it as a decision
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
