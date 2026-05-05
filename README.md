# Monte Carlo Risk Engine
### Cross-Asset Simulation & Risk Analysis · GLD · MSFT · COIN

**Live Demo → [monte-carlo-risk-engine.streamlit.app](https://share.streamlit.io)** *(deploy and replace this link)*

A quantitative finance project applying Monte Carlo simulation via Geometric Brownian Motion to model future price distributions across three fundamentally different asset classes. The project computes institutional-grade risk metrics — Value at Risk, Conditional Value at Risk, and European call option pricing — and compares how model assumptions hold differently depending on asset volatility.

Built as a fully interactive Streamlit application with a research notebook documenting the full methodology.

---

## Project Motivation

Basic Monte Carlo tutorials simulate a single stock and stop at a price chart. This project goes further by asking a more analytical question: **how does the same stochastic model behave across asset classes with fundamentally different risk profiles?**

By running identical simulations on a commodity ETF (GLD), a large-cap technology stock (MSFT), and a crypto-adjacent equity (COIN), the project quantifies how volatility drives divergent outcomes — and demonstrates that options pricing is fundamentally a bet on volatility, not direction.

---

## Methodology

### Geometric Brownian Motion (GBM)

Each asset's future price path is simulated using the GBM formula:

$$S_t = S_{t-1} \cdot e^{\left(\mu - \frac{\sigma^2}{2}\right)\Delta t + \sigma \varepsilon \sqrt{\Delta t}}$$

Where:
- $S_t$ — simulated price at time $t$
- $\mu$ — mean daily log return (drift)
- $\sigma$ — standard deviation of daily log returns (volatility)
- $\varepsilon$ — random shock drawn from $\mathcal{N}(0,1)$
- $\frac{\sigma^2}{2}$ — Itô correction, adjusting for the mathematical bias in log-normal compounding

### Parameter Calibration

Drift and volatility are calibrated empirically from historical daily log returns (2020–2024):

```
Daily log return = log(Pₜ / Pₜ₋₁)
Drift            = mean(log returns) − σ²/2
Volatility       = std(log returns)
```

### Risk Metrics

| Metric | Definition |
|--------|-----------|
| **VaR (5th percentile)** | The price threshold below which only the worst 5% of simulations fall |
| **CVaR (Expected Shortfall)** | The average ending price across all simulations that breach the VaR threshold — captures true tail severity |
| **Probability of Gain** | Proportion of 1,000 simulations ending above the starting price |
| **Call Option Price** | Monte Carlo payoff averaging: $C = e^{-rT} \cdot \mathbb{E}[\max(S_T - K, 0)]$ with strike $K = 1.1 \times S_0$ |

### Why CVaR over VaR?

VaR answers: *"where do bad outcomes begin?"*
CVaR answers: *"how bad do they actually get beyond that point?"*

During the 2008 financial crisis, institutions correctly calculated VaR but severely underestimated CVaR. The gap between the two metrics is widest for COIN — quantifying that tail risk is non-linear and compounds with volatility.

---

## Assets Analysed

| Asset | Type | Rationale |
|-------|------|-----------|
| **GLD** | SPDR Gold ETF | Safe haven commodity. Benchmark for low-volatility behaviour. Represents capital preservation. |
| **MSFT** | Microsoft Corp | Stable large-cap technology stock. Represents moderate-growth equity with strong historical drift. |
| **COIN** | Coinbase Global | Crypto-adjacent equity. Represents maximum volatility in public equity markets. Stress-tests model assumptions. |

---

## Key Findings

### Simulation Results (1,000 paths · 252 trading days)

| Asset | Start | Mean End | VaR (5%) | CVaR | 95th Pct | Prob Gain |
|-------|-------|----------|----------|------|----------|-----------|
| **GLD** | $191.17 | $205.84 | $158.00 | — | — | 65.4% |
| **MSFT** | $369.67 | $459.67 | $257.12 | $227.36 | $739.81 | 68.7% |
| **COIN** | $173.92 | $140.35 | $21.10 | $15.63 | $442.87 | 24.7% |

### Volatility Divergence

```
GLD  daily volatility: 0.987%
MSFT daily volatility: 2.056%  →  2.1× more volatile than GLD
COIN daily volatility: 5.684%  →  5.7× more volatile than GLD
```

### Critical Insights

**1. The same model produces radically different outcomes**
All three simulations use identical GBM code. The only difference is the calibrated volatility parameter. COIN's simulation fan spans from near-zero to $442.87 — while GLD stays in a tight, predictable band around its starting price. This demonstrates that volatility, not the model itself, drives risk.

**2. COIN's mean ending price is below its starting price**
Despite a positive drift, COIN's mean simulated price ($140.35) falls *below* its starting price ($173.92). This occurs because Itô's correction subtracts $\frac{\sigma^2}{2}$ from the arithmetic mean — at COIN's extreme volatility, this correction is large enough to pull the expected growth negative. A result that only appears when the mathematics is implemented correctly.

**3. Probability of gain diverges dramatically**
GLD: 65.4% · MSFT: 68.7% · COIN: 24.7%. Despite COIN having the highest upside potential ($442.87 at the 95th percentile), it has only a 24.7% chance of ending above its starting price — the fat downside tail dominates.

**4. Options pricing reflects volatility directly**
A call option struck 10% above the current price is worth far more on COIN than GLD, purely because volatility increases the probability of large upward moves. This confirms the fundamental principle: **when you buy an option, you are buying volatility, not direction.**

---

## Model Limitations

This project deliberately documents where GBM breaks down — understanding a model's failure modes is as important as implementing it correctly.

**1. Constant volatility assumption**
GBM assumes $\sigma$ is fixed. In reality, volatility clusters — markets are calm for months then suddenly chaotic. This is particularly problematic for COIN, which exhibits extreme volatility regime changes. The Heston Stochastic Volatility Model addresses this by allowing $\sigma$ itself to follow a random process.

**2. Log-normal return distribution**
Real asset returns have fat tails — extreme events occur more frequently than the normal distribution predicts. The 2020 COVID crash and the 2022 crypto collapse are examples GBM would dramatically underestimate.

**3. Independent asset simulation**
Each asset is simulated independently. In reality, GLD, MSFT and COIN have non-zero correlations that affect portfolio-level risk. A correlated simulation using Cholesky decomposition would more accurately reflect a real portfolio.

**4. No regime switching**
GBM uses a single drift and volatility calibrated from the full historical period. Markets switch between bull and bear regimes with different statistical properties — a Markov regime-switching model would capture this.

---

## Future Extensions

- [ ] Heston Stochastic Volatility Model — allow $\sigma$ to be random
- [ ] Correlated portfolio simulation via Cholesky decomposition
- [ ] Backtesting — compare simulated distributions against actual 2024 outcomes
- [ ] Quasi-Monte Carlo with Sobol sequences for faster convergence
- [ ] Variance reduction techniques (antithetic variates, control variates)


## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9 | Core language |
| NumPy | Simulation mathematics |
| Pandas | Data manipulation |
| yFinance | Historical price data |
| Matplotlib | Visualisation |
| Streamlit | Interactive web application |

---

## Author

**Priyanka Ghosh**  
Quantitative Finance · Python · Financial Modelling

[GitHub](https://github.com/PriyankaGhosh-quant) 

---

*Data sourced from Yahoo Finance via yfinance. Simulation results vary between runs due to random number generation. Historical performance does not guarantee future results.*
