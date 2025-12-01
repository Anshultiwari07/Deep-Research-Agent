from typing import Set
from ..state import ResearchState, EvidenceItem


async def curation_node(state: ResearchState) -> ResearchState:
    seen: Set[str] = set()

    def add_unique(items):
        for ev in items:
            key = ev.url or ev.snippet[:80]
            if key in seen:
                continue
            seen.add(key)
            state.curated_evidence.append(ev)

    add_unique(state.fundamentals_data)
    add_unique(state.positioning_data)
    add_unique(state.leadership_data)
    add_unique(state.aum_data)
    add_unique(state.founding_story_data)
    add_unique(state.outlook_data)
    add_unique(state.career_growth_data)
    add_unique(state.company_culture_data)

    return state
