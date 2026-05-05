import streamlit as st
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="Monte Carlo Risk Engine",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Bricolage+Grotesque:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Bricolage Grotesque', sans-serif;
}

.stApp {
    background: #09071a;
}

section[data-testid="stSidebar"] {
    background: #0f0c24;
    border-right: 1px solid rgba(127,119,221,0.15);
}

.block-container {
    padding: 1.5rem 2rem;
}

.page-title {
    padding-top: 2rem;
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #e8e5ff;
    letter-spacing: -0.03em;
    line-height: 1.1;
}

.page-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #6b6494;
    margin-top: 4px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.brand-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(127,119,221,0.15);
}

.brand-name {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #534AB7;
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 1rem 0;
}

.kpi {
    background: #14103a;
    border: 1px solid rgba(127,119,221,0.15);
    border-radius: 12px;
    padding: 13px 15px;
    position: relative;
    overflow: hidden;
}

.kpi-accent {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}

.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6b6494;
    margin-bottom: 6px;
}

.kpi-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.1rem;
    font-weight: 500;
    color: #e8e5ff;
}

.kpi-delta-up {
    font-size: 0.65rem;
    color: #1D9E75;
    margin-top: 3px;
}

.kpi-delta-down {
    font-size: 0.65rem;
    color: #E24B4A;
    margin-top: 3px;
}

.insight {
    background: rgba(83,74,183,0.1);
    border: 1px solid rgba(127,119,221,0.2);
    border-left: 3px solid #534AB7;
    border-radius: 0 10px 10px 0;
    padding: 11px 15px;
    font-size: 0.8rem;
    color: #AFA9EC;
    line-height: 1.6;
    margin: 0.5rem 0;
}

.insight strong {
    color: #e8e5ff;
}

.section-hdr {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #534AB7;
    border-bottom: 1px solid rgba(83,74,183,0.2);
    padding-bottom: 6px;
    margin: 1.2rem 0 0.8rem;
}

.asset-card {
    background: #14103a;
    border: 1px solid rgba(127,119,221,0.15);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    transition: border-color 0.2s;
}

.asset-ticker {
    font-family: 'DM Mono', monospace;
    font-size: 1rem;
    font-weight: 500;
}

.asset-name {
    font-size: 0.7rem;
    color: #6b6494;
    margin: 3px 0 6px;
}

.asset-desc {
    font-size: 0.73rem;
    color: #AFA9EC;
    line-height: 1.5;
}

.stButton > button {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    background: #534AB7 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.25rem !important;
    width: 100% !important;
    transition: all 0.18s !important;
}

.stButton > button:hover {
    background: #7F77DD !important;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #6b6494 !important;
}

.sidebar-logo {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #534AB7;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(83,74,183,0.2);
    margin-bottom: 8px;
}

.vol-card {
    background: #14103a;
    border: 1px solid rgba(127,119,221,0.15);
    border-radius: 11px;
    padding: 12px;
    text-align: center;
}

.vol-pct {
    font-family: 'DM Mono', monospace;
    font-size: 0.9rem;
    font-weight: 500;
    margin-top: 6px;
}

.vol-name {
    font-size: 0.65rem;
    color: #6b6494;
    margin-top: 2px;
}

