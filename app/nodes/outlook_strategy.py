from ..state import ResearchState, EvidenceItem
from ..tools import tavily_strategy_news_search


async def outlook_strategy_node(state: ResearchState) -> ResearchState:
    company = state.identity_basics.get("name") or ""
    if not company:
        return state

    results = await tavily_strategy_news_search(company)
    for res in results:
        state.outlook_data.append(
            EvidenceItem(
                source="tavily",
                url=res.get("url"),
                snippet=res.get("content") or res.get("raw_content", "")[:800],
                as_of=res.get("published_date"),
                topic="outlook",
            )
        )

    return state
