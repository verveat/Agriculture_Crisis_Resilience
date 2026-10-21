# 🌾 Agricultural Market Resilience in Germany

Interactive dashboard (Streamlit + Plotly) for the project
*A Comparative Analysis of Soft Wheat, Barley and Potato Markets*.
It shows how supply balances and prices of the three crops develop around 12 crisis
episodes (1990–2026) in the pre-crisis, crisis and post-crisis phases.

## What the dashboard shows

| Tab | Content |
|---|---|
| Overview | Problem, goal, approach, research questions |
| Risk framework | Risk categories and transmission mechanisms (OECD / FAO-based synthesis) |
| Timeline | Analysis windows of all episodes, details, date quality and sources |
| Long-term view | Any indicator over time with the crisis phases as background |
| Supply balance | Production, imports, exports, domestic use, self-sufficiency, import/export quota for one episode |
| Prices & recovery | Price index, shock magnitude, timing, duration and recovery |
| Crisis comparison | Heatmaps: production change and price shock for every crop × episode |

## Run locally (with uv)

```bash
uv add streamlit plotly
uv run streamlit run dashboard/app.py
```

or with pip:

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## Project structure

```
.streamlit/config.toml      colours of the Streamlit theme
dashboard/
  app.py                    the dashboard
  assets/banner.png         your banner (optional, a drawn fallback is used otherwise)
  data/
    events.csv              the 12 crisis episodes (included)
    supply_balance.csv      BLE supply balances (add your data here)
    prices.csv              annual prices in EUR per tonne (add your data here)
```

## Data

* `supply_balance.csv`: the BLE table is read as it is (German column names, decimal comma,
  marketing years such as `1991/92`). Used columns: `Wirtschaftsjahr`, `Bilanz_Produkt`,
  `Verwendbare_Erzeugung`, `Einfuhr`, `Ausfuhr`, `Inlandsverwendung_standardisiert`, and for the
  use breakdown `Futter`, `Industrielle_Verwertung`, `Nahrungsverbrauch`, `Saatgut`, `Verluste`.
  Self-sufficiency, import quota and export quota are computed from these.
* `prices.csv`: columns `crop,year,price_eur_per_t`.
* `events.csv`: the episode table with analysis windows, risk categories, mechanisms and sources.

Without `supply_balance.csv` or `prices.csv` the dashboard runs with clearly labelled
**synthetic demo data**. These are not real observations.

### Marketing years

A year `1991` stands for the marketing year 1991/92 (July–June). The crisis phase of an episode
is derived from its event start date or the years in `period` and clipped to its analysis window.

## Publish on GitHub

GitHub Pages cannot run Python. Push the repository to GitHub, then deploy it for free on
<https://share.streamlit.io> (New app → select repository → main file `dashboard/app.py`) and
put the resulting URL here.

## Method notes

* The risk categories are an analytical synthesis informed by OECD (2020) and FAO work, not a
  standardised taxonomy. Transmission mechanisms are hypotheses, not established causal effects.
* Temporal overlap of an episode and a market movement does not establish causality.
* Prices are nominal unless deflated beforehand.

Framework source: OECD (2020), *Strengthening Agricultural Resilience in the Face of Multiple
Risks*, <https://doi.org/10.1787/2250453e-en>