.vol-mult {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    padding: 2px 7px;
    border-radius: 10px;
    display: inline-block;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

COLORS = {
    "GLD":  "#4a9eff",
    "MSFT": "#8b7fe8",
    "COIN": "#6366f1"
}
STARTS = {"GLD": 191.17, "MSFT": 374.50, "COIN": 170.85}
VOLS   = {"GLD": 0.00987, "MSFT": 0.02056, "COIN": 0.05684}

def setup_fig():
    return "#09071a", "#0f0c24"

def style_ax(ax, fig_bg, ax_bg):
    ax.set_facecolor(ax_bg)
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2550")
    ax.tick_params(colors="#6b6494", labelsize=8)
    ax.xaxis.label.set_color("#6b6494")
    ax.yaxis.label.set_color("#6b6494")
    ax.title.set_color("#AFA9EC")

def run_simulation(ticker, simulations, days, start_date):
    data = yf.download(ticker, start=start_date, end="2024-01-01", progress=False)
    close = data["Close"].squeeze()
    log_ret = np.log(close / close.shift(1)).dropna()
    mean  = float(log_ret.mean())
    std   = float(log_ret.std())
    drift = mean - 0.5 * std**2
    last  = float(close.iloc[-1])
    results = np.zeros((days, simulations))
    for s in range(simulations):
        p = np.zeros(days)
        p[0] = last
        for d in range(1, days):
            p[d] = p[d-1] * np.exp(drift + std * np.random.normal())
        results[:, s] = p
    return results, last, std

def get_metrics(results, last):
    f   = results[-1, :]
    var = np.percentile(f, 5)
    return {
        "mean": f.mean(),
        "var":  var,
        "cvar": f[f <= var].mean(),
        "p95":  np.percentile(f, 95),
        "prob": (f > last).mean() * 100,
        "final": f
    }

def price_call(final, strike, r=0.05, days=252):
    return np.exp(-r * days / 252) * np.maximum(final - strike, 0).mean()

with st.sidebar:
    st.markdown('<div class="sidebar-logo">Monte Carlo · Risk Engine</div>', unsafe_allow_html=True)
    ticker  = st.selectbox("Asset", ["GLD", "MSFT", "COIN"],
                           help="GLD = Gold ETF | MSFT = Microsoft | COIN = Coinbase")
    sims    = st.slider("Simulations", 100, 2000, 1000, 100)
    days    = st.slider("Time horizon (trading days)", 30, 504, 252)
    start_d = st.selectbox("Historical data from",
                           ["2020-01-01", "2019-01-01", "2021-01-01"])
    st.markdown("---")
    run_single = st.button("Run simulation")
    run_all    = st.button("Compare all assets")

st.markdown('<div class="page-title">Monte Carlo Risk Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Cross-asset simulation · Geometric Brownian Motion · GLD · MSFT · COIN</div>',
            unsafe_allow_html=True)

if run_single:
    with st.spinner(f"Simulating {sims:,} paths for {ticker}…"):
        res, last, std = run_simulation(ticker, sims, days, start_d)

    m   = get_metrics(res, last)
    cp  = price_call(m["final"], last * 1.1, days=days)
    clr = COLORS[ticker]
    delta = (m["mean"] - last) / last * 100
    loss  = last - m["cvar"]

    st.markdown(f'<div class="section-hdr">Results — {ticker}</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    def kpi_html(label, value, accent, delta_str=None, delta_up=True):
        delta_html = ""
        if delta_str:
            cls = "kpi-delta-up" if delta_up else "kpi-delta-down"
            delta_html = f'<div class="{cls}">{delta_str}</div>'
        return f"""
        <div class="kpi">
            <div class="kpi-accent" style="background:{accent}"></div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>"""

    c1.markdown(kpi_html("Starting price",    f"${last:.2f}",       clr), unsafe_allow_html=True)
    c2.markdown(kpi_html("Mean ending price", f"${m['mean']:.2f}",  "#7F77DD",
                          f"{'+'if delta>=0 else ''}{delta:.1f}%",  delta >= 0), unsafe_allow_html=True)
    c3.markdown(kpi_html("Prob of gain",      f"{m['prob']:.1f}%",  "#534AB7"), unsafe_allow_html=True)
    c4.markdown(kpi_html("VaR (5th pct)",     f"${m['var']:.2f}",   "#E24B4A"), unsafe_allow_html=True)
    c5.markdown(kpi_html("CVaR",              f"${m['cvar']:.2f}",  "#A32D2D"), unsafe_allow_html=True)
    c6.markdown(kpi_html("Call option (+10%)",f"${cp:.2f}",         "#1D9E75"), unsafe_allow_html=True)

    st.markdown(f"""<div class="insight">
        <strong>{ticker}</strong> has a <strong>{m['prob']:.1f}%</strong> probability of gain over
        <strong>{days}</strong> trading days. Daily volatility of <strong>{std*100:.3f}%</strong>
        drives path dispersion. In the worst 5% of scenarios, CVaR estimates an average loss of
        <strong>${loss:.2f}</strong> from the starting price —
        {'extreme tail risk consistent with crypto-adjacent assets.' if std > 0.03
         else 'moderate tail risk consistent with the asset class.'}
    </div>""", unsafe_allow_html=True)

    fig_bg, ax_bg = setup_fig()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), facecolor=fig_bg)

    ax1.plot(res, alpha=0.04, color=clr, linewidth=0.5)
    ax1.plot(res.mean(axis=1), color="#e8e5ff", linewidth=2,
             label="Average path", zorder=5)
    ax1.axhline(last, color=clr, linewidth=1, linestyle="--",
                alpha=0.6, label="Starting price")
    ax1.axhline(m["var"], color="#E24B4A", linewidth=1, linestyle="--",
                alpha=0.7, label=f"VaR ${m['var']:.0f}")
    ax1.set_title(f"{ticker} — {sims:,} simulated paths", fontsize=10, pad=10)
    ax1.set_xlabel("Trading days", fontsize=9)
    ax1.set_ylabel("Price (USD)", fontsize=9)
    ax1.legend(fontsize=8, facecolor=ax_bg, edgecolor="none", labelcolor="#AFA9EC")
    style_ax(ax1, fig_bg, ax_bg)

    f = m["final"]
    var_mask = f <= m["var"]
    ax2.hist(f[~var_mask], bins=50, color=clr, alpha=0.7,
             edgecolor=ax_bg, linewidth=0.3, label="Normal outcomes")
    ax2.hist(f[var_mask],  bins=15, color="#E24B4A", alpha=0.85,
             edgecolor=ax_bg, linewidth=0.3, label="Tail risk (worst 5%)")
    ax2.axvline(last,       color="#e8e5ff", linewidth=1.5,
                linestyle="--", label=f"Start ${last:.0f}")
    ax2.axvline(m["var"],   color="#E24B4A", linewidth=1.5,
                linestyle="--", label=f"VaR ${m['var']:.0f}")
    ax2.axvline(m["cvar"],  color="#A32D2D", linewidth=1.5,
                linestyle=":",  label=f"CVaR ${m['cvar']:.0f}")
    ax2.set_title("Distribution of ending prices", fontsize=10, pad=10)
    ax2.set_xlabel("Price (USD)", fontsize=9)
    ax2.set_ylabel("Frequency", fontsize=9)
    ax2.legend(fontsize=8, facecolor=ax_bg, edgecolor="none", labelcolor="#AFA9EC")
    style_ax(ax2, fig_bg, ax_bg)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

