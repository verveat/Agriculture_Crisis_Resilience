"""Agricultural Market Resilience in Germany – interactive dashboard.

A comparative analysis of soft wheat, barley and potato markets.
Built with Streamlit + Plotly. Design follows the project banner
(terracotta / peach strata, sky blue, wheat gold, potato-plant green).

DATA
----
Real data are loaded in this order of priority:
  1. files uploaded in the sidebar
  2. dashboard/data/supply_balance.csv  and  dashboard/data/prices.csv
  3. otherwise: clearly labelled SYNTHETIC DEMO data (not real values!)

The supply-balance file can be the BLE table as it is (German column names,
decimal comma, marketing year like 1991/92). See the tab "Data & method".
"""

from __future__ import annotations

import ast
import base64
import io
import math
import pathlib
import re

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

HERE = pathlib.Path(__file__).parent
DATA_DIR = HERE / "data"

# ----------------------------------------------------------------------------
# Palette (estimated from the banner)
# ----------------------------------------------------------------------------
C = {
    "terracotta": "#C8664A",
    "terracotta_dark": "#A94E36",
    "peach": "#F2B79B",
    "peach_dark": "#E9A486",
    "cream": "#FBEEE4",
    "sand": "#F6D9C6",
    "card": "#FFF7F0",
    "sky": "#6C9BD1",
    "sky_light": "#BFD6EE",
    "lavender": "#8C86BF",
    "wheat": "#E3B341",
    "teal": "#2E9C85",
    "teal_dark": "#1F7A68",
    "ink": "#2E2A3B",
    "navy": "#10131F",
}

CROP_COLORS = {
    "Soft wheat": C["wheat"],
    "Barley": C["terracotta"],
    "Potatoes": C["teal"],
}

CAT_COLORS = {
    "Production Risks": C["wheat"],
    "Market and Price Risks": C["terracotta"],
    "Input Cost Risks": C["peach_dark"],
    "Trade and Supply Chain Risks": C["sky"],
    "Financial Risks": C["lavender"],
    "Policy and Institutional Risks": C["teal"],
    "Geopolitical and Systemic Risks": "#4A4766",
}

st.set_page_config(
    page_title="Agricultural Market Resilience in Germany",
    page_icon="🌾",
    layout="wide",
)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&display=swap');
    html, body, [class*="css"], .stApp {{
        font-family: 'Nunito', sans-serif;
        color: {C['ink']};
    }}
    .stApp {{
        background: linear-gradient({C['cream']} 0%, {C['cream']} 70%, {C['sand']} 100%);
    }}
    h1, h2, h3 {{ font-weight: 800; letter-spacing: -0.01em; color: {C['ink']}; }}
    .banner {{
        border-radius: 18px; overflow: hidden;
        box-shadow: 0 8px 24px rgba(16,19,31,.25);
        border: 6px solid {C['navy']};
        margin-bottom: 1.2rem;
    }}
    .banner img, .banner svg {{ display: block; width: 100%; height: auto; }}
    .kpi {{
        background: {C['card']}; border-radius: 16px; padding: 14px 18px;
        border-left: 8px solid var(--accent);
        box-shadow: 0 3px 10px rgba(169,78,54,.12);
    }}
    .kpi .label {{ font-size: .85rem; font-weight: 600; opacity: .75; }}
    .kpi .value {{ font-size: 1.8rem; font-weight: 800; line-height: 1.15; }}
    .kpi .sub {{ font-size: .85rem; font-weight: 600; color: var(--accent); }}
    .qcard {{
        background: {C['card']}; border-radius: 16px; padding: 16px 18px;
        border-top: 8px solid var(--accent); height: 100%;
        box-shadow: 0 3px 10px rgba(169,78,54,.12);
    }}
    .qcard h4 {{ margin: 0 0 .4rem 0; font-weight: 800; }}
    .qcard p {{ margin: 0; font-size: .95rem; }}
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {C['card']}; border-radius: 18px;
        border-color: {C['peach']};
    }}
    section[data-testid="stSidebar"] {{
        background: {C['sand']};
        border-right: 6px solid {C['peach']};
    }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 700; }}
    .stTabs [aria-selected="true"] {{ color: {C['terracotta_dark']}; }}
    .footnote {{ font-size: .8rem; opacity: .7; padding-top: .5rem; }}
    .chip {{
        display: inline-block; padding: 2px 10px; border-radius: 999px;
        font-size: .78rem; font-weight: 700; color: #fff; margin-right: 6px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Banner
# ----------------------------------------------------------------------------
def wheat_svg(x: float, base_y: float, height: float, lean: float = 0.0) -> str:
    top_x, top_y = x + lean, base_y - height
    parts = [
        f'<path d="M{x},{base_y} Q{x + lean * .3},{base_y - height * .5} {top_x},{top_y}" '
        f'stroke="#9DAA4E" stroke-width="2" fill="none"/>'
    ]
    for i in range(7):
        ex, ey = top_x - lean * (i / 7) * 0.15, top_y + i * 9
        parts.append(
            f'<ellipse cx="{ex - 4}" cy="{ey}" rx="3.2" ry="8" fill="{C["wheat"]}" '
            f'transform="rotate(-18 {ex - 4} {ey})"/>'
            f'<ellipse cx="{ex + 4}" cy="{ey + 3}" rx="3.2" ry="8" fill="#D9A52E" '
            f'transform="rotate(18 {ex + 4} {ey + 3})"/>'
        )
    return "".join(parts)


def fallback_banner_svg() -> str:
    wheat = "".join(
        wheat_svg(x, 235, h, lean)
        for x, h, lean in [
            (270, 150, -4), (310, 130, 4), (350, 170, -2), (390, 190, 3),
            (430, 175, -3), (480, 150, 6), (500, 135, 8),
            (770, 140, -6), (800, 160, 2), (835, 180, 5), (860, 150, 7),
        ]
    )
    leaves = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}" '
        f'transform="rotate({rot} {cx} {cy})"/>'
        for cx, cy, rx, ry, rot, col in [
            (560, 120, 20, 46, -25, C["teal"]), (640, 115, 20, 46, 25, C["teal_dark"]),
            (520, 170, 26, 44, -60, C["teal_dark"]), (680, 170, 26, 44, 60, C["teal"]),
            (580, 190, 24, 40, -40, C["teal"]), (620, 195, 24, 40, 40, C["teal_dark"]),
            (600, 70, 18, 40, 0, C["teal"]), (600, 150, 28, 40, 0, C["teal_dark"]),
        ]
    )
    flowers = "".join(
        f'<circle cx="{x}" cy="{y}" r="9" fill="#F7E8F1"/><circle cx="{x}" cy="{y}" r="3" fill="{C["wheat"]}"/>'
        for x, y in [(562, 128), (630, 75), (545, 180)]
    )
    potatoes = "".join(
        f'<ellipse cx="{x}" cy="262" rx="20" ry="12" fill="#E2B76A"/>' for x in (560, 600, 640)
    )
    clouds = "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w * .38}" fill="#E7E5F1" opacity=".95"/>'
        for x, y, w in [(85, 70, 70), (240, 38, 45), (870, 40, 50), (960, 65, 55), (990, 125, 40)]
    )
    people = "".join(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{col}"/>'
        f'<circle cx="{x + w / 2}" cy="{y - 10}" r="9" fill="#3A2B2B"/>'
        for x, y, w, h, col in [
            (62, 130, 28, 78, "#B97A6E"), (118, 138, 26, 72, "#E8854F"),
            (172, 158, 22, 55, "#C8664A"), (928, 150, 22, 62, "#2E7F86"),
            (965, 148, 26, 68, "#E3B341"),
        ]
    )
    return f"""
    <svg viewBox="0 0 1032 270" xmlns="http://www.w3.org/2000/svg" role="img"
         aria-label="Illustration: wheat and potato plant above soil layers">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="{C['sky']}"/><stop offset="1" stop-color="{C['sky_light']}"/>
        </linearGradient>
      </defs>
      <rect width="1032" height="270" fill="url(#sky)"/>
      {clouds}
      <path d="M0,270 L0,190 Q250,90 516,120 Q780,90 1032,190 L1032,270Z" fill="{C['peach']}"/>
      <path d="M0,270 L0,215 Q260,120 516,150 Q780,120 1032,215 L1032,270Z" fill="#F7D3BE"/>
      <path d="M0,270 L0,235 Q260,150 516,180 Q780,150 1032,235 L1032,270Z" fill="#E9A486"/>
      <path d="M0,270 L0,170 Q80,160 200,200 Q330,255 340,270Z" fill="{C['terracotta']}"/>
      <path d="M1032,270 L1032,170 Q960,165 880,205 Q850,255 840,270Z" fill="{C['terracotta']}"/>
      {wheat}{leaves}{flowers}{potatoes}{people}
    </svg>
    """


