"""
agent/prompt_builder.py — System and user prompts for the metals AI agent.
"""

SYSTEM_PROMPT = """You are a senior commodity markets analyst at a global investment bank,
specializing in precious and industrial metals. Your expertise spans macroeconomic analysis,
technical price action, and cross-commodity correlations.

Rules:
- Be precise, authoritative, and data-driven.
- Reference specific numbers from the provided data.
- Return ONLY a valid JSON object — no markdown, no prose outside JSON.
- Each metal must have exactly one of: "Bullish", "Bearish", or "Neutral" as its bias.
- confidence must be an integer 0–100 per metal.
- risk_level must be exactly "Low", "Medium", or "High".
- macro_drivers: list of 3–4 concise macro factors currently driving metals.
- cross_metal_insight: 2–3 sentences on relationships between the metals (e.g. gold/silver ratio, copper as economic barometer).
- outlook: 2–3 sentence forward-looking narrative.
- key_risks: list of 2–3 tail risk factors.

Required JSON schema:
{
  "metals": {
    "Gold":   { "bias": "<Bullish|Bearish|Neutral>", "confidence": <0-100>, "summary": "<1 sentence>" },
    "Silver": { "bias": "<Bullish|Bearish|Neutral>", "confidence": <0-100>, "summary": "<1 sentence>" },
    "Copper": { "bias": "<Bullish|Bearish|Neutral>", "confidence": <0-100>, "summary": "<1 sentence>" }
  },
  "risk_level": "<Low|Medium|High>",
  "macro_drivers": ["<driver1>", "<driver2>", "<driver3>"],
  "cross_metal_insight": "<2-3 sentences>",
  "outlook": "<2-3 sentences>",
  "key_risks": ["<risk1>", "<risk2>"]
}"""


def build_user_prompt(metrics: dict, headlines: list[str]) -> str:
    """
    Builds the structured user prompt from metals metrics and news.

    Args:
        metrics:   {metal_name: computed_metrics_dict}
        headlines: list of macro news headline strings

    Returns:
        Formatted prompt string.
    """
    lines = []
    for metal, m in metrics.items():
        gs_ratio = metrics.get("_gold_silver_ratio", "N/A")
        lines.append(f"""
## {metal}
- Current Price:    ${m['current_price']:,.4f} / troy oz
- 7-Day Change:     {m['change_7d']:+.2f}%
- 30-Day Change:    {m['change_30d']:+.2f}%
- Annualised Vol:   {m['volatility']}%
- SMA-7:            ${m['sma_7']:,.4f}
- SMA-20:           ${m['sma_20']:,.4f}
- Trend:            {m['trend']}
- 30-Day High:      ${m['period_high']:,.4f}  ({m['pct_from_high']:+.2f}% from current)
- 30-Day Low:       ${m['period_low']:,.4f}  ({m['pct_from_low']:+.2f}% from current)""")

    # Gold/Silver ratio
    if "Gold" in metrics and "Silver" in metrics:
        ratio = metrics["Gold"]["current_price"] / metrics["Silver"]["current_price"]
        lines.append(f"\n## Cross-Metal\n- Gold/Silver Ratio: {ratio:.2f}")

    news_text = "\n".join(f"  - {h}" for h in headlines)

    return (
        "Analyze the following commodity metals data and return your structured JSON report.\n"
        + "\n".join(lines)
        + f"\n\n## Macro News Headlines\n{news_text}\n\n"
        + "Provide your structured JSON analysis now."
    )
