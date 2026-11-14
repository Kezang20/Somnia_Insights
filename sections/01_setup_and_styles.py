import streamlit as st

# 1. APP CONFIGURATION AND THEME
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


# 2. CUSTOM STYLES
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

# 2.1 FILTER PANEL STYLES

FILTER_CSS = """

/* ============================================================
   FILTER PANEL - SOMNIA GREEN THEME
   ============================================================ */

[data-testid="stSidebar"] .st-key-filterbox {
    background: #1B2F26 !important;
    border: 1px solid #3C5A4B !important;
    border-radius: 12px;
    padding: 16px;
    margin-top: 1.4rem;
}

[data-testid="stSidebar"] .filter-title {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-weight: 700;
    font-size: .95rem;
    letter-spacing: .04em;
    color: #E4EFE9 !important;
    padding-bottom: 10px;
    margin: 0 0 6px;
    border-bottom: 1px solid #3C5A4B;
}

[data-testid="stSidebar"] .filter-title span {
    font-size: .75rem;
    font-weight: 500;
    color: #9FBCAE !important;
}

[data-testid="stSidebar"] .filter-label {
    display: flex;
    justify-content: space-between;
    font-size: .74rem;
    font-weight: 600;
    letter-spacing: .06em;
    color: #9FBCAE !important;
    margin: 14px 0 6px;
}

[data-testid="stSidebar"] .filter-label span {
    font-weight: 500;
    letter-spacing: 0;
    color: #7FD1A8 !important;
}


/* ---------- GENDER FILTER ---------- */

[data-testid="stSidebar"] .st-key-f_gender {
    width: 100% !important;
}

[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] {
    width: 100% !important;
    max-width: 100% !important;
    background: #101B15 !important;
    border: 1px solid #3C5A4B !important;
    border-radius: 9px !important;
    padding: 5px !important;
    box-sizing: border-box !important;
}

/* Make the inner control use the full available width */
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] > div,
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] [role="radiogroup"] {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    width: 100% !important;
    max-width: 100% !important;
    gap: 6px !important;
}

/* Give each gender option its own space */
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] button,
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] [role="radio"] {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    flex: none !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 8px 4px !important;
    background: #243D32 !important;
    color: #C9D8D4 !important;
    border: 1px solid #3C5A4B !important;
    border-radius: 7px !important;
    box-shadow: none !important;
    font-size: .78rem !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
}

/* Override Streamlit's default selected red/pink styling */
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] button[aria-pressed="true"],
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] button[aria-selected="true"],
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"] {
    background: #3F9B74 !important;
    color: #FFFFFF !important;
    border: 1px solid #70C49A !important;
}

/* Keep selected text white */
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] button[aria-pressed="true"] *,
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] button[aria-selected="true"] *,
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] [aria-checked="true"] * {
    color: #FFFFFF !important;
}

/* Hover */
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] button:hover,
[data-testid="stSidebar"] .st-key-f_gender [data-testid="stSegmentedControl"] [role="radio"]:hover {
    background: #315B46 !important;
    color: #FFFFFF !important;
    border-color: #70C49A !important;
}


/* ---------- OCCUPATION FILTER ---------- */

[data-testid="stSidebar"] .st-key-filterbox [data-testid="stExpander"] {
    background: #101B15 !important;
    border: 1px solid #3C5A4B !important;
    border-radius: 9px;
}

[data-testid="stSidebar"] .st-key-filterbox [data-testid="stExpander"] details {
    border: none !important;
}

[data-testid="stSidebar"] .st-key-filterbox [data-testid="stExpander"] summary {
    background: #243D32 !important;
    border-radius: 8px !important;
    color: #E4EFE9 !important;
}

[data-testid="stSidebar"] .st-key-filterbox [data-testid="stExpander"] summary * {
    color: #E4EFE9 !important;
}

[data-testid="stSidebar"] .st-key-filterbox [data-testid="stExpander"] summary:hover {
    background: #315B46 !important;
}

/* Multiselect input */
[data-testid="stSidebar"] .st-key-filterbox [data-baseweb="select"] > div {
    background: #1B2F26 !important;
    border: 1px solid #3C5A4B !important;
    border-radius: 8px !important;
}

/* Selected occupation tags - GREEN, NOT RED */
[data-testid="stSidebar"] .st-key-filterbox [data-baseweb="tag"],
[data-testid="stSidebar"] .st-key-filterbox span[data-baseweb="tag"] {
    background: #2A5B45 !important;
    border: 1px solid #4B8C68 !important;
    border-radius: 999px !important;
    color: #E4EFE9 !important;
}

/* Tag text and remove icon */
[data-testid="stSidebar"] .st-key-filterbox [data-baseweb="tag"] *,
[data-testid="stSidebar"] .st-key-filterbox span[data-baseweb="tag"] * {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}


/* ---------- SLEEP DISORDER CHECKBOXES ---------- */

/* Checked checkbox background */
[data-testid="stSidebar"] .st-key-filterbox [data-testid="stCheckbox"] [role="checkbox"][aria-checked="true"],
[data-testid="stSidebar"] .st-key-filterbox [data-baseweb="checkbox"] [role="checkbox"][aria-checked="true"] {
    background-color: #3F9B74 !important;
    border-color: #70C49A !important;
}

/* Checked checkbox icon */
[data-testid="stSidebar"] .st-key-filterbox [role="checkbox"][aria-checked="true"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

/* Checkbox hover */
[data-testid="stSidebar"] .st-key-filterbox [role="checkbox"]:hover {
    border-color: #7FD1A8 !important;
}

/* Checkbox focus */
[data-testid="stSidebar"] .st-key-filterbox [role="checkbox"]:focus,
[data-testid="stSidebar"] .st-key-filterbox [role="checkbox"]:focus-visible {
    outline: 2px solid #7FD1A8 !important;
    outline-offset: 2px !important;
}


/* ---------- FILTER FOOTER ---------- */

[data-testid="stSidebar"] .st-key-f_foot {
    border-top: 1px solid #3C5A4B;
    margin-top: 14px;
    padding-top: 12px;
}

[data-testid="stSidebar"] .filter-count {
    font-size: .75rem;
    color: #9FBCAE !important;
    padding-top: 8px;
}

/* Reset button */
[data-testid="stSidebar"] .st-key-f_foot div.stButton > button {
    background: #243D32 !important;
    border: 1px solid #5D8672 !important;
    border-radius: 9px !important;
    color: #E4EFE9 !important;
    font-weight: 500;
    padding: 5px 12px;
    min-height: 0;
    float: right;
    box-shadow: none !important;
}

[data-testid="stSidebar"] .st-key-f_foot div.stButton > button *,
[data-testid="stSidebar"] .st-key-f_foot div.stButton > button p {
    color: #E4EFE9 !important;
}

[data-testid="stSidebar"] .st-key-f_foot div.stButton > button:hover {
    background: #315B46 !important;
    border-color: #7FD1A8 !important;
    color: #FFFFFF !important;
}
"""

st.markdown("<style>" + NAV_ICON_CSS + PAGER_CSS + FILTER_CSS + "</style>", unsafe_allow_html=True)