elif run_all:
    tickers = ["GLD", "MSFT", "COIN"]
    all_res, all_m, all_last, all_std = {}, {}, {}, {}

    with st.spinner("Simulating GLD, MSFT and COIN…"):
        for t in tickers:
            r, lp, sd = run_simulation(t, sims, days, start_d)
            all_res[t]  = r
            all_m[t]    = get_metrics(r, lp)
            all_last[t] = lp
            all_std[t]  = sd

    st.markdown('<div class="section-hdr">Cross-asset comparison</div>', unsafe_allow_html=True)

    rows = []
    for t in tickers:
        m  = all_m[t]
        lp = all_last[t]
        cp = price_call(m["final"], lp * 1.1, days=days)
        rows.append({
            "Asset":        t,
            "Start":        f"${lp:.2f}",
            "Mean end":     f"${m['mean']:.2f}",
            "Daily vol":    f"{all_std[t]*100:.3f}%",
            "VaR (5%)":     f"${m['var']:.2f}",
            "CVaR":         f"${m['cvar']:.2f}",
            "Prob gain":    f"{m['prob']:.1f}%",
            "Call (+10%)":  f"${cp:.2f}",
        })
    st.dataframe(pd.DataFrame(rows).set_index("Asset"), use_container_width=True)

    coin_v = all_std["COIN"] * 100
    gld_v  = all_std["GLD"]  * 100
    st.markdown(f"""<div class="insight">
        COIN is <strong>{coin_v/gld_v:.1f}× more volatile</strong> than GLD
        ({coin_v:.3f}% vs {gld_v:.3f}% daily). The same GBM model produces
        fundamentally different risk profiles across asset classes — COIN's simulation
        fan spans near-zero to hundreds of dollars above the start, while GLD stays
        in a tight predictable band. <strong>Volatility is what you are really pricing.</strong>
    </div>""", unsafe_allow_html=True)

    fig_bg, ax_bg = setup_fig()
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), facecolor=fig_bg)
    fig.suptitle(f"Monte Carlo — {sims:,} paths — {days} trading days",
                 color="#AFA9EC", fontsize=11, y=1.01)

    for ax, t in zip(axes, tickers):
        ax.plot(all_res[t], alpha=0.04, color=COLORS[t], linewidth=0.5)
        ax.plot(all_res[t].mean(axis=1), color="#e8e5ff", linewidth=2)
        ax.axhline(all_last[t], color=COLORS[t], linewidth=1,
                   linestyle="--", alpha=0.55)
        ax.axhline(all_m[t]["var"], color="#E24B4A", linewidth=1,
                   linestyle="--", alpha=0.6)
        ax.set_title(t, fontsize=11, color=COLORS[t], pad=8)
        ax.set_xlabel("Trading days", fontsize=8)
        ax.set_ylabel("Price (USD)", fontsize=8)
        style_ax(ax, fig_bg, ax_bg)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 4), facecolor=fig_bg)

    vols  = [all_std[t] * 100 for t in tickers]
    bars  = ax3.bar(tickers, vols, color=[COLORS[t] for t in tickers],
                    width=0.5, edgecolor=ax_bg, linewidth=0.5)
    for bar, v in zip(bars, vols):
        ax3.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.05,
                 f"{v:.3f}%", ha="center", va="bottom",
                 fontsize=9, color="#e8e5ff", fontweight="bold")
    ax3.set_title("Daily volatility by asset", fontsize=10, pad=8)
    ax3.set_ylabel("Daily volatility (%)", fontsize=8)
    style_ax(ax3, fig_bg, ax_bg)

    for t in tickers:
        f = all_m[t]["final"] / all_last[t]
        ax4.hist(f, bins=55, alpha=0.5, color=COLORS[t],
                 label=t, edgecolor=ax_bg, linewidth=0.2)
    ax4.axvline(1, color="#e8e5ff", linewidth=1.5,
                linestyle="--", label="Break even")
    ax4.set_title("Return distributions — all assets", fontsize=10, pad=8)
    ax4.set_xlabel("Final price / starting price", fontsize=8)
    ax4.set_ylabel("Frequency", fontsize=8)
    ax4.legend(fontsize=8, facecolor=ax_bg, edgecolor="none", labelcolor="#AFA9EC")
    style_ax(ax4, fig_bg, ax_bg)

    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

    st.markdown('<div class="section-hdr">Volatility breakdown</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    gld_vol = all_std["GLD"]
    for col, t in zip([c1, c2, c3], tickers):
        v    = all_std[t] * 100
        mult = all_std[t] / gld_vol
        mult_str = "1× baseline" if mult < 1.5 else f"{mult:.1f}× GLD"
        col.markdown(f"""
        <div class="vol-card" style="border-top:2px solid {COLORS[t]}">
            <div class="vol-pct" style="color:{COLORS[t]}">{v:.3f}%</div>
            <div class="vol-name">{t} · daily volatility</div>
            <div class="vol-mult" style="background:rgba(127,119,221,0.1);color:{COLORS[t]}">{mult_str}</div>
        </div>""", unsafe_allow_html=True)

else:
    st.markdown('<div class="section-hdr">Assets</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    assets = [
        ("GLD",  "#4a9eff", "Gold ETF",   "Safe haven commodity. Low volatility (~0.99% daily). Benchmark for stable, predictable behaviour."),
        ("MSFT", "#8b7fe8", "Microsoft",  "Large cap technology stock. Moderate volatility (~2.06% daily). Strong historical upward drift."),
        ("COIN", "#6366f1", "Coinbase",   "Crypto-adjacent equity. Extreme volatility (~5.68% daily). Maximum risk and reward in public equities."),
    ]
    for col, (t, c, n, d) in zip([c1, c2, c3], assets):
        col.markdown(f"""
        <div class="asset-card" style="border-top:3px solid {c}">
            <div class="asset-ticker" style="color:{c}">{t}</div>
            <div class="asset-name">{n}</div>
            <div class="asset-desc">{d}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-hdr">Methodology</div>', unsafe_allow_html=True)
    st.markdown("""
    This app models future price paths using **Geometric Brownian Motion (GBM)**:

    $$S_t = S_{t-1} \\cdot e^{\\left(\\mu - \\frac{\\sigma^2}{2}\\right)\\Delta t + \\sigma \\varepsilon \\sqrt{\\Delta t}}$$

    Parameters are calibrated empirically from historical daily log returns (2020–2024).
    Risk metrics include **VaR** (5th percentile outcome), **CVaR** (average of worst 5% of scenarios),
    and **European call option pricing** via Monte Carlo payoff averaging.
    """)
    st.markdown("""<div class="insight">
        Select an asset and parameters in the sidebar, then click <strong>Run simulation</strong>
        for a single asset analysis — or <strong>Compare all assets</strong> to see GLD, MSFT
        and COIN side by side with full risk metric comparison.
    </div>""", unsafe_allow_html=True)
