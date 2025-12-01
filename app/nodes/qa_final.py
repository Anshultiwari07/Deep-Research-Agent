from ..state import ResearchState, DiscrepancyFlag


async def qa_final_node(state: ResearchState) -> ResearchState:
    # Simple QA: warn if no AUM evidence
    if not any(ev.topic == "aum" for ev in state.curated_evidence):
        state.discrepancy_flags.append(
            DiscrepancyFlag(
                section_key="financial_capacity",
                field="aum",
                message="No strong AUM evidence found.",
                severity="warning",
                sources=[],
            )
        )

    # For now just copy drafts
    state.cleaned_drafts = dict(state.drafts)

    # Build markdown
    lines = []
    company_name = state.identity_basics.get("name", "Unknown Company")

    lines.append(f"# Company Research Memo: {company_name}\n")

    lines.append("## Identity Basics")
    lines.append(f"- **Website:** {state.identity_basics.get('website', 'N/A')}")
    lines.append(f"- **Industry:** {state.identity_basics.get('industry', 'N/A')}")
    lines.append("")

    for key, draft in state.cleaned_drafts.items():
        lines.append(f"## {draft.title}")
        lines.append(draft.text.strip())
        lines.append("")

    if state.discrepancy_flags:
        lines.append("## QA / Discrepancies")
        for flag in state.discrepancy_flags:
            lines.append(
                f"- **[{flag.severity.upper()}] {flag.field} ({flag.section_key})** – {flag.message}"
            )
        lines.append("")

    state.final_report_markdown = "\n".join(lines)
    return state
