from ..state import ResearchState, EvidenceItem
from ..tools import tavily_culture_reviews_search


async def culture_careers_node(state: ResearchState) -> ResearchState:
    company = state.identity_basics.get("name") or ""
    if not company:
        return state

    results = await tavily_culture_reviews_search(company)
    for res in results:
        state.company_culture_data.append(
            EvidenceItem(
                source="tavily",
                url=res.get("url"),
                snippet=res.get("content") or res.get("raw_content", "")[:800],
                as_of=res.get("published_date"),
                topic="culture_careers",
            )
        )

    return state
