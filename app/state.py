# app/state.py
from typing import List, Dict, Any, Optional, Annotated
from pydantic import BaseModel, Field


# -------- Reducers for LangGraph concurrent updates --------

def merge_dict(left: Dict[str, Any], right: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dicts, with right-hand side overriding."""
    return {**left, **right}


def extend_list(left: List[Any], right: List[Any]) -> List[Any]:
    """Concatenate lists when multiple nodes append evidence, drafts, etc."""
    return left + right


def choose_str(left: Optional[str], right: Optional[str]) -> Optional[str]:
    """Pick the latest non-empty string."""
    return right or left


# -------------------- Pydantic helper models ----------------

class EvidenceItem(BaseModel):
    source: str
    url: Optional[str] = None
    snippet: str
    as_of: Optional[str] = None
    topic: Optional[str] = None
    score: Optional[float] = None


class SectionDraft(BaseModel):
    title: str
    key: str
    text: str
    confidence: float = 0.0
    caveats: List[str] = Field(default_factory=list)
    evidence_refs: List[int] = Field(default_factory=list)


class DiscrepancyFlag(BaseModel):
    section_key: str
    field: str
    message: str
    severity: str
    sources: List[str] = Field(default_factory=list)


# ------------------------- Graph state -----------------------

class ResearchState(BaseModel):
    # -------- Identity / grounding --------
    # Identity can be enriched by multiple nodes, so use merge_dict
    identity_basics: Annotated[Dict[str, Any], merge_dict] = Field(
        default_factory=dict
    )

    # How detailed the memo should be; several nodes can touch this
    memo_depth: Annotated[str, choose_str] = "standard"

    # Short natural-language description of the company
    ats_description: Annotated[Optional[str], choose_str] = None

    # Nodes may add external identifiers (tickers, LEIs, etc.)
    external_ids: Annotated[Dict[str, Any], merge_dict] = Field(
        default_factory=dict
    )

    # -------- Topic evidence (raw) --------
    fundamentals_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    positioning_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    market_significance_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    leadership_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    founders_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    aum_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    funds_aum_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    public_equity_aum_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    founding_story_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    outlook_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    aspiration_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    future_goals_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    career_growth_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )
    company_culture_data: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )

    # -------- Curation --------
    curated_evidence: Annotated[List[EvidenceItem], extend_list] = Field(
        default_factory=list
    )

    # -------- Drafts / QA / final --------
    drafts: Annotated[Dict[str, SectionDraft], merge_dict] = Field(
        default_factory=dict
    )
    discrepancy_flags: Annotated[List[DiscrepancyFlag], extend_list] = Field(
        default_factory=list
    )
    cleaned_drafts: Annotated[Dict[str, SectionDraft], merge_dict] = Field(
        default_factory=dict
    )

    # Final output + any reusable memory
    final_report_markdown: Optional[str] = None
    key_facts_memory: Annotated[Dict[str, Any], merge_dict] = Field(
        default_factory=dict
    )
