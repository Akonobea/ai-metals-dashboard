"""
services/news_service.py — Fetches macro and commodity news headlines.
Uses CryptoCompare's free news API (no key required for basic usage).
"""

import requests
from config import NEWS_API_URL


def get_macro_headlines(limit: int = 6) -> list[str]:
    """
    Fetches latest macro/commodity news headlines.

    Returns:
        List of headline strings, with graceful fallback on failure.
    """
    try:
        resp = requests.get(NEWS_API_URL, timeout=10)
        resp.raise_for_status()
        articles = resp.json().get("Data", [])
        return [a["title"] for a in articles[:limit] if "title" in a] or _fallback()
    except Exception:
        return _fallback()


def _fallback() -> list[str]:
    return [
        "Federal Reserve signals cautious approach to rate adjustments.",
        "USD strengthens amid global risk-off sentiment.",
        "Industrial demand for copper remains resilient in Q1.",
        "Gold holds safe-haven appeal as geopolitical tensions persist.",
        "Silver demand boosted by renewable energy sector growth.",
    ]
