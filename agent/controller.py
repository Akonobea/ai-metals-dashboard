"""
agent/controller.py — Orchestrates the full metals intelligence pipeline.

Handles None prices from the API gracefully — a metal with no live price
still goes through the pipeline using its history-derived current price.
"""

import json
import os
from datetime import datetime, timezone

from config import METALS, REPORTS_LOG_PATH, MAX_LOG_ENTRIES
from services.market_data import get_live_prices, get_price_history
from services.indicators import compute_metal_metrics
from services.news_service import get_macro_headlines
from agent.prompt_builder import build_user_prompt
from agent.decision_engine import get_ai_report


def run_analysis() -> dict:
    """
    Runs the full commodity metals intelligence pipeline.
    Resilient to partial API failures — if one metal's live price is null,
    the others still proceed normally.
    """
    # Step 1 — Live prices (may contain None for individual metals)
    live_prices = get_live_prices()

    # Step 2 & 3 — History + metrics per metal
    metrics = {}
    for metal in METALS:
        history = get_price_history(metal, days=30)
        m = compute_metal_metrics(history)

        live_price = live_prices.get(metal)   # could be None

        if live_price is not None:
            # Override the history-derived price with the fresher live price
            m["current_price"] = live_price
        elif m.get("current_price", 0) == 0:
            # Both live and history failed — mark clearly
            m["current_price"] = None
            m["data_unavailable"] = True

        metrics[metal] = m

    # Step 4 — News
    headlines = get_macro_headlines()

    # Step 5 — Prompt (only include metals with valid data)
    user_prompt = build_user_prompt(metrics, headlines)

    # Step 6 — AI report
    ai_report = get_ai_report(user_prompt)

    result = {
        "timestamp":   datetime.now(timezone.utc).isoformat(),
        "live_prices": {k: v for k, v in live_prices.items()},  # keep Nones for logging
        "metrics":     metrics,
        "headlines":   headlines,
        "ai_report":   ai_report,
    }

    _log_report(result)
    return result


def _log_report(result: dict) -> None:
    os.makedirs(os.path.dirname(REPORTS_LOG_PATH), exist_ok=True)
    log = []
    if os.path.exists(REPORTS_LOG_PATH):
        try:
            with open(REPORTS_LOG_PATH) as f:
                log = json.load(f)
        except (json.JSONDecodeError, IOError):
            log = []
    log.append(result)
    log = log[-MAX_LOG_ENTRIES:]
    with open(REPORTS_LOG_PATH, "w") as f:
        json.dump(log, f, indent=2, default=str)


def load_recent_reports(n: int = 5) -> list[dict]:
    if not os.path.exists(REPORTS_LOG_PATH):
        return []
    try:
        with open(REPORTS_LOG_PATH) as f:
            log = json.load(f)
        return log[-n:][::-1]
    except (json.JSONDecodeError, IOError):
        return []