def render_banner() -> None:
    path = HERE / "assets" / "banner.png"
    if path.exists():
        b64 = base64.b64encode(path.read_bytes()).decode()
        html = f'<div class="banner"><img src="data:image/png;base64,{b64}" alt="Project banner"/></div>'
    else:
        html = f'<div class="banner">{fallback_banner_svg()}</div>'
    st.markdown(html, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Content from the project concept
# ----------------------------------------------------------------------------
RESEARCH_QUESTIONS = [
    (
        "1 · Availability and Supply Balance",
        "How do domestic production, imports, exports, stocks and domestic use change?",
        C["wheat"],
    ),
    (
        "2 · Price Stability",
        "How do the three agricultural markets differ in their vulnerability to external "
        "shocks and their capacity to adapt?",
        C["terracotta"],
    ),
    (
        "3 · Adjustment and Recovery",
        "How do supply balances and prices evolve during and after crises, and how quickly "
        "do they return toward pre-crisis conditions?",
        C["teal"],
    ),
]

RISKS = [
    (
        "Production Risks",
        "Droughts, heatwaves, floods, pests and diseases",
        "Crop yields, production volumes and domestic supply",
    ),
    (
        "Market and Price Risks",
        "Shifts in supply and demand, global commodity price shocks and market disruptions",
        "Transmission of international price changes to domestic producer prices, changes in "
        "farm revenues and production incentives",
    ),
    (
        "Input Cost Risks",
        "Energy, fertiliser, fuel and other input price increases",
        "Production costs, input use and production decisions",
    ),
    (
        "Trade and Supply Chain Risks",
        "Export restrictions, transport disruptions and logistical bottlenecks",
        "Import availability, trade flows, delivery times and transport costs",
    ),
    (
        "Financial Risks",
        "Interest rate changes, credit constraints and liquidity shortages",
        "Financing costs, investment and farm liquidity",
    ),
    (
        "Policy and Institutional Risks",
        "Changes in agricultural, trade or environmental policies",
        "Market incentives, trade conditions and production decisions",
    ),
    (
        "Geopolitical and Systemic Risks",
        "Armed conflicts, pandemics and major cross-border economic disruptions",
        "Disruptions to energy and input supplies and prices; labour shortages, interruptions "
        "to international trade, shifts in aggregate demand",
    ),
]


SUPPLY_NAMES = {
    "production": "Usable production",
    "imports": "Imports",
    "exports": "Exports",
    "domestic_use": "Domestic use",
}
SUPPLY_LINE_COLORS = {
    "production": C["teal"],
    "imports": C["sky"],
    "exports": C["wheat"],
    "domestic_use": C["terracotta"],
}
USE_NAMES = {
    "feed": "Feed",
    "industrial": "Industrial use",
    "food": "Food",
    "seed": "Seed",
    "losses": "Losses",
}
USE_COLORS = {
    "feed": C["wheat"],
    "industrial": C["terracotta"],
    "food": C["teal"],
    "seed": C["sky"],
    "losses": C["lavender"],
}
INDICATOR_NAMES = {
    "self_sufficiency": "Self-sufficiency (%)",
    "import_quota": "Import quota (%)",
    "export_quota": "Export quota (%)",
}
CROP_MAP = {
    "gerste": "Barley", "barley": "Barley",
    "kartoffeln": "Potatoes", "kartoffel": "Potatoes", "potatoes": "Potatoes", "potato": "Potatoes",
    "weichweizen": "Soft wheat", "weizen": "Soft wheat", "soft wheat": "Soft wheat",
}


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
def clean_crop(value) -> str:
    text = str(value).strip()
    return CROP_MAP.get(text.lower(), text)


def parse_year(value) -> float:
    """'1991/92' -> 1991, 2018 -> 2018."""
    match = re.match(r"\s*(\d{4})", str(value))
    return float(match.group(1)) if match else np.nan


def read_raw(src) -> pd.DataFrame:
    """Read a CSV: separator (tab, ; , |) and decimal mark (. or ,) are detected."""
    raw = src.getvalue() if hasattr(src, "getvalue") else pathlib.Path(src).read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1252", errors="replace")
    lines = text.splitlines()
    if not lines:
        raise ValueError("the file is empty")
    sep = max(["\t", ";", "|", ","], key=lines[0].count)
    if lines[0].count(sep) == 0:
        raise ValueError("could not detect the column separator")
    decimal = "," if sep != "," and re.search(r"\d,\d", text) else "."
    df = pd.read_csv(io.StringIO(text), sep=sep, decimal=decimal, skipinitialspace=True)
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df


def first_column(df: pd.DataFrame, names: tuple[str, ...], label: str) -> str:
    for name in names:
        if name in df.columns:
            return name
    raise ValueError(f"column '{label}' not found")


def read_supply(src) -> pd.DataFrame:
    """BLE supply-balance table (German names) or the English template."""
    df = read_raw(src)
    crop_col = first_column(df, ("bilanz_produkt", "crop"), "Bilanz_Produkt")
    year_col = first_column(df, ("wirtschaftsjahr", "year"), "Wirtschaftsjahr")

    def pick(*names: str) -> pd.Series:
        out = pd.Series(np.nan, index=df.index, dtype=float)
        for name in names:
            if name in df.columns:
                out = out.combine_first(pd.to_numeric(df[name], errors="coerce"))
        return out

    res = pd.DataFrame(
        {
            "crop": df[crop_col].map(clean_crop),
            "year": df[year_col].map(parse_year),
            "production": pick("verwendbare_erzeugung", "production"),
            "imports": pick("einfuhr", "imports"),
            "exports": pick("ausfuhr", "exports"),
            "domestic_use": pick(
                "inlandsverwendung_standardisiert", "domestic_use",
                "inlandsverwendung_insgesamt", "inlandsverwendung",
            ),
            "feed": pick("futter", "feed"),
            "industrial": pick("industrielle_verwertung", "industrial"),
            "food": pick("nahrungsverbrauch", "nahrungsverbrauch_in_getreidewert", "food"),
            "seed": pick("saatgut", "seed"),
            "losses": pick("verluste", "losses"),
        }
    )
    base = ["production", "imports", "exports", "domestic_use"]
    if res[base].isna().all().all():
        raise ValueError(
            "none of the expected columns found (Verwendbare_Erzeugung, Einfuhr, Ausfuhr, "
            "Inlandsverwendung_standardisiert)"
        )
    res = res.dropna(subset=["year"]).assign(year=lambda x: x["year"].astype(int))
    return add_indicators(res.drop_duplicates(["crop", "year"], keep="last"))


def read_prices(src) -> pd.DataFrame:
    df = read_raw(src)
    crop_col = first_column(df, ("crop", "bilanz_produkt", "produkt"), "crop")
    year_col = first_column(df, ("year", "wirtschaftsjahr", "jahr"), "year")
    price_col = first_column(df, ("price_eur_per_t", "preis_eur_je_t", "preis"), "price_eur_per_t")
    res = pd.DataFrame(
        {
            "crop": df[crop_col].map(clean_crop),
            "year": df[year_col].map(parse_year),
            "price_eur_per_t": pd.to_numeric(df[price_col], errors="coerce"),
        }
    ).dropna()
    res["year"] = res["year"].astype(int)
    # several rows per year (e.g. monthly prices) are averaged
    return res.groupby(["crop", "year"], as_index=False)["price_eur_per_t"].mean()


def marketing_year(ts: pd.Timestamp) -> int:
    """Marketing (BLE fiscal) year start: July–June, e.g. 2019-11-01 -> 2019 (= 2019/20)."""
    return int(ts.year if ts.month >= 7 else ts.year - 1)


def my_label(year: int) -> str:
    return f"{year}/{str(year + 1)[-2:]}"


def decimal_year(ts: pd.Timestamp) -> float:
    return ts.year + (ts.dayofyear - 1) / 365.25


def parse_list(value) -> list[str]:
    """Cells like "['a', 'b']" (Python list notation) or "a; b" -> list of strings."""
    if value is None or (not isinstance(value, (list, tuple)) and pd.isna(value)):
        return []
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value]
    try:
        parsed = ast.literal_eval(str(value))
    except (ValueError, SyntaxError):
        return [p.strip() for p in str(value).split(";") if p.strip()]
    if isinstance(parsed, (list, tuple)):
        return [str(p) for p in parsed]
    return [str(parsed)]


