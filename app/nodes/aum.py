from ..state import ResearchState, EvidenceItem
from ..tools import tavily_aum_search, with_manager_aums_tool


async def aum_node(state: ResearchState) -> ResearchState:
    company = state.identity_basics.get("name") or ""
    if not company:
        return state

    # Web-based AUM hints
    results = await tavily_aum_search(company)
    for res in results:
        state.aum_data.append(
            EvidenceItem(
                source="tavily",
                url=res.get("url"),
                snippet=res.get("content") or res.get("raw_content", "")[:800],
                as_of=res.get("published_date"),
                topic="aum",
            )
        )

    # With Intelligence AUM (future: when external_ids["with_manager_id"] exists)
    manager_id = state.external_ids.get("with_manager_id")
    if manager_id:
        aums = await with_manager_aums_tool(manager_id)
        for rec in aums:
            state.aum_data.append(
                EvidenceItem(
                    source="with_intelligence",
                    url=None,
                    snippet=str(rec),
                    as_of=str(rec.get("as_of") or rec.get("asOf")),
                    topic="aum",
                )
            )

    return state
