import os
from typing import List, Dict, Any

import httpx
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
FMP_API_KEY = os.getenv("FMP_API_KEY")
WITH_API_KEY = os.getenv("WITH_API_KEY")


# ------------- Tavily search helpers -------------


async def _tavily_search(query: str, topic: str, max_results: int = 8) -> List[Dict[str, Any]]:
    """
    Generic Tavily search wrapper.
    Returns a list of dicts with url/content/etc.
    """
    if not TAVILY_API_KEY:
        return []

    url = "https://api.tavily.com/search"
    payload = {
        "query": query,
        "topic": topic,
        "max_results": max_results,
        "search_depth": "advanced",
        "include_raw_content": "text",
    }
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json().get("results", [])


async def tavily_overview_search(company_name: str):
    return await _tavily_search(f"{company_name} overview asset manager", "general")


async def tavily_leadership_search(company_name: str):
    return await _tavily_search(f"{company_name} leadership partners founders", "general")


async def tavily_aum_search(company_name: str):
    return await _tavily_search(f"{company_name} assets under management AUM", "finance")


async def tavily_strategy_news_search(company_name: str):
    return await _tavily_search(f"{company_name} strategy outlook expansion", "news")


async def tavily_culture_reviews_search(company_name: str):
    return await _tavily_search(f"{company_name} culture careers reviews glassdoor", "general")


# ------------- With Intelligence stubs (safe no-op) -------------


async def with_manager_aums_tool(manager_id: int) -> List[Dict[str, Any]]:
    """
    Stub for With Intelligence manager AUM lookup.

    We return an empty list for now so the app runs even if
    you don't have With Intelligence wired up yet.
    """
    return []


async def with_search_firms_tool(company_name: str) -> Dict[str, Any]:
    """
    Stub for With Intelligence firm search.
    """
    return {}


# ------------- FMP stub (optional) -------------


async def fmp_company_profile_tool(symbol: str) -> Dict[str, Any]:
    """
    Stub for Financial Modeling Prep company profile.
    We currently don't use this deeply, so it's safe to return {}.
    """
    if not FMP_API_KEY:
        return {}
    # You can fill this in later if you want real stock profiles.
    return {}
