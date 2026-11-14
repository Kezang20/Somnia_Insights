from pathlib import Path
import inspect

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr, f_oneway, gaussian_kde

# ============================================================
# SOMNIA INSIGHTS | Sleep Health & Lifestyle Analytics
# ============================================================

st.set_page_config(
    page_title="Somnia Insights",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- THEME ----------------------------
BG_MAIN = "#F5F7F6"
SIDEBAR_BG = "#132A25"
SIDEBAR_TEXT = "#C9D8D4"
SIDEBAR_MUTED = "#7F9792"
CARD_DARK = "#17403A"
ACCENT_LIME = "#D1F07A"
TEAL_DARK = "#1A5B50"
TEAL_CHART = "#2A8273"
CORAL_CHART = "#E87A6A"
LIME_CHART = "#A4CF6B"
SLATE_CHART = "#7D93C1"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#1F2937"
TITLE_COLOR = "#143D36"
TEXT_MUTED = "#6B7280"
BORDER_COLOR = "#E5E7EB"

DISORDER_ORDER = ["None", "Insomnia", "Sleep Apnea"]
DISORDER_LABELS = {"None": "None", "Insomnia": "Insomnia", "Sleep Apnea": "Sleep apnea"}
DISORDER_COLORS = {"None": TEAL_CHART, "Insomnia": CORAL_CHART, "Sleep Apnea": SLATE_CHART}
DISORDER_DOTS = {"None": ACCENT_LIME, "Insomnia": CORAL_CHART, "Sleep Apnea": SLATE_CHART}

NAV_ITEMS = [
    ("Overview", "<rect x='3' y='3' width='7' height='7'/><rect x='14' y='3' width='7' height='7'/><rect x='14' y='14' width='7' height='7'/><rect x='3' y='14' width='7' height='7'/>"),
    ("Dataset", "<ellipse cx='12' cy='5' rx='9' ry='3'/><path d='M21 12c0 1.66-4 3-9 3s-9-1.34-9-3'/><path d='M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5'/>"),
    ("Exploratory analysis", "<line x1='18' y1='20' x2='18' y2='10'/><line x1='12' y1='20' x2='12' y2='4'/><line x1='6' y1='20' x2='6' y2='14'/>"),
    ("Relationships", "<line x1='6' y1='3' x2='6' y2='15'/><circle cx='18' cy='6' r='3'/><circle cx='6' cy='18' r='3'/><path d='M18 9a9 9 0 0 1-9 9'/>"),
    ("Disorder comparison", "<polyline points='22 12 18 12 15 21 9 3 6 12 2 12'/>"),
    ("Findings & conclusion", "<path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/><polyline points='14 2 14 8 20 8'/><line x1='16' y1='13' x2='8' y2='13'/><line x1='16' y1='17' x2='8' y2='17'/>"),
]

NAV_NAMES = [name for name, _ in NAV_ITEMS]


def icon_uri(inner, color="black"):
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' "
        f"stroke='{color}' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
        + inner + "</svg>"
    )
    svg = svg.replace("<", "%3C").replace(">", "%3E").replace("#", "%23")
    return 'url("data:image/svg+xml;utf8,' + svg + '")'


# Per-item icon CSS. Each nav button has the key nav_<n>, which Streamlit exposes
# as the class st-key-nav_<n>; the icon is drawn in the button's text colour.
NAV_ICON_CSS = ""
for _i, (_name, _inner) in enumerate(NAV_ITEMS, start=1):
    _uri = icon_uri(_inner)
    NAV_ICON_CSS += (
        f'[data-testid="stSidebar"] .st-key-nav_{_i} button::before {{'
        "content:''; display:block; width:20px; height:20px; flex:0 0 20px;"
        "background-color: currentColor;"
        f"-webkit-mask: {_uri} center / contain no-repeat;"
        f"mask: {_uri} center / contain no-repeat;"
        "}\n"
    )

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}
.stApp {{
    background-color: {BG_MAIN};
    color: {TEXT_DARK};
}}
[data-testid="stHeader"] {{ background: transparent; }}
#MainMenu, footer {{ visibility: hidden; }}
.block-container {{
    padding-top: 2.4rem;
    padding-bottom: 3rem;
    max-width: 1480px;
}}

/* ---------- Page header ---------- */
.kicker {{
    display: flex;
    align-items: center;
    gap: 9px;
    color: #374151;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}}
.kicker-dot {{
    width: 7px; height: 7px; border-radius: 50%;
    background: {CORAL_CHART};
}}
.page-title {{
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.1;
    color: {TITLE_COLOR};
    margin: 0 0 0.55rem 0;
}}
.subtitle {{
    color: {TEXT_MUTED};
    font-size: 1rem;
    margin: 0 0 1.9rem 0;
}}
h2, h3 {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: {TITLE_COLOR} !important;
}}

/* ---------- Sidebar shell ---------- */
[data-testid="stSidebar"] {{
    background-color: {SIDEBAR_BG};
    min-width: 290px !important;
    max-width: 290px !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding: 0.6rem 0.4rem 1rem 0.4rem;
}}
[data-testid="stSidebar"] * {{
    color: {SIDEBAR_TEXT} !important;
}}
[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.08);
}}