def read_events(src) -> list[dict]:
    """Episode table (columns as in events.csv) -> list of episode dicts."""
    df = read_raw(src)
    need = ["id", "name", "period", "analysis_start_date", "risk_categories"]
    missing = [c for c in need if c not in df.columns]
    if missing:
        raise ValueError(f"column(s) missing in events file: {', '.join(missing)}")

    def stamp(row, col):
        value = pd.to_datetime(row.get(col), errors="coerce")
        return None if pd.isna(value) else value

    def text(row, col) -> str:
        value = row.get(col)
        return "" if value is None or pd.isna(value) else str(value).strip()

    events = []
    for _, row in df.iterrows():
        win_s = stamp(row, "analysis_start_date")
        if win_s is None:
            continue
        win_e = stamp(row, "analysis_end_date")
        ev_start = stamp(row, "event_start_date")
        years = [int(y) for y in re.findall(r"\d{4}", text(row, "period"))]
        open_ended = win_e is None
        c_start = marketing_year(ev_start) if ev_start is not None else (
            years[0] if years else marketing_year(win_s)
        )
        c_end = years[-1] if years else c_start
        if not open_ended:
            c_end = min(c_end, marketing_year(win_e))
        events.append(
            dict(
                id=text(row, "id"), name=text(row, "name"), period=text(row, "period"),
                cats=parse_list(row.get("risk_categories")),
                mechs=parse_list(row.get("transmission_mechanisms")),
                type=text(row, "type"), status=text(row, "status"),
                sources=parse_list(row.get("sources")),
                rationale=text(row, "analysis_window_rationale"),
                start_status=text(row, "start_date_status") or "unknown",
                end_status=text(row, "end_date_status") or "unknown",
                event_start=ev_start, win_s=win_s, win_e=win_e, open_ended=open_ended,
                c_start=c_start, c_end=max(c_end, c_start),
                win_s_my=marketing_year(win_s),
                win_e_my=None if open_ended else marketing_year(win_e),
            )
        )
    if not events:
        raise ValueError("no usable rows in the events file")
    return events


@st.cache_data
def load_events() -> list[dict]:
    return read_events(DATA_DIR / "events.csv")


def primary_cat(event: dict) -> str:
    return event["cats"][0] if event["cats"] else "Geopolitical and Systemic Risks"


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["crop", "year"]).reset_index(drop=True)
    df["self_sufficiency"] = df["production"] / df["domestic_use"] * 100
    df["import_quota"] = df["imports"] / df["domestic_use"] * 100
    df["export_quota"] = df["exports"] / df["production"] * 100
    return df


@st.cache_data
def demo_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """SYNTHETIC data for demonstration only. Not real observations."""
    rng = np.random.default_rng(7)
    years = np.arange(1990, 2026)
    crops = {
        "Soft wheat": dict(prod=22000, imp=4500, exp=8500, use=17500, price=150, ps=1.0, qs=1.0,
                           shares=(0.45, 0.04, 0.43, 0.04, 0.04)),
        "Barley": dict(prod=11500, imp=700, exp=3000, use=9000, price=140, ps=0.9, qs=0.9,
                       shares=(0.72, 0.26, 0.01, 0.04, 0.03)),
        "Potatoes": dict(prod=10500, imp=900, exp=2600, use=8400, price=180, ps=0.55, qs=0.7,
                         shares=(0.10, 0.28, 0.55, 0.05, 0.02)),
    }
    prod_shock = {2003: -0.12, 2018: -0.15, 2019: -0.04}
    price_shock = {
        1994: 0.08, 1995: 0.18, 1996: 0.12, 2003: 0.10, 2007: 0.30, 2008: 0.38,
        2009: 0.05, 2018: 0.10, 2019: 0.04, 2021: 0.15, 2022: 0.45, 2023: 0.20, 2024: 0.06,
    }
    sup, pri = [], []
    for crop, p in crops.items():
        for y in years:
            q = prod_shock.get(int(y), 0.0) * p["qs"]
            pr = price_shock.get(int(y), 0.0) * p["ps"]
            use = p["use"] * (1 + rng.normal(0, 0.02)) * (1 + 0.2 * q)
            raw = np.array(p["shares"]) * (1 + rng.normal(0, 0.05, 5))
            parts = raw / raw.sum() * use
            sup.append(
                dict(
                    crop=crop, year=int(y),
                    production=round(p["prod"] * (1 + rng.normal(0, 0.04)) * (1 + q)),
                    imports=round(p["imp"] * (1 + rng.normal(0, 0.05)) * (1 - 1.5 * q)),
                    exports=round(p["exp"] * (1 + rng.normal(0, 0.05)) * (1 + 1.2 * q)),
                    domestic_use=round(use),
                    feed=round(parts[0]), industrial=round(parts[1]), food=round(parts[2]),
                    seed=round(parts[3]), losses=round(parts[4]),
                )
            )
            pri.append(
                dict(
                    crop=crop, year=int(y),
                    price_eur_per_t=round(
                        p["price"] * (1 + 0.012 * (y - 1990)) * (1 + pr) * (1 + rng.normal(0, 0.03)), 1
                    ),
                )
            )
    return add_indicators(pd.DataFrame(sup)), pd.DataFrame(pri)


