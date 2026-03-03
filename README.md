# ⬡ AI Commodity Metals Intelligence Dashboard

A production-grade AI agent for real-time analysis of Gold, Silver, and Copper markets.
Features a luxury editorial UI — dark obsidian theme, Cormorant Garamond serif type,
JetBrains Mono data font, and metallic accent palette.

---

## 📁 Project Structure

```
ai-metals-dashboard/
├── app.py                        # Streamlit UI (premium design)
├── config.py                     # Centralized configuration
├── requirements.txt
├── .env                          # Local API keys (never commit)
├── .streamlit/
│   └── secrets.toml              # Streamlit Cloud secrets
├── agent/
│   ├── __init__.py
│   ├── controller.py             # Orchestration pipeline
│   ├── prompt_builder.py         # Prompt construction
│   └── decision_engine.py        # OpenAI API + JSON parsing
├── services/
│   ├── __init__.py
│   ├── market_data.py            # metals.dev API (prices + history)
│   ├── indicators.py             # Momentum, volatility, SMA, trend
│   └── news_service.py           # Macro news headlines
└── data/
    └── reports_log.json          # Rolling report log
```

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get your free API keys
#    Metals:  https://metals.dev  (free tier: 100 req/month)
#    OpenAI:  https://platform.openai.com/api-keys

# 3. Add keys to .env
#    OPENAI_API_KEY=sk-proj-...
#    METALS_API_KEY=your-key...

# 4. Run
streamlit run app.py
```

---

## ☁️ Streamlit Cloud Deployment

1. Push to GitHub (`.env` and `.streamlit/secrets.toml` are in `.gitignore`)
2. Go to share.streamlit.io → New app → select repo
3. App Settings → Secrets → paste both keys:
   ```toml
   OPENAI_API_KEY = "sk-proj-..."
   METALS_API_KEY = "your-key..."
   ```
4. Deploy

---

## 🤖 AI Agent Output

```json
{
  "metals": {
    "Gold":   { "bias": "Bullish",  "confidence": 78, "summary": "..." },
    "Silver": { "bias": "Neutral",  "confidence": 55, "summary": "..." },
    "Copper": { "bias": "Bearish",  "confidence": 62, "summary": "..." }
  },
  "risk_level": "Medium",
  "macro_drivers": ["USD weakness", "Inflation expectations", "..."],
  "cross_metal_insight": "Gold/Silver ratio at 85x suggests...",
  "outlook": "Precious metals remain supported by...",
  "key_risks": ["Fed hawkish pivot", "China demand slowdown"]
}
```

---

## ⚠️ Disclaimer
For educational and research purposes only. Not financial advice.