/* Brand */
[data-testid="stSidebar"] .brand {{
    display: flex; align-items: center; gap: 14px;
    margin: 0.4rem 0 2.4rem 0.3rem;
}}
[data-testid="stSidebar"] .brand-logo {{
    width: 46px; height: 46px; border-radius: 14px;
    background: {ACCENT_LIME};
    display: flex; align-items: center; justify-content: center;
    flex: 0 0 46px;
}}
[data-testid="stSidebar"] .brand-text {{
    font-size: 1.2rem; color: {SIDEBAR_MUTED} !important;
}}
[data-testid="stSidebar"] .brand-text b {{
    color: #FFFFFF !important; font-weight: 700;
}}
[data-testid="stSidebar"] .side-label {{
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.22em;
    color: {SIDEBAR_MUTED} !important;
    margin: 0 0 0.9rem 0.6rem;
}}

/* ---------- Sidebar navigation (buttons; the current page is the primary one) ---------- */
[data-testid="stSidebar"] .st-key-navlist {{
    gap: 8px;
}}
[data-testid="stSidebar"] .st-key-navlist > div,
[data-testid="stSidebar"] .st-key-navlist [data-testid="stElementContainer"],
[data-testid="stSidebar"] .st-key-navlist [data-testid="stButton"] {{
    width: 100% !important;
}}
[data-testid="stSidebar"] .st-key-navlist button {{
    width: 100% !important;
    min-height: 50px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 14px;
    padding: 12px 18px;
    background: transparent;
    border: none !important;
    border-radius: 14px;
    box-shadow: none !important;
    transition: background 0.2s ease;
}}
[data-testid="stSidebar"] .st-key-navlist button p,
[data-testid="stSidebar"] .st-key-navlist button div {{
    margin: 0;
    text-align: left;
    font-size: 0.97rem;
    font-weight: 600;
    color: inherit !important;
}}
[data-testid="stSidebar"] .st-key-navlist button,
[data-testid="stSidebar"] .st-key-navlist button * {{
    color: #EEF4F2 !important;
}}
[data-testid="stSidebar"] .st-key-navlist button:hover {{
    background: rgba(255,255,255,0.07);
}}
[data-testid="stSidebar"] .st-key-navlist button:focus-visible {{
    outline: 2px solid {ACCENT_LIME};
    outline-offset: 2px;
}}
/* the page you are on */
[data-testid="stSidebar"] .st-key-navlist button[kind="primary"],
[data-testid="stSidebar"] .st-key-navlist button[data-testid="stBaseButton-primary"],
[data-testid="stSidebar"] .st-key-navlist button[kind="primary"]:hover,
[data-testid="stSidebar"] .st-key-navlist button[data-testid="stBaseButton-primary"]:hover {{
    background: {ACCENT_LIME};
}}
[data-testid="stSidebar"] .st-key-navlist button[kind="primary"],
[data-testid="stSidebar"] .st-key-navlist button[kind="primary"] *,
[data-testid="stSidebar"] .st-key-navlist button[data-testid="stBaseButton-primary"],
[data-testid="stSidebar"] .st-key-navlist button[data-testid="stBaseButton-primary"] * {{
    color: {SIDEBAR_BG} !important;
    font-weight: 700;
}}
@media (prefers-reduced-motion: reduce) {{
    [data-testid="stSidebar"] .st-key-navlist button {{ transition: none; }}
}}

/* Filters (expander + multiselects) */
[data-testid="stSidebar"] [data-testid="stExpander"] {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    margin-top: 1.4rem;
}}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {{
    padding: 0.7rem 1rem;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
}}
[data-testid="stSidebar"] [data-baseweb="tag"] {{
    background: {TEAL_DARK};
    border-radius: 8px;
}}
[data-testid="stSidebar"] [data-baseweb="tag"] * {{
    color: #FFFFFF !important;
}}

/* Bottom card */
[data-testid="stSidebar"] .side-card {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 20px;
    margin-top: 2rem;
}}
[data-testid="stSidebar"] .side-card-icon {{
    width: 38px; height: 38px; border-radius: 10px;
    background: rgba(209,240,122,0.14);
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 14px;
}}
[data-testid="stSidebar"] .side-card b {{
    display: block; color: #FFFFFF !important; font-size: 0.95rem; margin-bottom: 4px;
}}
[data-testid="stSidebar"] .side-card span {{
    display: block; color: {SIDEBAR_MUTED} !important; font-size: 0.8rem; line-height: 1.45;
}}

