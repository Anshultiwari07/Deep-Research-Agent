from ..state import ResearchState, EvidenceItem
from ..tools import tavily_overview_search, tavily_strategy_news_search


async def fundamentals_node(state: ResearchState) -> ResearchState:
    company = state.identity_basics.get("name") or ""
    if not company:
        return state

    overview_results = await tavily_overview_search(company)
    strategy_results = await tavily_strategy_news_search(company)

    for res in overview_results:
        state.fundamentals_data.append(
            EvidenceItem(
                source="tavily",
                url=res.get("url"),
                snippet=res.get("content") or res.get("raw_content", "")[:800],
                as_of=res.get("published_date"),
                topic="fundamentals",
            )
        )

    for res in strategy_results:
        state.positioning_data.append(
            EvidenceItem(
                source="tavily",
                url=res.get("url"),
                snippet=res.get("content") or res.get("raw_content", "")[:800],
                as_of=res.get("published_date"),
                topic="market_positioning",
            )
        )

    return state
