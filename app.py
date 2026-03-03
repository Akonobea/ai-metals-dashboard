"""
app.py — AI Commodity Metals Intelligence Dashboard
Aesthetic: Luxury editorial meets trading terminal.
Dark obsidian base · warm gold/copper accent palette · bold serif display · monospaced data.
"""

import streamlit as st
import pandas as pd
from agent.controller import run_analysis, load_recent_reports
from config import METALS

st.set_page_config(
    page_title="Metals Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────── GLOBAL CSS ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;0,900;1,700;1,800&family=JetBrains+Mono:wght@400;500;700&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    background-color: #08080A !important;
    color: #EDE5D5 !important;
    font-family: 'Cormorant Garamond', serif !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 2.5rem 3.5rem 5rem !important; max-width: 1500px !important; }

/* ── Masthead ── */
.masthead {
    border-top: 2px solid #D4AF37;
    border-bottom: 1px solid #2A2418;
    padding: 2.5rem 0 2rem;
    margin-bottom: 3.5rem;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
}
.masthead-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.8rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    color: #EDE5D5;
    line-height: 1;
    text-transform: uppercase;
}
.masthead-title span { color: #D4AF37; font-style: italic; }
.masthead-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    color: #5A5040;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    line-height: 2;
    text-align: right;
}

/* ── Section labels ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #D4AF37;
    border-left: 3px solid #D4AF37;
    padding-left: 0.85rem;
    margin-bottom: 1.75rem;
    margin-top: 3rem;
}

/* ── Metal cards ── */
.metal-card {
    background: linear-gradient(145deg, #100F0C 0%, #0C0B09 100%);
    border: 1px solid #201E18;
    border-top: 3px solid var(--accent);
    border-radius: 3px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    height: 100%;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metal-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 80px;
    background: linear-gradient(180deg, color-mix(in srgb, var(--accent) 6%, transparent) 0%, transparent 100%);
    pointer-events: none;
}
.metal-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.metal-symbol {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.metal-name {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 800;
    color: #EDE5D5;
    margin-bottom: 1.5rem;
    letter-spacing: 0.03em;
}
.metal-price {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: #F8F0E0;
    letter-spacing: -0.02em;
    margin-bottom: 0.3rem;
}
.metal-change-pos { font-family:'JetBrains Mono',monospace; font-weight:500; font-size:0.82rem; color:#4CAF50; letter-spacing:0.05em; }
.metal-change-neg { font-family:'JetBrains Mono',monospace; font-weight:500; font-size:0.82rem; color:#EF5350; letter-spacing:0.05em; }
.metal-change-neu { font-family:'JetBrains Mono',monospace; font-weight:500; font-size:0.82rem; color:#6B6055; letter-spacing:0.05em; }
.metal-divider { border:none; border-top:1px solid #1E1C16; margin:1.25rem 0; }
.metal-stat-row { display:flex; justify-content:space-between; margin-bottom:0.65rem; }
.metal-stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    font-weight: 700;
    color: #5A5040;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    align-self: center;
}
.metal-stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
    color: #C8BFA8;
}
.metal-summary {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    font-weight: 400;
    color: #8C8070;
    font-style: italic;
    line-height: 1.55;
}

/* ── Bias badges ── */
.bias-Bullish { background:rgba(76,175,80,0.12);  color:#4CAF50; border:1px solid rgba(76,175,80,0.3);  padding:4px 14px; border-radius:2px; font-family:'JetBrains Mono',monospace; font-size:0.67rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; display:inline-block; margin-top:1rem; }
.bias-Bearish { background:rgba(239,83,80,0.12);  color:#EF5350; border:1px solid rgba(239,83,80,0.3);  padding:4px 14px; border-radius:2px; font-family:'JetBrains Mono',monospace; font-size:0.67rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; display:inline-block; margin-top:1rem; }
.bias-Neutral { background:rgba(120,113,108,0.15); color:#A8A29E; border:1px solid rgba(120,113,108,0.3); padding:4px 14px; border-radius:2px; font-family:'JetBrains Mono',monospace; font-size:0.67rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; display:inline-block; margin-top:1rem; }

/* ── AI report panels ── */
.report-panel {
    background: #0C0B09;
    border: 1px solid #201E18;
    border-left: 3px solid #D4AF37;
    border-radius: 3px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.25rem;
}
.report-panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #D4AF37;
    margin-bottom: 1.1rem;
}
.report-body {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;
    font-weight: 400;
    color: #B8AC98;
    line-height: 1.75;
}
.driver-item {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.73rem;
    font-weight: 500;
    color: #8C8070;
    padding: 0.55rem 0;
    border-bottom: 1px solid #181610;
    letter-spacing: 0.04em;
    line-height: 1.5;
}
.driver-item:last-child { border-bottom: none; }
.driver-item::before { content: "◆ "; color: #D4AF37; font-size: 0.5rem; vertical-align: middle; }

/* ── Risk badge ── */
.risk-Low    { background:rgba(76,175,80,0.1);  color:#4CAF50; border:1px solid rgba(76,175,80,0.25);  padding:10px 28px; border-radius:2px; font-family:'JetBrains Mono',monospace; font-size:0.78rem; font-weight:700; letter-spacing:0.25em; text-transform:uppercase; display:inline-block; }
.risk-Medium { background:rgba(212,175,55,0.1); color:#D4AF37; border:1px solid rgba(212,175,55,0.25); padding:10px 28px; border-radius:2px; font-family:'JetBrains Mono',monospace; font-size:0.78rem; font-weight:700; letter-spacing:0.25em; text-transform:uppercase; display:inline-block; }
.risk-High   { background:rgba(239,83,80,0.1);  color:#EF5350; border:1px solid rgba(239,83,80,0.25);  padding:10px 28px; border-radius:2px; font-family:'JetBrains Mono',monospace; font-size:0.78rem; font-weight:700; letter-spacing:0.25em; text-transform:uppercase; display:inline-block; }

/* ── Chart label ── */
.chart-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    color: #5A5040;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

/* ── History log ── */
.log-entry {
    background: #0C0B09;
    border: 1px solid #181610;
    border-radius: 3px;
    padding: 1.1rem 1.5rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 2rem;
}
.log-ts {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    font-weight: 700;
    color: #3A3428;
    letter-spacing: 0.12em;
    white-space: nowrap;
}
.log-body {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    font-weight: 400;
    color: #7A7060;
    font-style: italic;
    flex: 1;
    line-height: 1.5;
}
.log-risk { font-family:'JetBrains Mono',monospace; font-size:0.62rem; font-weight:700; letter-spacing:0.18em; text-transform:uppercase; white-space:nowrap; }
.log-risk-Low    { color:#4CAF50; }
.log-risk-Medium { color:#D4AF37; }
.log-risk-High   { color:#EF5350; }
.log-metals-line { font-family:'JetBrains Mono',monospace; font-size:0.6rem; font-weight:500; color:#3A3428; margin-bottom:0.3rem; letter-spacing:0.08em; }

/* ── Run button ── */
.stButton > button {
    background: transparent !important;
    border: 2px solid #D4AF37 !important;
    color: #D4AF37 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2.75rem !important;
    border-radius: 2px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(212,175,55,0.1) !important;
    border-color: #F0CC5A !important;
    color: #F0CC5A !important;
    box-shadow: 0 0 20px rgba(212,175,55,0.15) !important;
}

/* ── Streamlit metric overrides ── */
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    color: #5A5040 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #EDE5D5 !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
}

/* ── Expander ── */
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.67rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    color: #5A5040 !important;
}

/* ── Spinner text ── */
.stSpinner > div { border-color: #D4AF37 transparent transparent transparent !important; }

hr { border-color: #1A1810 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── MASTHEAD ────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div>
        <div class="masthead-title">⬡ &nbsp;METALS &nbsp;<span>Intelligence</span></div>
    </div>
    <div class="masthead-sub">
        Commodity Market Analysis System<br>
        Gold &nbsp;·&nbsp; Silver &nbsp;·&nbsp; Copper<br>
        Live Spot · Momentum · AI Risk Report
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────── RUN BUTTON ──────────────────────────────────────
col_btn, col_desc = st.columns([1, 4])
with col_btn:
    run_clicked = st.button("⬡  Run Analysis")
with col_desc:
    st.markdown(
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.67rem;font-weight:500;'
        'color:#3A3428;letter-spacing:0.18em;padding-top:0.95rem;text-transform:uppercase;">'
        'Fetches Live Spot Prices &nbsp;·&nbsp; Computes Momentum &amp; Volatility &nbsp;·&nbsp; Generates AI Risk Report'
        '</div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────── ANALYSIS ────────────────────────────────────────
if run_clicked:
    with st.spinner("Fetching metals data and generating AI report…"):
        try:
            result = run_analysis()
        except Exception as exc:
            st.error(f"Analysis error: {exc}")
            st.stop()

    report        = result["ai_report"]
    metrics       = result["metrics"]
    metal_reports = report.get("metals", {})

    accent_colors = {"Gold": "#D4AF37", "Silver": "#C0C0C0", "Copper": "#B87333"}

    # ── METAL CARDS ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Live Spot Prices &nbsp;·&nbsp; 30-Day Metrics</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, (metal, meta) in enumerate(METALS.items()):
        m   = metrics.get(metal, {})
        mr  = metal_reports.get(metal, {})
        acc = accent_colors[metal]

        c7   = m.get("change_7d",  0)
        c30  = m.get("change_30d", 0)
        price = m.get("current_price", 0)

        def chg_class(v):
            return "metal-change-pos" if v > 0 else ("metal-change-neg" if v < 0 else "metal-change-neu")

        arrow = lambda v: "▲" if v > 0 else ("▼" if v < 0 else "—")

        bias    = mr.get("bias", "Neutral")
        conf    = mr.get("confidence", 0)
        summary = mr.get("summary", "")
        trend   = m.get("trend", "N/A")

        with cols[idx]:
            unavailable = m.get("data_unavailable") or price is None

            if unavailable:
                # Graceful "no data" card — still renders, shows what we know
                st.markdown(f"""
<div class="metal-card" style="--accent:{acc};opacity:0.6;">
    <div class="metal-symbol">{meta['symbol']} &nbsp;·&nbsp; {metal.upper()}</div>
    <div class="metal-name">{metal}</div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;
        color:#5A5040;letter-spacing:0.15em;text-transform:uppercase;margin:1.5rem 0;">
        ⚠ &nbsp;Data Unavailable
    </div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:1rem;color:#5A5040;font-style:italic;">
        Live price could not be retrieved from the API.<br>
        Analysis will use estimated values.
    </div>
</div>
""", unsafe_allow_html=True)
            else:
                price_display = f"${price:,.2f}" if price else "N/A"
                st.markdown(f"""
<div class="metal-card" style="--accent:{acc}">
    <div class="metal-symbol">{meta['symbol']} &nbsp;·&nbsp; {metal.upper()}</div>
    <div class="metal-name">{metal}</div>
    <div class="metal-price">{price_display}</div>
    <div>
        <span class="{chg_class(c7)}">{arrow(c7)} {abs(c7):.2f}% (7d)</span>
        &nbsp;&nbsp;
        <span class="{chg_class(c30)}">{arrow(c30)} {abs(c30):.2f}% (30d)</span>
    </div>
    <hr class="metal-divider">
    <div class="metal-stat-row">
        <span class="metal-stat-label">Volatility</span>
        <span class="metal-stat-value">{m.get('volatility',0):.1f}% ann.</span>
    </div>
    <div class="metal-stat-row">
        <span class="metal-stat-label">SMA-7</span>
        <span class="metal-stat-value">${m.get('sma_7',0):,.4f}</span>
    </div>
    <div class="metal-stat-row">
        <span class="metal-stat-label">SMA-20</span>
        <span class="metal-stat-value">${m.get('sma_20',0):,.4f}</span>
    </div>
    <div class="metal-stat-row">
        <span class="metal-stat-label">30d High</span>
        <span class="metal-stat-value">${m.get('period_high',0):,.4f}
            <span style="color:#5A5040;font-size:0.65rem;"> ({m.get('pct_from_high',0):+.1f}%)</span>
        </span>
    </div>
    <div class="metal-stat-row">
        <span class="metal-stat-label">30d Low</span>
        <span class="metal-stat-value">${m.get('period_low',0):,.4f}
            <span style="color:#5A5040;font-size:0.65rem;"> ({m.get('pct_from_low',0):+.1f}%)</span>
        </span>
    </div>
    <div class="metal-stat-row">
        <span class="metal-stat-label">Trend</span>
        <span class="metal-stat-value">{trend}</span>
    </div>
    <hr class="metal-divider">
    <div class="metal-summary">{summary}</div>
    <div class="bias-{bias}">{bias} &nbsp;·&nbsp; {conf}% conf.</div>
</div>
""", unsafe_allow_html=True)

    # ── PRICE CHARTS ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">30-Day Price History</div>', unsafe_allow_html=True)
    chart_cols = st.columns(3)
    for idx, metal in enumerate(METALS):
        m       = metrics.get(metal, {})
        history = m.get("history", [])
        if history:
            df = pd.DataFrame(history)
            df["date"] = pd.to_datetime(df["date"])
            with chart_cols[idx]:
                st.markdown(f'<div class="chart-label">{metal} / USD</div>', unsafe_allow_html=True)
                st.line_chart(
                    df.set_index("date")["price"],
                    color=accent_colors[metal],
                    height=170,
                )

    # ── AI REPORT ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">AI Intelligence Report</div>', unsafe_allow_html=True)

    risk = report.get("risk_level", "Medium")
    st.markdown(f'<div class="risk-{risk}">◆ &nbsp;Market Risk — {risk}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.markdown(f"""
<div class="report-panel">
    <div class="report-panel-title">◆ &nbsp;Market Outlook</div>
    <div class="report-body">{report.get('outlook','')}</div>
</div>""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="report-panel">
    <div class="report-panel-title">◆ &nbsp;Cross-Metal Dynamics</div>
    <div class="report-body">{report.get('cross_metal_insight','')}</div>
</div>""", unsafe_allow_html=True)

    with right_col:
        drivers_html = "".join(f'<div class="driver-item">{d}</div>' for d in report.get("macro_drivers", []))
        st.markdown(f"""
<div class="report-panel">
    <div class="report-panel-title">◆ &nbsp;Macro Drivers</div>
    {drivers_html}
</div>""", unsafe_allow_html=True)

        risks_html = "".join(f'<div class="driver-item">{r}</div>' for r in report.get("key_risks", []))
        st.markdown(f"""
<div class="report-panel" style="border-left-color:#EF5350;">
    <div class="report-panel-title" style="color:#EF5350;">◆ &nbsp;Key Risks</div>
    {risks_html}
</div>""", unsafe_allow_html=True)

    # ── NEWS ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Macro News Feed</div>', unsafe_allow_html=True)
    headlines = result.get("headlines", [])
    news_cols = st.columns(2)
    for i, h in enumerate(headlines):
        with news_cols[i % 2]:
            st.markdown(
                f'<div class="driver-item" style="padding:0.7rem 0.5rem;font-size:0.76rem;">{h}</div>',
                unsafe_allow_html=True,
            )

# ─────────────────────── HISTORY LOG ─────────────────────────────────────────
st.markdown('<div class="section-label">Analysis History</div>', unsafe_allow_html=True)
recent = load_recent_reports(5)

if not recent:
    st.markdown(
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;font-weight:700;'
        'color:#201E18;letter-spacing:0.2em;text-transform:uppercase;">No reports logged yet</div>',
        unsafe_allow_html=True,
    )
else:
    for entry in recent:
        r   = entry.get("ai_report", {})
        ts  = entry["timestamp"][:16].replace("T", " ")
        risk = r.get("risk_level", "—")
        snippet = (r.get("outlook", "") or "")[:120] + "…"
        metals_line = " &nbsp;·&nbsp; ".join(
            f"{m}: {r.get('metals', {}).get(m, {}).get('bias', '—')}"
            for m in ["Gold", "Silver", "Copper"]
        )
        st.markdown(f"""
<div class="log-entry">
    <div class="log-ts">{ts}&nbsp;UTC</div>
    <div>
        <div class="log-metals-line">{metals_line}</div>
        <div class="log-body">"{snippet}"</div>
    </div>
    <div class="log-risk log-risk-{risk}">◆ {risk}&nbsp;Risk</div>
</div>""", unsafe_allow_html=True)

# ─────────────────────── FOOTER ──────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #181610;margin-top:5rem;padding-top:1.75rem;
    display:flex;justify-content:space-between;align-items:center;">
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;font-weight:700;
        color:#201E18;letter-spacing:0.22em;text-transform:uppercase;">
        Data: Metals.dev &nbsp;·&nbsp; CryptoCompare &nbsp;·&nbsp; AI: OpenAI GPT-4o-mini
    </div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:1rem;font-weight:600;
        color:#2A2418;font-style:italic;letter-spacing:0.05em;">
        For research purposes only &nbsp;·&nbsp; Not financial advice
    </div>
</div>
""", unsafe_allow_html=True)