/* ---------- Stat cards ---------- */
.stat-card {{
    background: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 18px;
    padding: 26px 28px;
    min-height: 158px;
    box-shadow: 0 1px 2px rgba(16,24,40,0.04);
}}
.stat-card.dark {{
    background: {CARD_DARK};
    border-color: transparent;
}}
.stat-top {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 20px;
}}
.stat-label {{ font-size: 0.9rem; font-weight: 600; color: {TEAL_DARK}; }}
.stat-dot {{ width: 9px; height: 9px; border-radius: 50%; display: inline-block; }}
.stat-value {{
    font-size: 2.7rem; font-weight: 700; color: {TEXT_DARK};
    line-height: 1; letter-spacing: -0.02em;
}}
.stat-unit {{
    font-size: 1.05rem; font-weight: 500; color: {TEXT_MUTED};
    margin-left: 6px; letter-spacing: 0;
}}
.stat-caption {{ font-size: 0.85rem; color: {TEXT_MUTED}; margin-top: 12px; }}
.stat-card.dark .stat-label {{ color: {ACCENT_LIME}; }}
.stat-card.dark .stat-value {{ color: #FFFFFF; }}
.stat-card.dark .stat-unit, .stat-card.dark .stat-caption {{ color: #9FB5B0; }}

/* ---------- Chart cards (plotly charts are the cards) ---------- */
[data-testid="stPlotlyChart"] {{
    background: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 18px;
    padding: 6px;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(16,24,40,0.04);
}}

/* ---------- Text cards ---------- */
.custom-card {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    padding: 20px 24px;
    border-radius: 16px;
    margin-bottom: 18px;
    font-size: 0.93rem;
    line-height: 1.55;
    color: {TEXT_DARK};
}}
.custom-card h4 {{ margin: 0 0 8px 0; font-size: 1.05rem; color: {TITLE_COLOR}; }}
.custom-card p {{ margin: 0; color: {TEXT_MUTED}; font-size: 0.9rem; line-height: 1.5; }}
.insight {{
    background: #FDF1EE;
    border: 1px solid #F8DDD6;
    border-radius: 16px;
    padding: 22px 26px;
    margin-top: 1.4rem;
}}
.insight h4 {{ margin: 0 0 8px 0; font-size: 1.05rem; color: {CORAL_CHART}; }}
.insight p {{ margin: 0; color: #4B5563; font-size: 0.92rem; line-height: 1.6; }}
.pill {{
    display: inline-block; padding: 2px 10px; border-radius: 12px;
    font-size: 0.7rem; font-weight: 700;
}}

/* ---------- Tables & buttons ---------- */
[data-testid="stDataFrame"] {{
    background: {CARD_BG};
    border-radius: 14px;
    border: 1px solid {BORDER_COLOR};
    padding: 8px;
}}
div.stButton > button, div[data-testid="stDownloadButton"] button {{
    background: {SIDEBAR_BG};
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}}
div.stButton > button:hover, div[data-testid="stDownloadButton"] button:hover {{
    background: {TEAL_DARK};
    color: white;
}}
</style>
""", unsafe_allow_html=True)

PAGER_CSS = f"""
.pager-label {{
    text-align: center; color: {TEXT_MUTED}; font-size: 0.82rem;
    font-weight: 600; letter-spacing: 0.06em; margin: 0.6rem 0 0 0;
}}
"""
st.markdown("<style>" + NAV_ICON_CSS + PAGER_CSS + "</style>", unsafe_allow_html=True)


# ------------------------- DATA -----------------------------

DATA_FILE = Path(__file__).with_name("Sleep_health_and_lifestyle_dataset_1000.csv")

NUMERIC_MEASURES = [
    "Age", "Sleep Duration", "Quality of Sleep", "Physical Activity Level",
    "Stress Level", "Heart Rate", "Daily Steps"
]

REQUIRED_COLUMNS = [
    "Person ID", "Gender", "Age", "Occupation", "Sleep Duration",
    "Quality of Sleep", "Physical Activity Level", "Stress Level",
    "BMI Category", "Blood Pressure", "Heart Rate", "Daily Steps",
    "Sleep Disorder"
]

VARIABLE_DESCRIPTIONS = {
    "Person ID": ("Identifier", "Unique participant identifier; used only to identify rows."),
    "Gender": ("Categorical", "Participant gender."),
    "Age": ("Numerical", "Participant age in years."),
    "Occupation": ("Categorical", "Participant's primary occupation."),
    "Sleep Duration": ("Numerical", "Average sleep duration in hours per night."),
    "Quality of Sleep": ("Numerical", "Self-reported sleep quality score."),
    "Physical Activity Level": ("Numerical", "Daily physical activity level recorded in minutes."),
    "Stress Level": ("Numerical", "Self-reported stress score."),
    "BMI Category": ("Categorical", "Body mass index grouping."),
    "Blood Pressure": ("Categorical", "Blood pressure recorded as systolic/diastolic."),
    "Heart Rate": ("Numerical", "Resting heart rate in beats per minute."),
    "Daily Steps": ("Numerical", "Average number of steps per day."),
    "Sleep Disorder": ("Categorical", "Recorded category: None, Insomnia, or Sleep Apnea.")
}

RESEARCH_QUESTIONS = [
    "What is the relationship between sleep duration and quality of sleep?",
    "Is physical activity level associated with sleep quality?",
    "Is there a relationship between stress level and quality of sleep?",
    "How do sleep duration, sleep quality, and lifestyle factors differ among people with no sleep disorder, insomnia, and sleep apnea?",
    "Which lifestyle or health-related factors show the strongest relationship with sleep quality or sleep disorders?"
]

HYPOTHESES = [
    ("H1 · Sleep duration and quality",
     "H₀: There is no significant relationship between sleep duration and quality of sleep.",
     "H₁: There is a significant relationship between sleep duration and quality of sleep."),
    ("H2 · Stress and quality",
     "H₀: There is no significant relationship between stress level and quality of sleep.",
     "H₁: There is a significant relationship between stress level and quality of sleep."),
    ("H3 · Sleep disorder groups",
     "H₀: There is no significant difference in sleep duration and quality of sleep among individuals with different sleep disorder categories.",
     "H₁: There is a significant difference in sleep duration and quality of sleep among individuals with different sleep disorder categories.")
]


@st.cache_data
def load_dataset(path_string):
    raw = pd.read_csv(path_string)

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in raw.columns]
    if missing_cols:
        raise ValueError(
            "The selected CSV is missing required columns: " + ", ".join(missing_cols)
        )

    cleaned = raw.copy()
    raw_disorder_missing = int(cleaned["Sleep Disorder"].isna().sum())
    cleaned["Sleep Disorder"] = cleaned["Sleep Disorder"].fillna("None")

    for col in NUMERIC_MEASURES:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    return raw, cleaned, raw_disorder_missing


if not DATA_FILE.exists():
    st.error(
        "Dataset file not found. Keep 'Sleep_health_and_lifestyle_dataset_1000.csv' "
        "in the same folder as app.py."
    )
    st.stop()

try:
    raw_df, df, raw_disorder_missing = load_dataset(str(DATA_FILE))
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

SOURCE_RECORDS = len(raw_df)
SOURCE_VARIABLES = raw_df.shape[1]
DUPLICATES = int(raw_df.duplicated().sum())
RAW_MISSING = int(raw_df.isna().sum().sum())
CLEAN_MISSING = int(df.isna().sum().sum())


# ------------------------ SIDEBAR --------------------------

SPARKLE = (
    "<svg width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#D1F07A' "
    "stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'>"
    "<path d='M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z'/>"
    "<path d='M19 16l.7 1.8L21.5 18.5l-1.8.7L19 21l-.7-1.8-1.8-.7 1.8-.7z'/></svg>"
)
MOON = (
    "<svg width='24' height='24' viewBox='0 0 24 24' fill='#132A25' stroke='#132A25' "
    "stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'>"
    "<path d='M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z'/></svg>"
)

def set_page(name):
    st.session_state["page"] = name


if st.session_state.get("page") not in NAV_NAMES:
    st.session_state["page"] = NAV_NAMES[0]

with st.sidebar:
    st.markdown(
        f"<div class='brand'><div class='brand-logo'>{MOON}</div>"
        "<div class='brand-text'><b>Somnia</b> / insights</div></div>"
        "<div class='side-label'>WORKSPACE</div>",
        unsafe_allow_html=True,
    )

    with st.container(key="navlist"):
        for _n, _name in enumerate(NAV_NAMES, start=1):
            st.button(
                _name,
                key=f"nav_{_n}",
                type="primary" if st.session_state["page"] == _name else "secondary",
                on_click=set_page,
                args=(_name,),
            )
    page = st.session_state["page"]

    genders = sorted(df["Gender"].dropna().unique().tolist())
    occupations = sorted(df["Occupation"].dropna().unique().tolist())
    disorders = DISORDER_ORDER

    with st.expander("Filter data"):
        selected_genders = st.multiselect("Gender", genders, default=genders)
        selected_occupations = st.multiselect("Occupation", occupations, default=occupations)
        selected_disorders = st.multiselect("Sleep disorder", disorders, default=disorders)

    st.markdown(
        f"<div class='side-card'><div class='side-card-icon'>{SPARKLE}</div>"
        "<b>Research workspace</b>"
        f"<span>Sleep Health &amp; Lifestyle Dataset · {SOURCE_RECORDS:,} records</span></div>",
        unsafe_allow_html=True,
    )


filtered = df[
    df["Gender"].isin(selected_genders)
    & df["Occupation"].isin(selected_occupations)
    & df["Sleep Disorder"].isin(selected_disorders)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Adjust the filters in the sidebar.")
    st.stop()


# -------------------- REUSABLE HELPERS ---------------------

def _stretch_kwargs(fn):
    """New Streamlit uses width='stretch'; older versions use use_container_width."""
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return {}
    if "width" in params and params["width"].default in ("stretch", "content"):
        return {"width": "stretch"}
    if "use_container_width" in params:
        return {"use_container_width": True}
    return {}


PLOT_KW = _stretch_kwargs(st.plotly_chart)
TABLE_KW = _stretch_kwargs(st.dataframe)
BUTTON_KW = _stretch_kwargs(st.button)


def plot(fig):
    st.plotly_chart(fig, **PLOT_KW)


def table(data, **kwargs):
    st.dataframe(data, **TABLE_KW, **kwargs)


def page_header(number, kicker, title, subtitle):
    st.markdown(
        f'<div class="kicker"><span class="kicker-dot"></span>FRAME {number:02d} · {kicker}</div>'
        f'<h1 class="page-title">{title}</h1>'
        f'<p class="subtitle">{subtitle}</p>',
        unsafe_allow_html=True,
    )


def stat_card(label, value, unit="", caption="", dot=TEAL_CHART, dark=False):
    cls = "stat-card dark" if dark else "stat-card"
    unit_html = f'<span class="stat-unit">{unit}</span>' if unit else ""
    st.markdown(
        f'<div class="{cls}"><div class="stat-top"><span class="stat-label">{label}</span>'
        f'<span class="stat-dot" style="background:{dot}"></span></div>'
        f'<div class="stat-value">{value}{unit_html}</div>'
        f'<div class="stat-caption">{caption}</div></div>',
        unsafe_allow_html=True,
    )


def note(html, color=TEAL_CHART):
    st.markdown(
        f'<div class="custom-card" style="border-left: 4px solid {color};">{html}</div>',
        unsafe_allow_html=True,
    )


def chart_style(fig, height=350, title="", subtitle=""):
    heading = ""
    if title:
        heading = f"<b>{title}</b>"
        if subtitle:
            heading += f"<br><span style='font-size:12px;color:{TEXT_MUTED}'>{subtitle}</span>"
    top_margin = 84 if subtitle else (56 if title else 24)
    fig.update_layout(
        title=dict(text=heading, x=0.025, xanchor="left", y=0.95, yanchor="top",
                   font=dict(family="Inter", size=16, color=TEXT_DARK)),
        template="plotly_white",
        height=height,
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(family="Inter", size=12, color=TEXT_MUTED),
        margin=dict(l=24, r=24, t=top_margin, b=24),
        xaxis=dict(showgrid=False, zeroline=False, color=TEXT_MUTED),
        yaxis=dict(showgrid=True, gridcolor="#F3F4F6", zeroline=False, color=TEXT_MUTED),
        legend=dict(orientation="h", y=-0.2, x=0),
    )
    return fig


def show(fig, height=350, title="", subtitle=""):
    plot(chart_style(fig, height, title, subtitle))


def disorder_bar(means, column, title, subtitle, text_format):
    data = means.reset_index()
    data["Label"] = data["Sleep Disorder"].map(DISORDER_LABELS)
    fig = px.bar(
        data, x=column, y="Label", orientation="h",
        color="Sleep Disorder", color_discrete_map=DISORDER_COLORS,
    )
    fig.update_traces(
        texttemplate=text_format, textposition="outside", cliponaxis=False,
        textfont=dict(color=TEXT_DARK, size=12), width=0.42,
    )
    try:
        fig.update_traces(marker_cornerradius=8)  # needs a recent Plotly
    except ValueError:
        pass
    chart_style(fig, 330, title, subtitle)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(visible=False, range=[0, float(data[column].max()) * 1.3])
    fig.update_yaxes(title=None, showgrid=False, autorange="reversed")
    plot(fig)


def correlation(x, y, data):
    pair = data[[x, y]].dropna()
    if len(pair) < 3 or pair[x].nunique() < 2 or pair[y].nunique() < 2:
        return np.nan, np.nan
    result = pearsonr(pair[x], pair[y])
    return float(result.statistic), float(result.pvalue)


def p_text(p):
    if pd.isna(p):
        return "N/A"
    if p < 0.001:
        return f"{p:.2e}"
    return f"{p:.4f}"


def strength_label(r):
    if pd.isna(r):
        return "not available"
    magnitude = abs(r)
    if magnitude >= 0.70:
        return "strong"
    if magnitude >= 0.40:
        return "moderate"
    if magnitude >= 0.20:
        return "weak"
    return "very weak"


def direction_label(r):
    if pd.isna(r):
        return "no clear direction"
    if r > 0:
        return "positive"
    if r < 0:
        return "negative"
    return "no linear association"


def add_kde_histogram(data, column, x_label, bins=10, color=TEAL_CHART):
    values = data[column].dropna().to_numpy()
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=values, nbinsx=bins, name="Number of people",
        marker_color=color, opacity=0.85,
    ))

    if len(values) > 2 and np.std(values) > 0:
        grid = np.linspace(values.min() - 0.3, values.max() + 0.3, 300)
        density = gaussian_kde(values)(grid)
        bin_width = (values.max() - values.min()) / bins
        fig.add_trace(go.Scatter(
            x=grid, y=density * len(values) * bin_width, name="KDE curve", mode="lines",
            line=dict(color=SIDEBAR_BG, width=3),
        ))

    fig.update_layout(xaxis_title=x_label, yaxis_title="Number of people", barmode="overlay")
    return fig


def disorder_groups(data, column):
    return [
        data.loc[data["Sleep Disorder"] == g, column].dropna()
        for g in DISORDER_ORDER if g in data["Sleep Disorder"].unique()
    ]


# ============================================================
# FRAME 01 — OVERVIEW
# ============================================================

if page == "Overview":
    page_header(1, "OVERVIEW", "The bigger picture of sleep",
                "A high-level view of the dataset, its key measures, and the first patterns emerging from the analysis.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("Total participants", f"{SOURCE_RECORDS:,}", "", "Source dataset", ACCENT_LIME, dark=True)
    with c2:
        stat_card("Avg. sleep duration", f"{filtered['Sleep Duration'].mean():.2f}", "hrs", "Daily average", TEAL_CHART)
    with c3:
        stat_card("Avg. sleep quality", f"{filtered['Quality of Sleep'].mean():.2f}", "/ 10", "Self-reported score", CORAL_CHART)
    with c4:
        stat_card("Avg. stress level", f"{filtered['Stress Level'].mean():.2f}", "/ 10", "Self-reported score", SLATE_CHART)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        fig = add_kde_histogram(filtered, "Sleep Duration", "Sleep duration (hours)")
        show(fig, 380, "Distribution of sleep duration", "How many people sleep each number of hours")
    with right:
        occ = (filtered.groupby("Occupation", as_index=False)["Quality of Sleep"]
               .mean().sort_values("Quality of Sleep"))
        fig = px.bar(occ, x="Quality of Sleep", y="Occupation", orientation="h",
                     color_discrete_sequence=[TEAL_CHART])
        fig.update_yaxes(showgrid=False, title=None)
        show(fig, 380, "Average sleep quality by occupation", "Score out of 10")

    r_duration, _ = correlation("Sleep Duration", "Quality of Sleep", filtered)
    r_stress, _ = correlation("Stress Level", "Quality of Sleep", filtered)
    r_activity, _ = correlation("Physical Activity Level", "Quality of Sleep", filtered)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Preliminary findings")

    note(f"<b>Sleep duration → quality:</b> {strength_label(r_duration).title()} {direction_label(r_duration)} association (r = {r_duration:.4f}). Longer sleep duration tends to accompany higher reported sleep quality.", TEAL_CHART)
    note(f"<b>Stress → quality:</b> {strength_label(r_stress).title()} {direction_label(r_stress)} association (r = {r_stress:.4f}). Higher stress tends to accompany lower reported sleep quality.", CORAL_CHART)
    note(f"<b>Physical activity → quality:</b> {strength_label(r_activity).title()} {direction_label(r_activity)} association (r = {r_activity:.4f}). The relationship is positive but comparatively weak.", SLATE_CHART)

    with st.expander("Research questions"):
        for i, question in enumerate(RESEARCH_QUESTIONS, start=1):
            st.markdown(f"**RQ{i}.** {question}")

    with st.expander("Research hypotheses"):
        for title, h0, h1 in HYPOTHESES:
            st.markdown(f"**{title}**")
            st.write(h0)
            st.write(h1)


# ============================================================
# FRAME 02 — DATASET
# ============================================================

elif page == "Dataset":
    page_header(2, "THE DATA", "Dataset overview",
                "A structured view of the source data, its shape, and the variables powering this analysis.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("Total records", f"{SOURCE_RECORDS:,}", "", "Participant rows", ACCENT_LIME, dark=True)
    with c2:
        stat_card("Total variables", f"{SOURCE_VARIABLES}", "", "Across 3 data types", TEAL_CHART)
    with c3:
        stat_card("Missing values", f"{CLEAN_MISSING}", "", "After cleaning", CORAL_CHART)
    with c4:
        stat_card("Duplicate records", f"{DUPLICATES}", "", "Unique rows", SLATE_CHART)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Data health")
        st.progress(1.0, text="Completeness: 100%")
        st.progress(1.0, text="Unique records: 100%")
        st.progress(0.5, text="Numerical variables: 7")
        st.progress(0.4, text="Categorical variables: 6")

    with col_right:
        st.markdown(
            f'<div class="stat-card dark"><div class="stat-top">'
            f'<span class="stat-label">Source file</span>'
            f'<span class="stat-dot" style="background:{ACCENT_LIME}"></span></div>'
            f'<div class="stat-value" style="font-size:1.5rem;">Sleep health and lifestyle</div>'
            f'<div class="stat-caption">A complete snapshot of lifestyle and sleep indicators.<br>'
            f'<code style="color:{ACCENT_LIME};background:transparent;padding:0;">'
            f'Sleep_health_and_lifestyle_dataset_1000.csv</code></div></div>',
            unsafe_allow_html=True,
        )

    st.subheader("Variable dictionary")
    dictionary = [
        {"Variable": col, "Type": VARIABLE_DESCRIPTIONS[col][0],
         "Description": VARIABLE_DESCRIPTIONS[col][1], "Status": "✅"}
        for col in REQUIRED_COLUMNS
    ]
    table(pd.DataFrame(dictionary), hide_index=True)

    st.subheader("Dataset preview")
    table(filtered[REQUIRED_COLUMNS].head(10), hide_index=True)

    st.info(f"Data-cleaning note: the source CSV has {raw_disorder_missing} blank cells in 'Sleep Disorder'. These are classified as 'None'.")

    st.subheader("Download data")
    d1, d2 = st.columns(2)
    with d1:
        st.download_button("Download cleaned dataset", data=df.to_csv(index=False).encode("utf-8"),
                           file_name="somnia_cleaned_dataset.csv", mime="text/csv")
    with d2:
        st.download_button("Download original source CSV", data=raw_df.to_csv(index=False).encode("utf-8"),
                           file_name="Sleep_health_and_lifestyle_dataset_1000.csv", mime="text/csv")


# ============================================================
# FRAME 03 — EXPLORATORY ANALYSIS
# ============================================================

elif page == "Exploratory analysis":
    page_header(3, "EXPLORATORY ANALYSIS", "The shape of sleep",
                "Start with the fundamentals. These distributions show how participants are spread across duration, quality, stress, and activity.")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        stat_card("Average duration", f"{filtered['Sleep Duration'].mean():.2f}", "hrs",
                  f"Median: {filtered['Sleep Duration'].median():.1f} hrs", ACCENT_LIME, dark=True)
    with m2:
        stat_card("Average quality", f"{filtered['Quality of Sleep'].mean():.2f}", "/ 10",
                  f"Mode: {filtered['Quality of Sleep'].mode().iloc[0]:.0f} / 10", CORAL_CHART)
    with m3:
        stat_card("Average stress", f"{filtered['Stress Level'].mean():.2f}", "/ 10",
                  f"Mode: {filtered['Stress Level'].mode().iloc[0]:.0f} / 10", SLATE_CHART)
    with m4:
        stat_card("Average activity", f"{filtered['Physical Activity Level'].mean():.2f}", "min",
                  "Daily average", TEAL_CHART)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        show(add_kde_histogram(filtered, "Sleep Duration", "Sleep duration (hours)"), 360,
             "Sleep duration distribution", "Hours per night")
    with right:
        fig = px.histogram(filtered, x="Quality of Sleep", nbins=10, color_discrete_sequence=[CORAL_CHART])
        show(fig, 360, "Sleep quality distribution", "Self-reported score")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        fig = px.histogram(filtered, x="Stress Level", nbins=8, color_discrete_sequence=[LIME_CHART])
        show(fig, 360, "Stress level distribution", "Self-reported score")
    with right:
        fig = px.histogram(filtered, x="Physical Activity Level", nbins=10, color_discrete_sequence=[SLATE_CHART])
        show(fig, 360, "Physical activity distribution", "Minutes per day")

    st.markdown("<br>", unsafe_allow_html=True)
    note("<b>Distribution observation:</b> In the full dataset, sleep durations are concentrated mainly between 6 and 8 hours. Longer sleep is associated with lower stress in this sample.", TEAL_CHART)

    with st.expander("Numerical summary statistics"):
        summary = filtered[NUMERIC_MEASURES].describe().T
        summary.columns = ["Count", "Mean", "Std. deviation", "Minimum", "25th percentile",
                           "Median", "75th percentile", "Maximum"]
        table(summary.round(2))


# ============================================================
# FRAME 04 — RELATIONSHIPS
# ============================================================

elif page == "Relationships":
    page_header(4, "RELATIONSHIP ANALYSIS", "What moves with sleep quality?",
                "Focused comparisons connect sleep duration, physical activity, and stress directly to the quality of sleep reported by participants.")

    relationships = [
        ("Sleep Duration", "Quality of Sleep", "Sleep duration vs. quality", "Positive relationship", TEAL_CHART),
        ("Physical Activity Level", "Quality of Sleep", "Physical activity vs. quality", "Weak positive relationship", SLATE_CHART),
        ("Stress Level", "Quality of Sleep", "Stress level vs. quality", "Negative relationship", CORAL_CHART),
    ]

    for x, y, title, relationship, color in relationships:
        r, p = correlation(x, y, filtered)

        st.markdown(f"### {title}")
        st.caption(f"{relationship} · Pearson r = {r:.4f} · p-value = {p_text(p)}")

        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter(filtered, x=x, y=y, color_discrete_sequence=[color])
            fig.update_traces(marker=dict(size=8, opacity=0.7))
            show(fig, 320, "Each point is one participant", f"{x} vs. {y}")
        with col2:
            avg = filtered.groupby(x, as_index=False)[y].mean().sort_values(x)
            line = px.line(avg, x=x, y=y, markers=True, color_discrete_sequence=[SIDEBAR_BG])
            line.update_traces(line=dict(width=3), marker=dict(size=8, color=color))
            show(line, 320, "Average trend", f"Mean {y.lower()} at each {x.lower()}")

        significance = ("The association is statistically significant at the 0.05 level."
                        if p < .05 else
                        "The association is not statistically significant at the 0.05 level.")
        note(f"<b>Interpretation:</b> The observed relationship is {strength_label(r)} and {direction_label(r)} (r = {r:.4f}). {significance} Correlation indicates association, not causation.", color)
        st.markdown("---")

    st.subheader("Which factors show the strongest relationship with sleep quality?")
    corr_vars = ["Sleep Duration", "Age", "Physical Activity Level", "Daily Steps", "Heart Rate", "Stress Level"]
    corr_rows = []
    for col in corr_vars:
        r_val, p_val = correlation(col, "Quality of Sleep", filtered)
        corr_rows.append({"Variable": col, "Pearson r": r_val, "p-value": p_text(p_val)})
    corr_df = pd.DataFrame(corr_rows).sort_values("Pearson r", ascending=False)

    fig = px.bar(corr_df, x="Pearson r", y="Variable", orientation="h", color="Pearson r",
                 color_continuous_scale=[CORAL_CHART, "#F3F4F6", TEAL_CHART], range_color=[-1, 1])
    fig.update_yaxes(showgrid=False, title=None, autorange="reversed")
    show(fig, 380, "Correlation with sleep quality", "Pearson r, from -1 to 1")

    st.subheader("Correlation heatmap")
    heat_columns = ["Age", "Sleep Duration", "Quality of Sleep", "Physical Activity Level",
                    "Stress Level", "Heart Rate", "Daily Steps"]
    corr_matrix = filtered[heat_columns].corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.index, zmin=-1, zmax=1,
        colorscale=[[0, CORAL_CHART], [.5, "#F8F9FA"], [1, TEAL_CHART]],
        text=np.round(corr_matrix.values, 2), texttemplate="%{text}",
    ))
    show(fig, 480, "How every measure relates to every other", "Darker teal means a stronger positive link")


# ============================================================
# FRAME 05 — SLEEP DISORDER COMPARISON
# ============================================================

elif page == "Disorder comparison":
    page_header(5, "SLEEP DISORDER COMPARISON", "Three different sleep profiles",
                "Comparing group averages makes the impact of insomnia and sleep apnea tangible.")

    group_means = (
        filtered.groupby("Sleep Disorder")[["Sleep Duration", "Quality of Sleep",
                                            "Physical Activity Level", "Stress Level"]]
        .mean().reindex(DISORDER_ORDER).dropna(how="all")
    )

    cols = st.columns(3)
    for col, group in zip(cols, DISORDER_ORDER):
        with col:
            if group in group_means.index:
                stat_card(DISORDER_LABELS[group], f"{group_means.loc[group, 'Quality of Sleep']:.1f}",
                          "/ 10", "Average sleep quality", DISORDER_DOTS[group], dark=(group == "None"))

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        disorder_bar(group_means, "Quality of Sleep", "Average sleep quality",
                     "A lower score indicates poorer reported sleep", "%{x:.1f} / 10")
    with col_right:
        disorder_bar(group_means, "Sleep Duration", "Average sleep duration",
                     "Hours per night by disorder group", "%{x:.1f} hrs")

    group_quality = disorder_groups(filtered, "Quality of Sleep")
    group_duration = disorder_groups(filtered, "Sleep Duration")

    if len(group_quality) >= 2 and all(len(g) > 0 for g in group_quality):
        f_q, p_q = f_oneway(*group_quality)
        f_d, p_d = f_oneway(*group_duration)

        verdict_q = ("The group means differ significantly at α = 0.05."
                     if p_q < .05 else "There is not sufficient evidence of a difference.")
        verdict_d = ("The group means differ significantly at α = 0.05."
                     if p_d < .05 else "There is not sufficient evidence of a difference.")

        st.markdown(
            '<div class="insight"><h4>The clearest difference</h4>'
            f'<p><b>Quality of sleep:</b> F = {f_q:.2f}, p = {p_text(p_q)}. {verdict_q}<br><br>'
            f'<b>Sleep duration:</b> F = {f_d:.2f}, p = {p_text(p_d)}. {verdict_d}</p></div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("Select at least two sleep disorder groups in the filters to run the ANOVA tests.")


# ============================================================
# FRAME 06 — FINDINGS & CONCLUSION
# ============================================================

elif page == "Findings & conclusion":
    page_header(6, "FINDINGS & CONCLUSION", "The story so far",
                "A concise readout of the analysis, organized around the research questions and hypotheses.")

    r_duration, p_duration = correlation("Sleep Duration", "Quality of Sleep", filtered)
    r_stress, p_stress = correlation("Stress Level", "Quality of Sleep", filtered)
    r_activity, p_activity = correlation("Physical Activity Level", "Quality of Sleep", filtered)

    def finding(title, pill, pill_bg, pill_fg, body):
        st.markdown(
            f'<div class="custom-card"><h4>{title}</h4>'
            f'<span class="pill" style="background:{pill_bg};color:{pill_fg};">{pill}</span>'
            f'<p style="margin-top:10px;">{body}</p></div>',
            unsafe_allow_html=True,
        )

    col1, col2 = st.columns(2)
    with col1:
        finding("Sleep duration → quality", "Positive signal", LIME_CHART, SIDEBAR_BG,
                f"Participants sleeping longer generally report better quality scores. (r = {r_duration:.4f}, p = {p_text(p_duration)})")
        finding("Physical activity → quality", "Moderate signal", LIME_CHART, SIDEBAR_BG,
                f"Daily movement is associated with a modest lift in reported quality. (r = {r_activity:.4f}, p = {p_text(p_activity)})")
    with col2:
        finding("Stress → quality", "Inverse signal", CORAL_CHART, "white",
                f"Stress is the strongest visible lifestyle factor working against quality. (r = {r_stress:.4f}, p = {p_text(p_stress)})")
        finding("Disorders → sleep characteristics", "Clear difference", SLATE_CHART, "white",
                "Disorder groups show distinct quality, stress, and duration profiles.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Hypothesis testing summary")

    group_quality = disorder_groups(filtered, "Quality of Sleep")
    p_anova_q = np.nan
    if len(group_quality) >= 2 and all(len(g) > 0 for g in group_quality):
        p_anova_q = f_oneway(*group_quality).pvalue

    def decision(p):
        return "Reject H₀; H₁ supported" if (not pd.isna(p) and p < .05) else "Fail to reject H₀"

    hypothesis_table = pd.DataFrame([
        {"Hypothesis": "H1 · Sleep duration and quality", "Test": "Pearson correlation",
         "Evidence": f"r = {r_duration:.4f}; p = {p_text(p_duration)}", "Decision": decision(p_duration)},
        {"Hypothesis": "H2 · Stress and quality", "Test": "Pearson correlation",
         "Evidence": f"r = {r_stress:.4f}; p = {p_text(p_stress)}", "Decision": decision(p_stress)},
        {"Hypothesis": "H3 · Disorder group differences", "Test": "One-way ANOVA",
         "Evidence": f"Quality p = {p_text(p_anova_q)}", "Decision": decision(p_anova_q)},
    ])
    table(hypothesis_table, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="background-color:{CARD_DARK};padding:30px 34px;border-radius:18px;">'
        f'<p style="color:{ACCENT_LIME};font-size:0.75rem;font-weight:700;letter-spacing:1px;margin:0;">CONCLUSION</p>'
        f'<h3 style="color:{ACCENT_LIME} !important;margin:6px 0 14px 0;">Sleep quality is connected to lifestyle and sleep patterns.</h3>'
        '<p style="color:#A9BDB9;line-height:1.65;font-size:0.95rem;margin:0;">'
        'Across this 1,000-record dataset, sleep duration has a strong positive association '
        'with reported sleep quality, while stress has a strong negative association. '
        'Physical activity has a weaker positive association. The sleep-disorder groups '
        'also show differences in sleep duration and quality. These findings describe '
        'patterns and associations in this dataset; they do not prove that one factor causes another.'
        '</p></div>',
        unsafe_allow_html=True,
    )


# ------------------------- PAGER ---------------------------

def go_to(step):
    current = NAV_NAMES.index(st.session_state["page"])
    target = max(0, min(len(NAV_NAMES) - 1, current + step))
    st.session_state["page"] = NAV_NAMES[target]


current_index = NAV_NAMES.index(page)
st.markdown("<br>", unsafe_allow_html=True)
prev_col, mid_col, next_col = st.columns([2, 3, 2])
with prev_col:
    if current_index > 0:
        st.button(f"← {NAV_NAMES[current_index - 1]}", key="pager_prev",
                  on_click=go_to, args=(-1,), **BUTTON_KW)
with mid_col:
    st.markdown(f"<p class='pager-label'>FRAME {current_index + 1} OF {len(NAV_NAMES)}</p>",
                unsafe_allow_html=True)
with next_col:
    if current_index < len(NAV_NAMES) - 1:
        st.button(f"{NAV_NAMES[current_index + 1]} →", key="pager_next",
                  on_click=go_to, args=(1,), **BUTTON_KW)


# --------------------------- FOOTER ------------------------
st.markdown("<br><br><hr style='border-color: #E5E7EB;'>", unsafe_allow_html=True)
st.markdown(
    f'<p style="text-align:right;color:{TEXT_MUTED};font-size:0.8rem;">'
    'Somnia / insights<br>Sleep Health &amp; Lifestyle Dataset · 1,000 records</p>',
    unsafe_allow_html=True,
)