def load_source(upload, filename: str, reader):
    """Return (dataframe or None, description or None, error or None)."""
    try:
        if upload is not None:
            return reader(upload), "uploaded file", None
        path = DATA_DIR / filename
        if path.exists():
            return reader(path), f"data/{filename}", None
    except Exception as exc:  # noqa: BLE001 - show any problem to the user
        return None, None, str(exc)
    return None, None, None


# ----------------------------------------------------------------------------
# Analysis helpers
# ----------------------------------------------------------------------------
def year_bounds(event: dict, last_year: int) -> tuple[int, int]:
    """Crisis phase as marketing-year starts (open-ended episodes run to the last data year)."""
    s = event["c_start"]
    e = last_year if event["open_ended"] else event["c_end"]
    return s, max(s, min(e, last_year))


def series_for(df: pd.DataFrame, crop: str, col: str) -> pd.Series:
    return df[df["crop"] == crop].set_index("year")[col].dropna().sort_index()


def phase_means(df, crop, cols, s, e, pre_n, post_n, relative=True) -> pd.DataFrame:
    """Phase means; change vs pre-crisis in % (volumes) or percentage points (ratios)."""
    d = df[df["crop"] == crop].set_index("year").sort_index()
    out = pd.DataFrame(
        {
            "Pre-crisis": d.loc[s - pre_n : s - 1, cols].mean(),
            "Crisis": d.loc[s : e, cols].mean(),
            "Post-crisis": d.loc[e + 1 : e + post_n, cols].mean(),
        }
    )
    if relative:
        out["Crisis vs pre (%)"] = (out["Crisis"] / out["Pre-crisis"] - 1) * 100
        out["Post vs pre (%)"] = (out["Post-crisis"] / out["Pre-crisis"] - 1) * 100
    else:
        out["Crisis vs pre (pp)"] = out["Crisis"] - out["Pre-crisis"]
        out["Post vs pre (pp)"] = out["Post-crisis"] - out["Pre-crisis"]
    return out


def price_metrics(series: pd.Series, s, e, pre_n, tol) -> dict | None:
    pre = series.loc[s - pre_n : s - 1]
    crisis = series.loc[s : e]
    if pre.empty or crisis.empty:
        return None
    base = pre.mean()
    peak_year = int(crisis.idxmax())
    peak = float(crisis.max())
    upper = base * (1 + tol)
    after = series.loc[s:]
    exceed = after[after > upper]
    if exceed.empty:
        duration, recovered = 0, "no shock above band"
    else:
        first = exceed.index[0]
        run, rec = 0, None
        for year, value in after.loc[first:].items():
            if value > upper:
                run += 1
            else:
                rec = int(year)
                break
        duration = run
        recovered = str(rec) if rec is not None else "not yet"
    return {
        "Pre-crisis mean (€/t)": round(base, 1),
        "Peak (€/t)": round(peak, 1),
        "Shock magnitude (%)": round((peak / base - 1) * 100, 1),
        "Peak year": peak_year,
        "Years from start to peak": peak_year - s,
        "Years above band": duration,
        "Back within band": recovered,
    }


def add_phases(fig: go.Figure, s: int, e: int, pre_n: int, post_n: int) -> None:
    fig.add_vrect(x0=s - pre_n - 0.5, x1=s - 0.5, fillcolor=C["sky_light"], opacity=0.25,
                  line_width=0, annotation_text="pre", annotation_position="top left")
    fig.add_vrect(x0=s - 0.5, x1=e + 0.5, fillcolor=C["terracotta"], opacity=0.15,
                  line_width=0, annotation_text="crisis", annotation_position="top left")
    fig.add_vrect(x0=e + 0.5, x1=e + post_n + 0.5, fillcolor=C["teal"], opacity=0.12,
                  line_width=0, annotation_text="post", annotation_position="top left")


def style(fig: go.Figure, height: int = 400) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Nunito, sans-serif", color=C["ink"], size=14),
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=-0.2),
        hoverlabel=dict(bgcolor=C["cream"], font_family="Nunito"),
    )
    fig.update_xaxes(gridcolor="rgba(200,102,74,.15)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(200,102,74,.15)", zeroline=False)
    return fig


def kpi(label: str, value: str, sub: str, accent: str) -> str:
    return (
        f'<div class="kpi" style="--accent:{accent}">'
        f'<div class="label">{label}</div><div class="value">{value}</div>'
        f'<div class="sub">{sub}</div></div>'
    )


try:
    EVENTS = load_events()
except Exception as exc:  # noqa: BLE001
    st.error(f"The episode table dashboard/data/events.csv could not be read: {exc}")
    st.stop()
EVENT_LABELS = [f"{e['id']} · {e['name']}" for e in EVENTS]

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.header("🌾 Settings")
    st.subheader("Crisis episode")
    event_idx = st.selectbox(
        "Episode to analyse", range(len(EVENTS)), index=min(5, len(EVENTS) - 1), format_func=lambda i: EVENT_LABELS[i]
    )
    pre_n = st.slider("Pre-crisis window (years)", 1, 5, 2)
    post_n = st.slider("Post-crisis window (years)", 1, 5, 2)
    tol = st.slider("Recovery tolerance band (%)", 5, 30, 10) / 100

    st.subheader("Data")
    supply_up = st.file_uploader("Supply balance (CSV)", type="csv", key="supply_up")
    price_up = st.file_uploader("Prices (CSV)", type="csv", key="price_up")

event = EVENTS[event_idx]

supply, supply_src, supply_err = load_source(supply_up, "supply_balance.csv", read_supply)
prices, price_src, price_err = load_source(price_up, "prices.csv", read_prices)
demo_supply, demo_prices = demo_data()
supply_is_demo, prices_is_demo = supply is None, prices is None
if supply is None:
    supply = demo_supply
if prices is None:
    prices = demo_prices

with st.sidebar:
    for err, name in [(supply_err, "Supply balance"), (price_err, "Prices")]:
        if err:
            st.error(f"{name} file could not be used ({err}). Showing demo data instead.")
    st.caption(
        f"Supply balance: {'DEMO data' if supply_is_demo else supply_src}  \n"
        f"Prices: {'DEMO data' if prices_is_demo else price_src}"
    )

