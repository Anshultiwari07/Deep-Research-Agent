# app/nodes/planner.py
from ..state import ResearchState


async def planner_node(state: ResearchState) -> ResearchState:
    """
    Initialize or normalize identity_basics using what we already have.
    No Bullhorn / ATS / employee-id logic.
    """

    # What we got from the API (set in main.py)
    basics = dict(state.identity_basics) if state.identity_basics else {}

    name = basics.get("name") or "Unknown Company"
    website = basics.get("website") or "N/A"
    industry = basics.get("industry") or "N/A"

    # Normalize and enrich identity_basics
    state.identity_basics = {
        **basics,
        "name": name,
        "website": website,
        "industry": industry,
    }

    # Simple description other nodes can reuse
    state.ats_description = (
        f"{name} is a company in the {industry} sector. "
        f"Website: {website}."
    )

    return state
