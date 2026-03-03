"""
services/indicators.py — Computes momentum, volatility, and trend metrics.
Fully defensive — always returns a complete dict with sensible defaults.
"""

import statistics
import math


_EMPTY = {
    "current_price": 0.0,
    "change_7d":     0.0,
    "change_30d":    0.0,
    "volatility":    0.0,
    "sma_7":         0.0,
    "sma_20":        0.0,
    "trend":         "N/A",
    "period_high":   0.0,
    "period_low":    0.0,
    "pct_from_high": 0.0,
    "pct_from_low":  0.0,
    "history":       [],
}


def compute_metal_metrics(history: list[dict]) -> dict:
    """
    Computes key technical metrics from a price history list.

    Args:
        history: [{"date": str, "price": float}, ...] sorted oldest->newest

    Returns:
        Always returns a complete dict — uses safe defaults if data is thin.
    """
    # Need at least 2 points for any meaningful calculation
    if not history or len(history) < 2:
        return dict(_EMPTY)

    try:
        prices  = [h["price"] for h in history if isinstance(h.get("price"), (int, float))]
        n       = len(prices)

        if n < 2:
            return dict(_EMPTY)

        current = prices[-1]
        oldest  = prices[0]

        # ── Period changes ────────────────────────────────────────────────────
        change_30d = ((current - oldest) / oldest * 100) if oldest else 0.0

        change_7d = 0.0
        if n >= 7:
            base7 = prices[-7]
            change_7d = ((current - base7) / base7 * 100) if base7 else 0.0

        # ── Volatility ────────────────────────────────────────────────────────
        daily_returns = [
            (prices[i] - prices[i - 1]) / prices[i - 1]
            for i in range(1, n)
            if prices[i - 1] != 0
        ]
        vol_daily     = statistics.stdev(daily_returns) if len(daily_returns) > 1 else 0.0
        vol_annualised = vol_daily * math.sqrt(252) * 100

        # ── Moving averages ───────────────────────────────────────────────────
        sma_7  = sum(prices[-min(7,  n):]) / min(7,  n)
        sma_20 = sum(prices[-min(20, n):]) / min(20, n)

        # ── Trend ─────────────────────────────────────────────────────────────
        if   current > sma_20 * 1.005:  trend = "Bullish"
        elif current < sma_20 * 0.995:  trend = "Bearish"
        else:                            trend = "Ranging"

        # ── Range ─────────────────────────────────────────────────────────────
        high = max(prices)
        low  = min(prices)
        pct_from_high = ((current - high) / high * 100) if high else 0.0
        pct_from_low  = ((current - low)  / low  * 100) if low  else 0.0

        return {
            "current_price": round(current,        4),
            "change_7d":     round(change_7d,       2),
            "change_30d":    round(change_30d,      2),
            "volatility":    round(vol_annualised,  2),
            "sma_7":         round(sma_7,           4),
            "sma_20":        round(sma_20,          4),
            "trend":         trend,
            "period_high":   round(high,            4),
            "period_low":    round(low,             4),
            "pct_from_high": round(pct_from_high,   2),
            "pct_from_low":  round(pct_from_low,    2),
            "history":       history,
        }

    except Exception:
        # Last-resort fallback — never crash the pipeline
        result = dict(_EMPTY)
        if history:
            result["current_price"] = history[-1].get("price", 0.0)
            result["history"]       = history
        return result