crops_all = sorted(set(supply["crop"]) | set(prices["crop"]))
last_year = int(max(supply["year"].max(), prices["year"].max()))
s_year, e_year = year_bounds(event, last_year)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
render_banner()
st.title("Agricultural Market Resilience in Germany")
st.caption("A comparative analysis of soft wheat, barley and potato markets")

if supply_is_demo or prices_is_demo:
    st.warning(
        "**Demo mode:** the supply-balance and/or price charts currently use **synthetic "
        "example data**, not real observations. Upload your BLE / price CSV files in the "
        "sidebar (see tab *Data & method*) to see real results.",
        icon="⚠️",
    )

tab_over, tab_risk, tab_time, tab_long, tab_supply, tab_price, tab_comp, tab_data = st.tabs(
    [
        "🌱 Overview",
        "⚠️ Risk framework",
        "🕰️ Timeline",
        "📈 Long-term view",
        "📦 Supply balance",
        "💶 Prices & recovery",
        "🔀 Crisis comparison",
        "📥 Data & method",
    ]
)

# ----------------------------------------------------------------------------
# Overview
# ----------------------------------------------------------------------------
with tab_over:
    st.subheader("Project overview")
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi("Commodities", "3", "Soft wheat · Barley · Potatoes", C["wheat"]), unsafe_allow_html=True)
    k2.markdown(kpi("Risk categories", str(len(RISKS)), "OECD / FAO-based synthesis", C["terracotta"]), unsafe_allow_html=True)
    k3.markdown(kpi("Episodes", str(len(EVENTS)), "1990 – 2026", C["teal"]), unsafe_allow_html=True)
    k4.markdown(kpi("Phases", "3", "pre-crisis · crisis · post-crisis", C["sky"]), unsafe_allow_html=True)

    st.write("")
    p1, p2 = st.columns(2)
    with p1:
        with st.container(border=True):
            st.markdown("#### Problem")
            st.write(
                "Agricultural markets are exposed to external shocks that can disrupt supply "
                "chains, increase price volatility, and affect domestic production and trade. "
                "The effects may differ across commodities, as markets vary in their "
                "vulnerability and capacity to adjust. Comparing soft wheat, barley and potato "
                "markets in Germany provides insights into these differences and their "
                "implications for market resilience."
            )
    with p2:
        with st.container(border=True):
            st.markdown("#### Goal and approach")
            st.write(
                "Analyse the economic mechanisms of the selected commodities across three "
                "dimensions and throughout the pre-crisis, crisis and post-crisis phases. "
                "Approach: data collection and preparation, exploratory analysis, and "
                "visualisation of market and price dynamics as well as international trade "
                "dependencies, to investigate shock magnitude, response timing, shock duration "
                "and recovery patterns."
            )

    st.markdown("#### Research questions")
    cols = st.columns(3)
    for col, (title, text, accent) in zip(cols, RESEARCH_QUESTIONS):
        col.markdown(
            f'<div class="qcard" style="--accent:{accent}"><h4>{title}</h4><p>{text}</p></div>',
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------------
# Risk framework
# ----------------------------------------------------------------------------
with tab_risk:
    st.subheader("Conceptual framework: risk categories and transmission mechanisms")
    st.info(
        "There is no single universally applicable classification of crises affecting "
        "agricultural markets. The categories below are a structured synthesis informed by the "
        "OECD agricultural risk management framework and FAO work on agricultural supply "
        "chains, not a verbatim reproduction of one official taxonomy. They may overlap."
    )
    chosen = st.multiselect(
        "Show risk categories",
        [r[0] for r in RISKS],
        default=[r[0] for r in RISKS],
        key="risk_filter",
    )
    for cat, drivers, mech in RISKS:
        if cat not in chosen:
            continue
        with st.container(border=True):
            st.markdown(
                f'<span class="chip" style="background:{CAT_COLORS[cat]}">{cat}</span>',
                unsafe_allow_html=True,
            )
            a, b = st.columns(2)
            a.markdown(f"**Examples of risk drivers**  \n{drivers}")
            b.markdown(f"**Potential transmission mechanisms**  \n{mech}")
    st.markdown(
        '<p class="footnote">Conceptual sources: OECD (2020), Strengthening Agricultural '
        "Resilience in the Face of Multiple Risks · FAO, Guidelines to Increase the Resilience "
        "of Agricultural Supply Chains. Additional sources: FAO – Agricultural Commodity "
        "Markets · European Commission – Fertiliser Markets · UNCTAD – Maritime Trade "
        "Disruptions.</p>",
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# Timeline
# ----------------------------------------------------------------------------
with tab_time:
    st.subheader("Crisis episodes and analysis windows (1990–2026)")
    cat_filter = st.multiselect(
        "Filter by risk category",
        list(CAT_COLORS),
        default=list(CAT_COLORS),
        key="time_filter",
    )
    shown = [e for e in EVENTS if set(e["cats"]) & set(cat_filter)]
    fig = go.Figure()
    seen: set[str] = set()
    marker_shown = False
    for e in shown:
        primary = primary_cat(e)
        x0 = decimal_year(e["win_s"])
        x1 = 2026.8 if e["open_ended"] else decimal_year(e["win_e"])
        short = e["name"] if len(e["name"]) <= 40 else e["name"][:39] + "…"
        ylabel = f"{e['id']} · {short}"
        end_txt = "open" if e["open_ended"] else f"{e['win_e']:%b %Y}"
        highlighted = e is event
        fig.add_trace(
            go.Bar(
                y=[ylabel], x=[x1 - x0], base=[x0], orientation="h",
                name=primary, legendgroup=primary, showlegend=primary not in seen,
                marker=dict(
                    color=CAT_COLORS.get(primary, C["ink"]),
                    line=dict(color="#4A4766" if highlighted else C["card"], width=3 if highlighted else 1),
                    pattern=dict(shape="/" if e["open_ended"] else ""),
                ),
                hovertemplate=(
                    f"<b>{e['id']} · {e['name']}</b><br>Analysis window: "
                    f"{e['win_s']:%b %Y} – {end_txt}<br>{', '.join(e['cats'])}<extra></extra>"
                ),
            )
        )
        seen.add(primary)
        if e["event_start"] is not None:
            fig.add_trace(
                go.Scatter(
                    x=[decimal_year(e["event_start"])], y=[ylabel], mode="markers",
                    marker=dict(symbol="diamond", size=12, color=C["ink"],
                                line=dict(color="#fff", width=1)),
                    name="Documented event start", legendgroup="start",
                    showlegend=not marker_shown,
                    hovertemplate=f"Event start: {e['event_start']:%d %b %Y}<extra></extra>",
                )
            )
            marker_shown = True
    fig.add_vline(x=2026.8, line_dash="dot", line_color=C["ink"],
                  annotation_text="Oct 2026", annotation_position="top")
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[1989, 2028], dtick=5, tickformat="d")
    fig.update_layout(
        title="Analysis windows by episode (colour = primary risk category, hatched = open-ended)"
    )
    with st.container(border=True):
        st.plotly_chart(style(fig, 160 + 36 * max(len(shown), 1)), width="stretch")

    st.markdown(f"#### Details: {EVENT_LABELS[event_idx]}")
    with st.container(border=True):
        chips = "".join(
            f'<span class="chip" style="background:{CAT_COLORS.get(c, C["ink"])}">{c}</span>'
            for c in event["cats"]
        )
        st.markdown(chips, unsafe_allow_html=True)
        st.markdown(f"**Period:** {event['period']} · **Type:** {event['type']} · **Status:** {event['status']}")
        if event["mechs"]:
            st.markdown("**Potential transmission mechanisms (hypotheses)**")
            st.markdown("\n".join(f"- {m}" for m in event["mechs"]))
        st.markdown(f"**Analysis window:** {event['rationale']}")
        start_txt = f"{event['event_start']:%d %b %Y}" if event["event_start"] is not None else "not set"
        st.markdown(
            f"**Date quality:** event start {start_txt} ({event['start_status']}) · "
            f"event end ({event['end_status']})"
        )
        if event["sources"]:
            st.markdown("**Sources**")
            st.markdown("\n".join(f"- <{u}>" if u.startswith("http") else f"- {u}" for u in event["sources"]))
        end_my = "open end" if event["open_ended"] else my_label(event["win_e_my"])
        st.caption(
            f"Analysis window in marketing years: {my_label(event['win_s_my'])} to {end_my}. "
            f"Crisis phase in the charts: {my_label(s_year)} to {my_label(e_year)} "
            "(derived from the event dates and period). Change the episode in the sidebar. "
            "Mechanisms are hypotheses, not established causal effects."
        )

# ----------------------------------------------------------------------------
# Long-term view
# ----------------------------------------------------------------------------
with tab_long:
    st.subheader("Long-term development against the background of crises")
    if supply_is_demo or prices_is_demo:
        st.caption("⚠️ Synthetic demo data (at least one of the data sets)")
    METRICS = {
        "Usable production (1,000 t)": ("supply", "production"),
        "Domestic use (1,000 t)": ("supply", "domestic_use"),
        "Imports (1,000 t)": ("supply", "imports"),
        "Exports (1,000 t)": ("supply", "exports"),
        "Self-sufficiency (%)": ("supply", "self_sufficiency"),
        "Import quota (%)": ("supply", "import_quota"),
        "Export quota (%)": ("supply", "export_quota"),
        "Price (€ per t)": ("prices", "price_eur_per_t"),
    }
    lc1, lc2 = st.columns([2, 3])
    metric = lc1.selectbox("Indicator", list(METRICS), key="long_metric")
    crops_l = lc2.multiselect("Commodities", crops_all, default=crops_all, key="long_crops")
    ev_sel = st.multiselect(
        "Episodes shown as background", list(range(len(EVENTS))),
        default=list(range(len(EVENTS))), format_func=lambda i: EVENT_LABELS[i], key="long_events",
    )
    as_index = st.checkbox("Index the series (mean of the first three years = 100)", key="long_index")

    table_name, column = METRICS[metric]
    source = supply if table_name == "supply" else prices
    fig = go.Figure()
    for crop in crops_l:
        ser = series_for(source, crop, column)
        if ser.empty:
            continue
        if as_index:
            ser = ser / ser.iloc[:3].mean() * 100
        fig.add_trace(
            go.Scatter(
                x=ser.index, y=ser.values, name=crop, mode="lines",
                line=dict(color=CROP_COLORS.get(crop, C["ink"]), width=3),
                hovertemplate="%{y:,.1f}<extra>" + crop + "</extra>",
            )
        )
    for i in ev_sel:
        ev = EVENTS[i]
        s0, e0 = year_bounds(ev, last_year)
        fig.add_vrect(
            x0=s0 - 0.5, x1=e0 + 0.5, fillcolor=CAT_COLORS.get(primary_cat(ev), C["ink"]),
            opacity=0.18, line_width=0, layer="below",
            annotation_text=ev["id"], annotation_position="top left", annotation_font_size=10,
        )
    if table_name == "supply" and column == "self_sufficiency" and not as_index:
        fig.add_hline(y=100, line_dash="dot", line_color=C["ink"])
    fig.update_layout(
        title=f"{metric}{' (indexed)' if as_index else ''}: shaded bands = crisis phases "
        "(colour = primary risk category)"
    )
    fig.update_xaxes(tickformat="d", title_text="Marketing year (1991 = 1991/92)")
    with st.container(border=True):
        st.plotly_chart(style(fig, 470), width="stretch")
    st.caption(
        "Crisis phases are the marketing years in which an episode is assumed to act "
        "(see tab Timeline). Overlapping episodes are drawn on top of each other. "
        "Temporal overlap alone does not establish causality."
    )

# ----------------------------------------------------------------------------
# Supply balance
# ----------------------------------------------------------------------------
def change_chart(table: pd.DataFrame, crisis_col: str, post_col: str, title: str, unit: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=list(table.index), y=table[crisis_col], name="Crisis vs pre-crisis",
            marker_color=C["terracotta"],
            hovertemplate="%{y:+.1f} " + unit + "<extra>Crisis</extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=list(table.index), y=table[post_col], name="Post-crisis vs pre-crisis",
            marker_color=C["teal"],
            hovertemplate="%{y:+.1f} " + unit + "<extra>Post-crisis</extra>",
        )
    )
    fig.add_hline(y=0, line_color=C["ink"], line_width=1)
    fig.update_layout(barmode="group", title=title)
    fig.update_yaxes(ticksuffix=" " + unit)
    return fig


