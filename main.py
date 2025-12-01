# main.py
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.graph import build_graph
from app.state import ResearchState

app = FastAPI(title="Deep Research Agent")

# --- CORS so the frontend (localhost:5173) can call the API ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compile the LangGraph graph once at startup
graph_app = build_graph()


class ResearchRequest(BaseModel):
    # Public inputs for your open company research agent
    company_name: str
    website: Optional[str] = None
    industry: Optional[str] = None

    # How detailed the memo should be
    memo_depth: str = "standard"  # e.g. "brief" | "detailed" | custom length tags


class ResearchResponse(BaseModel):
    memo_depth: str
    final_report_markdown: str


@app.get("/")
async def root():
    return {"message": "Deep Research Agent is running. Go to /docs for API UI."}


@app.post("/research", response_model=ResearchResponse)
async def run_research(req: ResearchRequest):
    # Build initial graph state – inject identity_basics directly
    initial_state = ResearchState(
        identity_basics={
            "name": req.company_name,
            "website": req.website or "N/A",
            "industry": req.industry or "N/A",
        },
        memo_depth=req.memo_depth,
        ats_description="User-provided identity; no ATS/Bullhorn used.",
    )

    try:
        # LangGraph usually gives back a plain dict, not a ResearchState instance
        final_state = await graph_app.ainvoke(initial_state)

        # Normalize to a dict so we can safely access fields
        if isinstance(final_state, ResearchState):
            final_state_dict = final_state.model_dump()
        elif isinstance(final_state, dict):
            final_state_dict = final_state
        else:
            raise TypeError(
                f"Unexpected graph result type: {type(final_state).__name__}"
            )

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {e}",
        )

    # Pull the markdown out of the dict (default to empty string)
    markdown = final_state_dict.get("final_report_markdown") or ""

    return ResearchResponse(
        memo_depth=req.memo_depth,
        final_report_markdown=markdown,
    )
