from typing import List, Dict, Tuple

from ..state import ResearchState, SectionDraft, EvidenceItem
from ..llm import generate_section_with_hf


SECTION_SPECS: Dict[str, Dict] = {
    "overview": {
        "title": "Short Overview of the Company",
        "topics": ["fundamentals"],
    },
    "leadership": {
        "title": "Current Partners / Executives",
        "topics": ["leadership", "founders"],
    },
    "financial_capacity": {
        "title": "Financial / Business Capacity (AUM)",
        "topics": ["aum"],
    },
    "founding_story": {
        "title": "Founding Story",
        "topics": ["founding_story", "fundamentals"],
    },
    "business_outlook": {
        "title": "Current Business Outlook",
        "topics": ["outlook", "aspiration"],
    },
    "market_significance": {
        "title": "Significance in the Market",
        "topics": ["market_significance", "positioning"],
    },
    "aspiration": {
        "title": "Aspiration",
        "topics": ["aspiration"],
    },
    "future_goals": {
        "title": "Company Future and Goals",
        "topics": ["future_goals", "outlook"],
    },
    "career_growth": {
        "title": "Professional Career Growth Opportunity",
        "topics": ["career_growth"],
    },
    "culture": {
        "title": "Company Culture",
        "topics": ["company_culture", "culture_careers"],
    },
}


def _build_evidence_context(
    all_evidence: List[EvidenceItem],
    topics: List[str],
    max_items: int = 8,
) -> Tuple[str, List[int]]:
    selected_lines: List[str] = []
    used_indexes: List[int] = []

    for idx, ev in enumerate(all_evidence):
        if topics and ev.topic not in topics:
            continue

        line = (
            f"[{idx}] Source={ev.source}, Topic={ev.topic}, AsOf={ev.as_of}\n"
            f"{ev.snippet.strip()}"
        )
        selected_lines.append(line)
        used_indexes.append(idx)

        if len(selected_lines) >= max_items:
            break

    if not selected_lines:
        return "No direct evidence found for this section.", []

    return "\n\n".join(selected_lines), used_indexes


async def section_writer_node(state: ResearchState) -> ResearchState:
    company_name = state.identity_basics.get("name", "the company")
    website = state.identity_basics.get("website", "N/A")
    industry = state.identity_basics.get("industry", "N/A")
    ats_desc = state.ats_description or "N/A"

    system_prompt = (
        "You are a senior equity research analyst writing memos for a recruiting firm. "
        "Your tone is neutral, factual and concise. "
        "Never invent hard numbers (AUM, years, headcount) if they are not clearly "
        "stated in the evidence. Prefer qualitative wording instead of fabricating numbers."
    )

    for key, spec in SECTION_SPECS.items():
        title = spec["title"]
        topics = spec["topics"]

        context_text, evidence_ids = _build_evidence_context(
            state.curated_evidence,
            topics=topics,
            max_items=8,
        )

        user_prompt = f"""
You are writing ONE section of a company research memo.

Section title: "{title}"

Company identity:
- Name: {company_name}
- Website: {website}
- Industry: {industry}
- Additional description: {ats_desc}

Use ONLY the evidence snippets below. Do not hallucinate facts
that are not supported by the evidence.

Evidence snippets (each has an index in square brackets):

{context_text}

Write 1–3 short paragraphs for this section in clear, recruiter-friendly language.
Do NOT mention the evidence indexes or refer to 'snippets' explicitly.
If evidence is weak or missing, write a cautious, high-level paragraph instead of guessing.
"""

        text = generate_section_with_hf(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=600,
            temperature=0.35,
        )

        state.drafts[key] = SectionDraft(
            title=title,
            key=key,
            text=text.strip(),
            confidence=0.75 if "HF LLM" not in text else 0.2,
            caveats=[],
            evidence_refs=evidence_ids,
        )

    return state