with tab_supply:
    st.subheader("Availability and supply balance")
    if supply_is_demo:
        st.caption("⚠️ Synthetic demo data")
    crop_s = st.selectbox("Commodity", sorted(supply["crop"].unique()), key="crop_supply")
    d = supply[supply["crop"] == crop_s].set_index("year").sort_index()

    c1, c2 = st.columns([3, 2])
    with c1:
        fig = go.Figure()
        for col, name in SUPPLY_NAMES.items():
            fig.add_trace(
                go.Scatter(
                    x=d.index, y=d[col], name=name, mode="lines",
                    line=dict(color=SUPPLY_LINE_COLORS[col], width=3),
                    hovertemplate="%{y:,.0f}<extra>" + name + "</extra>",
                )
            )
        add_phases(fig, s_year, e_year, pre_n, post_n)
        fig.update_layout(title=f"{crop_s}: supply balance (1,000 t)")
        fig.update_xaxes(tickformat="d", title_text="Marketing year (1991 = 1991/92)")
        with st.container(border=True):
            st.plotly_chart(style(fig, 420), width="stretch")
    with c2:
        fig = go.Figure(
            go.Scatter(
                x=d.index, y=d["self_sufficiency"], mode="lines+markers",
                line=dict(color=CROP_COLORS.get(crop_s, C["terracotta"]), width=3),
                hovertemplate="%{y:.0f} %<extra>Self-sufficiency</extra>",
            )
        )
        fig.add_hline(y=100, line_dash="dot", line_color=C["ink"])
        add_phases(fig, s_year, e_year, pre_n, post_n)
        fig.update_layout(title="Self-sufficiency: usable production ÷ domestic use (%)", showlegend=False)
        fig.update_xaxes(tickformat="d", title_text="Marketing year (1991 = 1991/92)")
        with st.container(border=True):
            st.plotly_chart(style(fig, 420), width="stretch")

    c3, c4 = st.columns([3, 2])
    with c3:
        use_cols = [c for c in USE_NAMES if c in d.columns and d[c].notna().any()]
        if use_cols:
            fig = go.Figure()
            for col in use_cols:
                fig.add_trace(
                    go.Bar(
                        x=d.index, y=d[col], name=USE_NAMES[col],
                        marker_color=USE_COLORS[col],
                        hovertemplate="%{y:,.0f}<extra>" + USE_NAMES[col] + "</extra>",
                    )
                )
            fig.update_layout(barmode="stack", title=f"{crop_s}: what domestic use consists of (1,000 t)")
            add_phases(fig, s_year, e_year, pre_n, post_n)
            fig.update_xaxes(tickformat="d", title_text="Marketing year (1991 = 1991/92)")
            with st.container(border=True):
                st.plotly_chart(style(fig, 400), width="stretch")
        else:
            st.info("No columns for the use breakdown (feed, industrial use, food, seed, losses) in this data set.")
    with c4:
        fig = go.Figure()
        for col, color in [("import_quota", C["sky"]), ("export_quota", C["wheat"])]:
            fig.add_trace(
                go.Scatter(
                    x=d.index, y=d[col], name=INDICATOR_NAMES[col], mode="lines",
                    line=dict(color=color, width=3),
                    hovertemplate="%{y:.1f} %<extra>" + INDICATOR_NAMES[col] + "</extra>",
                )
            )
        add_phases(fig, s_year, e_year, pre_n, post_n)
        fig.update_layout(title="Trade dependence: import and export quota (%)")
        fig.update_xaxes(tickformat="d", title_text="Marketing year (1991 = 1991/92)")
        with st.container(border=True):
            st.plotly_chart(style(fig, 400), width="stretch")

    st.markdown(f"#### Phase comparison: {EVENT_LABELS[event_idx]}")
    vol = phase_means(supply, crop_s, list(SUPPLY_NAMES), s_year, e_year, pre_n, post_n).rename(
        index=SUPPLY_NAMES
    )
    ind = phase_means(
        supply, crop_s, list(INDICATOR_NAMES), s_year, e_year, pre_n, post_n, relative=False
    ).rename(index=INDICATOR_NAMES)
    if vol[["Pre-crisis", "Crisis"]].isna().all().any():
        st.info("Not enough observations for the selected episode and windows in this data set.")
    else:
        p1, p2 = st.columns(2)
        with p1:
            fig = change_chart(vol, "Crisis vs pre (%)", "Post vs pre (%)",
                               "Volumes: change vs pre-crisis mean (%)", "%")
            with st.container(border=True):
                st.plotly_chart(style(fig, 380), width="stretch")
        with p2:
            fig = change_chart(ind, "Crisis vs pre (pp)", "Post vs pre (pp)",
                               "Indicators: change vs pre-crisis mean (percentage points)", "pp")
            with st.container(border=True):
                st.plotly_chart(style(fig, 380), width="stretch")
        st.caption(
            f"Phase means. Pre-crisis: {s_year - pre_n}–{s_year - 1}, "
            f"crisis: {s_year}–{e_year}, post-crisis: {e_year + 1}–{e_year + post_n}. "
            "Volumes are assumed to be in 1,000 t. Calendar-year events are matched to the "
            "starting year of the marketing year (e.g. 2018 = 2018/19)."
        )

