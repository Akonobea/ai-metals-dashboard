"""
config.py — Centralized configuration for the AI Commodity Metals Dashboard.
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except ImportError:
    pass


def get_openai_key() -> str:
    key = os.getenv("OPENAI_API_KEY", "")
    if key:
        return key
    try:
        import streamlit as st
        key = st.secrets.get("OPENAI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    raise ValueError(
        "OPENAI_API_KEY not found.\n"
        "Local:  add to .env  ->  OPENAI_API_KEY=sk-...\n"
        "Cloud:  Streamlit Cloud -> App Settings -> Secrets"
    )


def get_metals_key() -> str:
    key = os.getenv("METALS_API_KEY", "")
    if key:
        return key
    try:
        import streamlit as st
        key = st.secrets.get("METALS_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    raise ValueError(
        "METALS_API_KEY not found.\n"
        "Get a free key at https://metals.dev\n"
        "Local:  add to .env  ->  METALS_API_KEY=your-key\n"
        "Cloud:  Streamlit Cloud -> App Settings -> Secrets"
    )


# ── Metals ────────────────────────────────────────────────────────────────────
METALS = {
    "Gold":   {"symbol": "XAU", "unit": "troy oz", "emoji": "🥇", "color": "#D4AF37"},
    "Silver": {"symbol": "XAG", "unit": "troy oz", "emoji": "🥈", "color": "#C0C0C0"},
    "Copper": {"symbol": "XCU", "unit": "lb",      "emoji": "🟤", "color": "#B87333"},
}

# ── API endpoints ─────────────────────────────────────────────────────────────
METALS_API_BASE    = "https://api.metals.dev/v1"
NEWS_API_URL       = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN&categories=Commodity,Macro,Gold,Silver&sortOrder=latest"

# ── LLM ───────────────────────────────────────────────────────────────────────
LLM_MODEL       = "gpt-4o-mini"
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS  = 900

# ── Logging ───────────────────────────────────────────────────────────────────
REPORTS_LOG_PATH = "data/reports_log.json"
MAX_LOG_ENTRIES  = 50