# ----------------------------------------------------------------------------
# Prices & recovery
# ----------------------------------------------------------------------------

with tab_price:
    st.subheader("Price stability, adjustment and recovery")
    if prices_is_demo:
        st.caption("⚠️ Synthetic demo data")
    sel = st.multiselect(
        "Commodities", sorted(prices["crop"].unique()),
        default=sorted(prices["crop"].unique()), key="crops_price",
    )
    fig = go.Figure()
    rows = {}
    lo, hi = s_year - pre_n - 1, e_year + post_n + 2
    for crop in sel:
        ser = series_for(prices, crop, "price_eur_per_t")
        pre = ser.loc[s_year - pre_n : s_year - 1]
        if pre.empty:
            continue
        idx = (ser / pre.mean() * 100).loc[lo:hi]
        fig.add_trace(
            go.Scatter(
                x=idx.index, y=idx.values, name=crop, mode="lines+markers",
                line=dict(color=CROP_COLORS.get(crop, C["ink"]), width=3),
                hovertemplate="%{y:.0f}<extra>" + crop + "</extra>",
            )
        )
        m = price_metrics(ser, s_year, e_year, pre_n, tol)
        if m:
            rows[crop] = m
    fig.add_hline(y=100, line_dash="dot", line_color=C["ink"])
    fig.add_hline(y=100 * (1 + tol), line_dash="dash", line_color=C["terracotta_dark"],
                  annotation_text="tolerance band", annotation_position="top right")
    add_phases(fig, s_year, e_year, pre_n, post_n)
    fig.update_layout(title=f"Price index (pre-crisis mean = 100) · {EVENT_LABELS[event_idx]}")
    fig.update_xaxes(tickformat="d", title_text="Marketing year (1991 = 1991/92)")
    with st.container(border=True):
        st.plotly_chart(style(fig, 440), width="stretch")

    if rows:
        names = list(rows)
        colors = [CROP_COLORS.get(n, C["ink"]) for n in names]
        st.markdown("#### Shock magnitude, timing, duration and recovery")
        cards = st.columns(len(names))
        for col, n in zip(cards, names):
            m = rows[n]
            col.markdown(
                kpi(
                    n,
                    f"{m['Shock magnitude (%)']:+.0f} %",
                    f"peak {m['Peak year']} · back within band: {m['Back within band']}",
                    CROP_COLORS.get(n, C["ink"]),
                ),
                unsafe_allow_html=True,
            )
        st.write("")
        r1, r2 = st.columns(2)
        with r1:
            fig = go.Figure(
                go.Bar(
                    x=names, y=[rows[n]["Shock magnitude (%)"] for n in names],
                    marker_color=colors,
                    text=[f"peak {rows[n]['Peak year']}" for n in names],
                    textposition="outside",
                    hovertemplate="%{y:+.1f} %<extra></extra>",
                )
            )
            fig.update_layout(title="Shock magnitude: peak vs pre-crisis mean (%)", showlegend=False)
            fig.update_yaxes(ticksuffix=" %")
            with st.container(border=True):
                st.plotly_chart(style(fig, 360), width="stretch")
        with r2:
            fig = go.Figure(
                go.Bar(
                    x=names, y=[rows[n]["Years above band"] for n in names],
                    marker_color=colors,
                    text=[f"timing: {rows[n]['Years from start to peak']} y to peak" for n in names],
                    textposition="outside",
                    hovertemplate="%{y} years above band<extra></extra>",
                )
            )
            fig.update_layout(title="Shock duration: years above tolerance band", showlegend=False)
            fig.update_yaxes(dtick=1)
            with st.container(border=True):
                st.plotly_chart(style(fig, 360), width="stretch")
        st.caption(
            f"A shock is counted while the price stays more than {tol * 100:.0f} % above the "
            "pre-crisis mean. Prices are nominal; consider deflating them before drawing "
            "conclusions about real price changes."
        )
    else:
        st.info("Not enough price observations for the selected episode and windows.")

# ----------------------------------------------------------------------------
# Comparison
# ----------------------------------------------------------------------------

with tab_comp:
    st.subheader("Resilience compared across crises")
    if supply_is_demo or prices_is_demo:
        st.caption("⚠️ Synthetic demo data (at least one of the data sets)")
    crops_c = [c for c in crops_all if c in set(supply["crop"]) | set(prices["crop"])]
    ids = [e["id"] for e in EVENTS]
    names = [e["name"] for e in EVENTS]
    prod_change = np.full((len(crops_c), len(EVENTS)), np.nan)
    price_shock = np.full((len(crops_c), len(EVENTS)), np.nan)
    for j, ev in enumerate(EVENTS):
        s0, e0 = year_bounds(ev, last_year)
        for i, crop in enumerate(crops_c):
            ser = series_for(supply, crop, "production")
            pre, cri = ser.loc[s0 - pre_n : s0 - 1], ser.loc[s0:e0]
            if len(pre) and len(cri):
                prod_change[i, j] = (cri.mean() / pre.mean() - 1) * 100
            m = price_metrics(series_for(prices, crop, "price_eur_per_t"), s0, e0, pre_n, tol)
            if m:
                price_shock[i, j] = m["Shock magnitude (%)"]

    custom = np.array([names] * len(crops_c))
    h1, h2 = st.columns(2)
    with h1:
        lim = float(np.nanmax(np.abs(prod_change))) if np.isfinite(prod_change).any() else 1.0
        fig = go.Figure(
            go.Heatmap(
                z=prod_change, x=ids, y=crops_c, customdata=custom, zmin=-lim, zmax=lim, zmid=0,
                colorscale=[[0, C["terracotta"]], [0.5, C["cream"]], [1, C["teal"]]],
                texttemplate="%{z:+.0f}", xgap=3, ygap=3,
                colorbar=dict(title="%"),
                hovertemplate="<b>%{x}</b> %{customdata}<br>%{y}: %{z:+.1f} %<extra></extra>",
            )
        )
        fig.update_layout(title="Usable production: crisis phase vs pre-crisis mean (%)")
        fig.update_xaxes(side="top")
        fig.update_yaxes(autorange="reversed")
        with st.container(border=True):
            st.plotly_chart(style(fig, 280 + 40 * len(crops_c)), width="stretch")
    with h2:
        top = float(np.nanmax(price_shock)) if np.isfinite(price_shock).any() else 1.0
        fig = go.Figure(
            go.Heatmap(
                z=price_shock, x=ids, y=crops_c, customdata=custom, zmin=0, zmax=max(top, 1.0),
                colorscale=[[0, C["cream"]], [0.5, C["peach_dark"]], [1, C["terracotta_dark"]]],
                texttemplate="%{z:+.0f}", xgap=3, ygap=3,
                colorbar=dict(title="%"),
                hovertemplate="<b>%{x}</b> %{customdata}<br>%{y}: %{z:+.1f} %<extra></extra>",
            )
        )
        fig.update_layout(title="Price shock: peak vs pre-crisis mean (%)")
        fig.update_xaxes(side="top")
        fig.update_yaxes(autorange="reversed")
        with st.container(border=True):
            st.plotly_chart(style(fig, 280 + 40 * len(crops_c)), width="stretch")
    st.caption(
        f"Pre-crisis window: {pre_n} marketing year(s). Empty cells: no observations for that "
        "episode in the data set (e.g. episodes before the first or after the last data year). "
        "Prices are nominal. Hover over a cell to see the episode name."
    )

# ----------------------------------------------------------------------------
# Data & method
# ----------------------------------------------------------------------------

with tab_data:
    st.subheader("Data format")
    st.write(
        "Upload CSV files in the sidebar, or place them in the folder `dashboard/data/` as "
        "`supply_balance.csv` and `prices.csv`. Column separators (tab, `;`, `,`) and decimal "
        "commas are detected automatically."
    )
    a, b = st.columns(2)
    with a:
        with st.container(border=True):
            st.markdown("**supply_balance.csv: the BLE table works as it is**")
            st.markdown(
                "Used columns: `Wirtschaftsjahr` (e.g. 1991/92), `Bilanz_Produkt` "
                "(Gerste, Kartoffeln, Weichweizen), `Verwendbare_Erzeugung`, `Einfuhr`, "
                "`Ausfuhr`, `Inlandsverwendung_standardisiert`; for the use breakdown "
                "`Futter`, `Industrielle_Verwertung`, `Nahrungsverbrauch` "
                "(cereals: `Nahrungsverbrauch_in_Getreidewert`), `Saatgut`, `Verluste`. "
                "Self-sufficiency, import quota and export quota are computed from these."
            )
            st.download_button(
                "⬇️ Download minimal template",
                "Wirtschaftsjahr;Bilanz_Produkt;Verwendbare_Erzeugung;Einfuhr;Ausfuhr;Inlandsverwendung_standardisiert\n",
                file_name="supply_balance.csv", mime="text/csv", key="dl_supply",
            )
    with b:
        with st.container(border=True):
            st.markdown("**prices.csv (€ per tonne, one value per year)**")
            st.code("crop,year,price_eur_per_t", language="text")
            st.markdown(
                "`crop`: Soft wheat / Weichweizen, Barley / Gerste, Potatoes / Kartoffeln. "
                "`year`: calendar year or marketing year (1991/92 or 1991). Several rows per "
                "year (e.g. months) are averaged."
            )
            st.download_button(
                "⬇️ Download template",
                "crop,year,price_eur_per_t\n",
                file_name="prices.csv", mime="text/csv", key="dl_prices",
            )

    with st.container(border=True):
        st.markdown("**events.csv: the crisis episodes (already included)**")
        st.markdown(
            "Stored in `dashboard/data/events.csv` and read at every start. Columns: `id`, `name`, "
            "`period`, `event_start_date`, `event_end_date`, `analysis_start_date`, "
            "`analysis_end_date` (empty = open-ended), `risk_categories`, "
            "`transmission_mechanisms`, `type`, `status`, `sources`, `analysis_window_rationale`, "
            "`start_date_status`, `end_date_status`. Edit the file to add or change episodes. "
            "Crisis phase = marketing years (July–June) derived from the event start date or the "
            "years in `period`, clipped to the analysis window."
        )

    st.subheader("Methodological note")
    st.markdown(
        "- The risk categories are an analytical synthesis informed by the OECD framework and "
        "FAO work on agricultural supply chains, not a standardised official taxonomy.\n"
        "- The listed transmission mechanisms are **hypotheses**, not established causal "
        "effects. Their relevance must be assessed with product-specific evidence and the "
        "observed BLE supply-balance indicators.\n"
        "- Calendar-year events must be aligned carefully with BLE financial-year "
        "observations (e.g. 2018/19). Annual harvest outcomes are treated as empirical "
        "observations, not classified as crises by default.\n"
        "- The 2026 entry reflects information available as of October 2026 and should be "
        "updated as new evidence becomes available.\n\n"
        "Framework source: OECD (2020), *Strengthening Agricultural Resilience in the Face of "
        "Multiple Risks*, https://doi.org/10.1787/2250453e-en"
    )
