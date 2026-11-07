from pathlib import Path
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
    initial_sidebar_state="collapsed",
)

# ------------------------- THEME ----------------------------
BURGUNDY = "#641C32"
BURGUNDY_DARK = "#421323"
SAFFRON = "#C58B32"
SAFFRON_LIGHT = "#E8C98E"
CREAM = "#FAF6EF"
WHITE = "#FFFFFF"
INK = "#302B2A"
MUTED = "#625A55"
BORDER = "#E8DED1"
PALETTE = ["#641C32", "#C58B32", "#A66A78", "#8C806B", "#D8B978"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #FAF6EF;
    color: #302B2A;
}

h1, h2, h3 {
    color: #641C32 !important;
}

h1 {
    font-family: 'Playfair Display', serif !important;
}

p, li, label {
    color: #302B2A;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #641C32;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #F2DDBB !important;
}

/* METRICS */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E8DED1;
    padding: 16px 18px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(66,19,35,.05);
}

[data-testid="stMetricLabel"] {
    color: #641C32 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #9A6726 !important;
    font-weight: 700;
}

[data-testid="stMetricDelta"] {
    color: #625A55 !important;
}

[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border-radius: 10px;
}

/* BUTTONS */

div.stButton > button,
div[data-testid="stDownloadButton"] button {
    background: #641C32;
    color: #FFFFFF;
    border: 1px solid #641C32;
    border-radius: 9px;
    font-weight: 600;
}

div.stButton > button:hover,
div[data-testid="stDownloadButton"] button:hover {
    background: #421323;
    color: #FFFFFF;
    border-color: #421323;
}

/* GENERAL LAYOUT */

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

.kicker {
    color: #9A6726;
    font-size: .76rem;
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-bottom: .3rem;
}

.subtle {
    color: #625A55;
    font-size: .94rem;
}

.insight {
    background: #FFFFFF;
    border: 1px solid #E8DED1;
    border-left: 5px solid #C58B32;
    padding: 14px 17px;
    border-radius: 10px;
    margin: 8px 0 12px 0;
    color: #302B2A;
}

.research-card {
    background: #FFFFFF;
    border: 1px solid #E8DED1;
    border-radius: 12px;
    padding: 15px 17px;
    margin: 8px 0;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #E8DED1;
    border-radius: 14px;
}

hr {
    border-color: #E8DED1;
}

/* ============================================================
   HAMBURGER NAVIGATION
   ============================================================ */

[data-testid="stSidebar"] [data-testid="stRadio"] {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.16);
    border-radius: 13px;
    padding: 8px;
    margin: 8px 0 20px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    color: #F2DDBB !important;
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin: 0 4px 8px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
    gap: 4px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
    border-radius: 9px;
    padding: 9px 10px;
    margin: 0;
    transition: background .2s ease, transform .2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
    background: rgba(255,255,255,.12);
    transform: translateX(2px);
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    background: #FFFFFF;
    box-shadow: 0 3px 8px rgba(0,0,0,.14);
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #641C32 !important;
    font-weight: 700;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label p {
    color: #FFFFFF !important;
    font-size: .84rem;
    font-weight: 600;
    margin: 0;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
    display: none;
}

</style>
""", unsafe_allow_html=True)


DATA_FILE = Path(__file__).with_name(
    "Sleep_health_and_lifestyle_dataset_1000.csv"
)

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


# ---------------------- DATA LOADING -----------------------

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

    # Blank Sleep Disorder entries are classified as "None".
    cleaned["Sleep Disorder"] = cleaned["Sleep Disorder"].fillna("None")

    for col in NUMERIC_MEASURES:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    # Keep every participant row.
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
NUMERICAL_COUNT = len(NUMERIC_MEASURES)


# ------------------------ SIDEBAR --------------------------

with st.sidebar:
    st.markdown("# 🌙 Somnia")
    st.markdown("### INSIGHTS")
    st.caption("Sleep health & lifestyle analytics")
    st.markdown("---")

    page = st.radio(
        "Main Navigation",
        [
            "01 · Overview",
            "02 · Dataset",
            "03 · Exploratory Analysis",
            "04 · Relationships",
            "05 · Disorder Comparison",
            "06 · Findings & Conclusion"
        ],
        label_visibility="visible",
        key="main_navigation"
    )

    st.markdown("### FILTER DATA")

    genders = sorted(df["Gender"].dropna().unique().tolist())
    occupations = sorted(df["Occupation"].dropna().unique().tolist())
    disorders = ["None", "Insomnia", "Sleep Apnea"]

    selected_genders = st.multiselect("Gender", genders, default=genders)

    selected_occupations = st.multiselect(
        "Occupation", occupations, default=occupations
    )

    selected_disorders = st.multiselect(
        "Sleep disorder", disorders, default=disorders
    )

    st.markdown("---")
    st.caption(f"Source records: {SOURCE_RECORDS:,}")
    st.caption("PRG405 · Introduction to Data Science")


filtered = df[
    df["Gender"].isin(selected_genders)
    & df["Occupation"].isin(selected_occupations)
    & df["Sleep Disorder"].isin(selected_disorders)
].copy()

if filtered.empty:
    st.warning(
        "No records match the selected filters. Adjust the filters in the sidebar."
    )
    st.stop()


# -------------------- REUSABLE HELPERS ---------------------

def page_header(number, kicker, title, subtitle):
    st.markdown(
        f'<div class="kicker">FRAME {number:02d} · {kicker}</div>',
        unsafe_allow_html=True
    )

    st.title(title)

    st.markdown(
        f'<p class="subtle">{subtitle}</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")


def chart_style(fig, height=390):
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="DM Sans", size=12, color=INK),
        title_font=dict(family="DM Sans", size=17, color=BURGUNDY),
        margin=dict(l=28, r=20, t=58, b=35),
        legend_title_text=""
    )

    fig.update_xaxes(
        showgrid=True, gridcolor="#EEE8DF", zeroline=False, color=INK
    )

    fig.update_yaxes(
        showgrid=True, gridcolor="#EEE8DF", zeroline=False, color=INK
    )

    return fig


def show(fig, height=390):
    st.plotly_chart(chart_style(fig, height), use_container_width=True)


def correlation(x, y, data):
    pair = data[[x, y]].dropna()

    if len(pair) < 3 or pair[x].nunique() < 2 or pair[y].nunique() < 2:
        return np.nan, np.nan

    result = pearsonr(pair[x], pair[y])

    return float(result.statistic), float(result.pvalue)


def p_text(p):
    if pd.isna(p):
        return "Not available"

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


def add_kde_histogram(data, column, title, x_label, bins=10, color=SAFFRON):
    values = data[column].dropna().to_numpy()

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=values,
        nbinsx=bins,
        name="Number of people",
        marker_color=color,
        opacity=0.78
    ))

    if len(values) > 2 and np.std(values) > 0:
        grid = np.linspace(values.min() - 0.3, values.max() + 0.3, 300)
        kde = gaussian_kde(values)
        density = kde(grid)

        bin_width = (values.max() - values.min()) / bins
        scaled = density * len(values) * bin_width

        fig.add_trace(go.Scatter(
            x=grid,
            y=scaled,
            name="KDE curve",
            mode="lines",
            line=dict(color=BURGUNDY, width=3)
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title="Number of People",
        barmode="overlay",
        legend=dict(orientation="h", y=1.12, x=0)
    )

    return fig


# -------------------------- HEADER -------------------------

st.markdown(
    '<div class="kicker">SLEEP HEALTH & LIFESTYLE DATA ANALYSIS</div>',
    unsafe_allow_html=True
)

st.title("🌙 Somnia Insights")

st.markdown(
    '<p class="subtle">Explore how sleep duration, sleep quality, stress, physical activity '
    'and sleep disorders relate across 1,000 participant records.</p>',
    unsafe_allow_html=True
)


# ============================================================
# FRAME 01 — OVERVIEW
# ============================================================

if page.startswith("01"):

    page_header(
        1,
        "OVERVIEW",
        "The bigger picture of sleep",
        "A high-level view of the dataset, its key measures, and the first patterns emerging from the analysis."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total participants", f"{SOURCE_RECORDS:,}", "Source dataset")
    c2.metric("Average sleep duration", f"{filtered['Sleep Duration'].mean():.2f} hrs")
    c3.metric("Average sleep quality", f"{filtered['Quality of Sleep'].mean():.2f} / 10")
    c4.metric("Average stress level", f"{filtered['Stress Level'].mean():.2f} / 10")

    st.subheader("Overview graphs")

    left, right = st.columns(2)

    with left:
        fig = add_kde_histogram(
            filtered,
            "Sleep Duration",
            "Distribution of Sleep Duration",
            "Sleep Duration (hours)",
            bins=10
        )

        show(fig)

    with right:
        occ = filtered.groupby(
            "Occupation", as_index=False
        )["Quality of Sleep"].mean()

        occ = occ.sort_values("Quality of Sleep")

        fig = px.bar(
            occ,
            x="Quality of Sleep",
            y="Occupation",
            orientation="h",
            title="Average Sleep Quality by Occupation",
            labels={
                "Quality of Sleep": "Average Quality of Sleep (1–10)",
                "Occupation": ""
            },
            color_discrete_sequence=[BURGUNDY]
        )

        show(fig)

    r_duration, p_duration = correlation(
        "Sleep Duration", "Quality of Sleep", filtered
    )

    r_stress, p_stress = correlation(
        "Stress Level", "Quality of Sleep", filtered
    )

    r_activity, p_activity = correlation(
        "Physical Activity Level", "Quality of Sleep", filtered
    )

    st.subheader("Preliminary findings")

    st.markdown(
        f'<div class="insight"><b>Sleep duration → quality:</b> '
        f'{strength_label(r_duration).title()} {direction_label(r_duration)} association '
        f'(r = {r_duration:.4f}). Longer sleep duration tends to accompany higher reported sleep quality.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="insight"><b>Stress → quality:</b> '
        f'{strength_label(r_stress).title()} {direction_label(r_stress)} association '
        f'(r = {r_stress:.4f}). Higher stress tends to accompany lower reported sleep quality.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="insight"><b>Physical activity → quality:</b> '
        f'{strength_label(r_activity).title()} {direction_label(r_activity)} association '
        f'(r = {r_activity:.4f}). The relationship is positive but comparatively weak.</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Preliminary correlations are descriptive associations and do not establish cause and effect."
    )

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

elif page.startswith("02"):

    page_header(
        2,
        "THE DATA",
        "Dataset overview",
        "A structured view of the source data, its shape, and the variables powering this analysis."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total records", f"{SOURCE_RECORDS:,}", "Participant rows")
    c2.metric("Total variables", f"{SOURCE_VARIABLES}", "Across 3 data roles")
    c3.metric("Missing after cleaning", f"{CLEAN_MISSING}", "Complete analysis table")
    c4.metric("Duplicate records", f"{DUPLICATES}", "Unique rows")

    st.subheader("Data health")

    h1, h2, h3, h4 = st.columns(4)

    completeness = (
        100 if CLEAN_MISSING == 0
        else 100 * (1 - CLEAN_MISSING / df.size)
    )

    uniqueness = (
        100 if DUPLICATES == 0
        else 100 * (1 - DUPLICATES / SOURCE_RECORDS)
    )

    h1.metric("Completeness", f"{completeness:.0f}%")
    h2.metric("Unique records", f"{uniqueness:.0f}%")
    h3.metric("Numerical measures", "7")
    h4.metric("Categorical variables", "5")

    st.success("Ready for analysis · 1,000 participant rows retained.")

    st.markdown("### Source file")

    st.markdown(
        '<div class="research-card"><b>Sleep health and lifestyle</b><br>'
        '<span style="color:#625A55">A clean, complete snapshot of lifestyle and sleep indicators.</span><br><br>'
        '<code>Sleep_health_and_lifestyle_dataset_1000.csv</code></div>',
        unsafe_allow_html=True
    )

    st.subheader("Variable dictionary")
    st.caption("Names, types, and descriptions · 13 variables")

    dictionary = []

    for column in REQUIRED_COLUMNS:
        kind, description = VARIABLE_DESCRIPTIONS[column]

        dictionary.append({
            "Variable": column,
            "Type": kind,
            "Description": description,
            "Status": "Complete"
        })

    st.dataframe(
        pd.DataFrame(dictionary),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Dataset preview")

    preview = filtered[REQUIRED_COLUMNS].head(20).copy()

    preview = preview.rename(columns={
        "Person ID": "ID",
        "Sleep Duration": "Sleep duration",
        "Quality of Sleep": "Quality",
        "Physical Activity Level": "Activity",
        "Stress Level": "Stress",
        "BMI Category": "BMI",
        "Blood Pressure": "Blood pressure",
        "Heart Rate": "Heart rate",
        "Daily Steps": "Steps",
        "Sleep Disorder": "Disorder"
    })

    st.dataframe(
        preview,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        f"Data-cleaning note: the source CSV has {raw_disorder_missing} blank cells in "
        "'Sleep Disorder'. Following the cleaning decision in the analysis notebook, "
        "these are classified as 'None' (no disorder recorded). This preserves all 1,000 "
        "participants and leaves 0 missing values in the cleaned analysis table. "
        "The source file itself is not silently altered."
    )

    st.subheader("Download data")

    d1, d2 = st.columns(2)

    with d1:
        st.download_button(
            "Download cleaned dataset",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="somnia_cleaned_dataset.csv",
            mime="text/csv"
        )

    with d2:
        st.download_button(
            "Download original source CSV",
            data=raw_df.to_csv(index=False).encode("utf-8"),
            file_name="Sleep_health_and_lifestyle_dataset_1000.csv",
            mime="text/csv"
        )


# ============================================================
# FRAME 03 — EXPLORATORY ANALYSIS
# ============================================================

elif page.startswith("03"):

    page_header(
        3,
        "EXPLORATORY ANALYSIS",
        "The shape of sleep",
        "Start with the fundamentals. These distributions show how participants are spread across duration, quality, stress, and activity."
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Average duration",
        f"{filtered['Sleep Duration'].mean():.2f} hrs",
        f"Median: {filtered['Sleep Duration'].median():.1f} hrs"
    )

    m2.metric(
        "Average quality",
        f"{filtered['Quality of Sleep'].mean():.2f} / 10",
        f"Mode: {filtered['Quality of Sleep'].mode().iloc[0]:.0f} / 10"
    )

    m3.metric(
        "Average stress",
        f"{filtered['Stress Level'].mean():.2f} / 10",
        f"Mode: {filtered['Stress Level'].mode().iloc[0]:.0f} / 10"
    )

    m4.metric(
        "Average activity",
        f"{filtered['Physical Activity Level'].mean():.2f} min",
        "Daily average"
    )

    left, right = st.columns(2)

    with left:
        show(add_kde_histogram(
            filtered,
            "Sleep Duration",
            "Sleep duration distribution",
            "Sleep Duration (hours)",
            bins=10
        ))

    with right:
        fig = px.histogram(
            filtered,
            x="Quality of Sleep",
            nbins=10,
            title="Sleep quality distribution",
            labels={
                "Quality of Sleep": "Self-reported score (1–10)",
                "count": "Number of participants"
            },
            color_discrete_sequence=[BURGUNDY]
        )

        show(fig)

    left, right = st.columns(2)

    with left:
        fig = px.histogram(
            filtered,
            x="Stress Level",
            nbins=8,
            title="Stress level distribution",
            labels={
                "Stress Level": "Stress level (1–10)",
                "count": "Number of participants"
            },
            color_discrete_sequence=[SAFFRON]
        )

        show(fig)

    with right:
        fig = px.histogram(
            filtered,
            x="Physical Activity Level",
            nbins=10,
            title="Physical activity distribution",
            labels={
                "Physical Activity Level": "Activity level (minutes)",
                "count": "Number of participants"
            },
            color_discrete_sequence=["#A66A78"]
        )

        show(fig)

    st.subheader("Additional exploratory analysis")

    occupation_means = filtered.groupby(
        "Occupation", as_index=False
    )["Quality of Sleep"].mean()

    occupation_means = occupation_means.sort_values("Quality of Sleep")

    fig = px.bar(
        occupation_means,
        x="Quality of Sleep",
        y="Occupation",
        orientation="h",
        title="Average Sleep Quality by Occupation",
        labels={
            "Quality of Sleep": "Average Quality of Sleep",
            "Occupation": ""
        },
        color_discrete_sequence=[BURGUNDY]
    )

    show(fig)

    fig = px.scatter(
        filtered,
        x="Sleep Duration",
        y="Stress Level",
        title="Sleep Duration vs Stress Level",
        labels={
            "Sleep Duration": "Sleep Duration (hours)",
            "Stress Level": "Stress Level"
        },
        color_discrete_sequence=[BURGUNDY],
        opacity=.7
    )

    fig.update_traces(
        marker=dict(size=8, line=dict(width=1, color=SAFFRON))
    )

    show(fig)

    st.markdown(
        '<div class="insight"><b>Distribution observation:</b> In the full dataset, '
        'sleep durations are concentrated mainly between 6 and 8 hours. The sleep-duration '
        'versus stress scatterplot generally trends downward, suggesting that longer sleep '
        'is associated with lower stress in this sample.</div>',
        unsafe_allow_html=True
    )

    with st.expander("Numerical summary statistics"):
        summary = filtered[NUMERIC_MEASURES].describe().T

        summary.columns = [
            "Count", "Mean", "Std. deviation", "Minimum",
            "25th percentile", "Median", "75th percentile", "Maximum"
        ]

        st.dataframe(
            summary.round(2),
            use_container_width=True
        )


# ============================================================
# FRAME 04 — RELATIONSHIPS
# ============================================================

elif page.startswith("04"):

    page_header(
        4,
        "RELATIONSHIP ANALYSIS",
        "What moves with sleep quality?",
        "Focused comparisons connect sleep duration, physical activity, and stress directly to the quality of sleep reported by participants."
    )

    relationships = [
        (
            "Sleep Duration",
            "Quality of Sleep",
            "Sleep duration vs. quality",
            "Positive relationship"
        ),
        (
            "Physical Activity Level",
            "Quality of Sleep",
            "Physical activity vs. quality",
            "Weak positive relationship"
        ),
        (
            "Stress Level",
            "Quality of Sleep",
            "Stress level vs. quality",
            "Negative relationship"
        )
    ]

    for i in range(0, len(relationships), 1):

        x, y, title, relationship = relationships[i]

        r, p = correlation(x, y, filtered)

        st.markdown(f"### {title}")

        st.caption(
            f"{relationship} · Pearson r = {r:.4f} · p-value = {p_text(p)}"
        )

        fig = px.scatter(
            filtered,
            x=x,
            y=y,
            title=title,
            labels={
                "Sleep Duration": "Sleep Duration (hours)",
                "Physical Activity Level": "Physical Activity Level (minutes)",
                "Stress Level": "Stress Level",
                "Quality of Sleep": "Quality of Sleep (1–10)"
            },
            color_discrete_sequence=[BURGUNDY],
            opacity=.65
        )

        fig.update_traces(
            marker=dict(size=8, line=dict(width=.8, color=SAFFRON))
        )

        show(fig, 360)

        avg = filtered.groupby(x, as_index=False)[y].mean().sort_values(x)

        line = px.line(
            avg,
            x=x,
            y=y,
            markers=True,
            title=f"Average {y} across {x}",
            labels={x: x, y: f"Average {y}"},
            color_discrete_sequence=[SAFFRON]
        )

        line.update_traces(
            line=dict(width=3),
            marker=dict(size=8, color=BURGUNDY)
        )

        show(line, 330)

        st.markdown(
            f'<div class="insight"><b>Interpretation:</b> The observed relationship is '
            f'{strength_label(r)} and {direction_label(r)} (r = {r:.4f}). '
            f'{"The association is statistically significant at the 0.05 level." if p < .05 else "The association is not statistically significant at the 0.05 level."} '
            f'Correlation indicates association, not causation.</div>',
            unsafe_allow_html=True
        )

        if i < 2:
            st.markdown("---")

    st.subheader("Which factors show the strongest relationship with sleep quality?")

    corr_vars = [
        "Sleep Duration",
        "Age",
        "Physical Activity Level",
        "Daily Steps",
        "Heart Rate",
        "Stress Level"
    ]

    corr_rows = []

    for col in corr_vars:
        r, p = correlation(col, "Quality of Sleep", filtered)

        corr_rows.append({
            "Variable": col,
            "Pearson r": r,
            "p-value": p_text(p)
        })

    corr_df = pd.DataFrame(corr_rows).sort_values(
        "Pearson r", ascending=False
    )

    fig = px.bar(
        corr_df.sort_values("Pearson r"),
        x="Pearson r",
        y="Variable",
        orientation="h",
        title="Correlation with Quality of Sleep",
        color="Pearson r",
        color_continuous_scale=[
            "#A66A78", "#F3E9DA", "#C58B32"
        ],
        range_color=[-1, 1]
    )

    show(fig)

    st.dataframe(
        corr_df.round({"Pearson r": 4}),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Correlation heatmap")

    heat_columns = [
        "Age",
        "Sleep Duration",
        "Quality of Sleep",
        "Physical Activity Level",
        "Stress Level",
        "Heart Rate",
        "Daily Steps"
    ]

    corr_matrix = filtered[heat_columns].corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        zmin=-1,
        zmax=1,
        colorscale=[
            [0, "#A66A78"],
            [.5, "#FAF6EF"],
            [1, "#641C32"]
        ],
        text=np.round(corr_matrix.values, 2),
        texttemplate="%{text}",
        colorbar=dict(title="Pearson r")
    ))

    fig.update_layout(
        title="Correlation Between Numerical Variables",
        height=560
    )

    show(fig, 560)


# ============================================================
# FRAME 05 — SLEEP DISORDER COMPARISON
# ============================================================

elif page.startswith("05"):

    page_header(
        5,
        "SLEEP DISORDER COMPARISON",
        "Three different sleep profiles",
        "Compare group averages to understand how sleep duration, sleep quality, stress, and activity differ across disorder categories."
    )

    order = ["None", "Insomnia", "Sleep Apnea"]

    group_means = filtered.groupby("Sleep Disorder")[
        [
            "Sleep Duration",
            "Quality of Sleep",
            "Physical Activity Level",
            "Stress Level",
            "Heart Rate",
            "Daily Steps"
        ]
    ].mean().reindex(order).dropna(how="all")

    cards = st.columns(3)

    for col, group in zip(cards, order):
        if group in group_means.index:
            col.metric(
                group,
                f"{group_means.loc[group, 'Quality of Sleep']:.2f} / 10",
                "Average sleep quality"
            )

    st.subheader("Average sleep quality")

    fig = px.bar(
        group_means.reset_index(),
        x="Sleep Disorder",
        y="Quality of Sleep",
        color="Sleep Disorder",
        category_orders={"Sleep Disorder": order},
        title="Average Quality of Sleep by Disorder",
        labels={
            "Quality of Sleep": "Average Quality of Sleep (1–10)"
        },
        color_discrete_map={
            "None": BURGUNDY,
            "Insomnia": SAFFRON,
            "Sleep Apnea": "#A66A78"
        }
    )

    show(fig)

    st.subheader("Average sleep duration")

    fig = px.bar(
        group_means.reset_index(),
        x="Sleep Disorder",
        y="Sleep Duration",
        color="Sleep Disorder",
        category_orders={"Sleep Disorder": order},
        title="Average Sleep Duration by Disorder",
        labels={
            "Sleep Duration": "Average Sleep Duration (hours)"
        },
        color_discrete_map={
            "None": BURGUNDY,
            "Insomnia": SAFFRON,
            "Sleep Apnea": "#A66A78"
        }
    )

    show(fig)

    st.subheader("Full group comparison")

    st.dataframe(
        group_means.round(2),
        use_container_width=True
    )

    left, right = st.columns(2)

    with left:
        fig = px.box(
            filtered,
            x="Sleep Disorder",
            y="Quality of Sleep",
            category_orders={"Sleep Disorder": order},
            color="Sleep Disorder",
            title="Distribution of Sleep Quality by Disorder",
            color_discrete_map={
                "None": BURGUNDY,
                "Insomnia": SAFFRON,
                "Sleep Apnea": "#A66A78"
            }
        )

        show(fig)

    with right:
        fig = px.box(
            filtered,
            x="Sleep Disorder",
            y="Sleep Duration",
            category_orders={"Sleep Disorder": order},
            color="Sleep Disorder",
            title="Distribution of Sleep Duration by Disorder",
            color_discrete_map={
                "None": BURGUNDY,
                "Insomnia": SAFFRON,
                "Sleep Apnea": "#A66A78"
            }
        )

        show(fig)

    st.subheader("One-way ANOVA hypothesis tests")

    group_quality = [
        filtered.loc[
            filtered["Sleep Disorder"] == g,
            "Quality of Sleep"
        ].dropna()
        for g in order
        if g in filtered["Sleep Disorder"].unique()
    ]

    group_duration = [
        filtered.loc[
            filtered["Sleep Disorder"] == g,
            "Sleep Duration"
        ].dropna()
        for g in order
        if g in filtered["Sleep Disorder"].unique()
    ]

    if len(group_quality) >= 2 and all(len(g) > 0 for g in group_quality):

        f_q, p_q = f_oneway(*group_quality)
        f_d, p_d = f_oneway(*group_duration)

        a, b = st.columns(2)

        a.metric("Quality of Sleep · p-value", p_text(p_q))
        b.metric("Sleep Duration · p-value", p_text(p_d))

        st.write(
            f"Quality of Sleep: F = {f_q:.2f}, p = {p_text(p_q)}. "
            + (
                "The group means differ significantly at α = 0.05."
                if p_q < .05
                else "There is not sufficient evidence of a difference at α = 0.05."
            )
        )

        st.write(
            f"Sleep Duration: F = {f_d:.2f}, p = {p_text(p_d)}. "
            + (
                "The group means differ significantly at α = 0.05."
                if p_d < .05
                else "There is not sufficient evidence of a difference at α = 0.05."
            )
        )

        st.caption(
            "ANOVA tests whether at least one group mean differs; "
            "it does not identify which specific pairs differ."
        )

    else:
        st.info("Select at least two disorder groups to calculate ANOVA.")

    if set(order).issubset(set(group_means.dropna().index)):

        lowest = group_means["Quality of Sleep"].idxmin()

        st.markdown(
            f'<div class="insight"><b>The clearest difference:</b> '
            f'{lowest} has the lowest average sleep quality in the currently selected data '
            f'({group_means.loc[lowest, "Quality of Sleep"]:.2f}/10).</div>',
            unsafe_allow_html=True
        )


# ============================================================
# FRAME 06 — FINDINGS & CONCLUSION
# ============================================================

elif page.startswith("06"):

    page_header(
        6,
        "FINDINGS & CONCLUSION",
        "The story so far",
        "A concise readout of the analysis, organized around the five research questions and three formal hypotheses."
    )

    r_duration, p_duration = correlation(
        "Sleep Duration", "Quality of Sleep", filtered
    )

    r_activity, p_activity = correlation(
        "Physical Activity Level", "Quality of Sleep", filtered
    )

    r_stress, p_stress = correlation(
        "Stress Level", "Quality of Sleep", filtered
    )

    findings = [
        (
            "Sleep duration → quality",
            r_duration,
            "Participants with longer sleep duration generally report higher sleep quality."
        ),
        (
            "Stress → quality",
            r_stress,
            "Higher stress levels tend to coincide with lower reported sleep quality."
        ),
        (
            "Physical activity → quality",
            r_activity,
            "Physical activity shows a weaker positive association with sleep quality."
        )
    ]

    for title, r, description in findings:

        p_value = (
            p_duration if title.startswith("Sleep")
            else p_stress if title.startswith("Stress")
            else p_activity
        )

        st.markdown(
            f'<div class="insight"><b>{title} · {strength_label(r).title()} '
            f'{direction_label(r)} signal</b><br>{description}<br>'
            f'<b>Pearson r = {r:.4f}</b> · p = {p_text(p_value)}</div>',
            unsafe_allow_html=True
        )

    st.subheader("Research question results")

    rq_results = [
        (
            "RQ1 · Sleep duration and quality",
            f"Strong positive relationship (r = {r_duration:.4f}, p = {p_text(p_duration)})."
        ),
        (
            "RQ2 · Physical activity and sleep quality",
            f"Weak positive relationship (r = {r_activity:.4f}, p = {p_text(p_activity)})."
        ),
        (
            "RQ3 · Stress and sleep quality",
            f"Strong negative relationship (r = {r_stress:.4f}, p = {p_text(p_stress)})."
        ),
        (
            "RQ4 · Differences between disorder groups",
            "The group averages differ; one-way ANOVA tests the differences in sleep duration and quality."
        ),
        (
            "RQ5 · Strongest factors related to sleep quality",
            "Sleep duration and stress level show the strongest correlations with sleep quality among the measured variables."
        )
    ]

    for title, result in rq_results:
        st.markdown(
            f'<div class="research-card"><b>{title}</b><br>{result}</div>',
            unsafe_allow_html=True
        )

    st.subheader("Hypothesis testing summary")

    order = ["None", "Insomnia", "Sleep Apnea"]

    group_quality = [
        filtered.loc[
            filtered["Sleep Disorder"] == g,
            "Quality of Sleep"
        ].dropna()
        for g in order
        if g in filtered["Sleep Disorder"].unique()
    ]

    group_duration = [
        filtered.loc[
            filtered["Sleep Disorder"] == g,
            "Sleep Duration"
        ].dropna()
        for g in order
        if g in filtered["Sleep Disorder"].unique()
    ]

    p_anova_q = np.nan
    p_anova_d = np.nan

    if len(group_quality) >= 2 and all(len(g) > 0 for g in group_quality):
        p_anova_q = f_oneway(*group_quality).pvalue
        p_anova_d = f_oneway(*group_duration).pvalue

    h1_status = (
        "Reject H₀; H₁ supported"
        if p_duration < .05
        else "Fail to reject H₀"
    )

    h2_status = (
        "Reject H₀; H₁ supported"
        if p_stress < .05
        else "Fail to reject H₀"
    )

    h3_status = (
        "Reject H₀; H₁ supported"
        if (p_anova_q < .05 and p_anova_d < .05)
        else "Fail to reject H₀"
    )

    hypothesis_table = pd.DataFrame([
        {
            "Hypothesis": "H1 · Sleep duration and quality",
            "Test": "Pearson correlation",
            "Evidence": f"r = {r_duration:.4f}; p = {p_text(p_duration)}",
            "Decision": h1_status
        },
        {
            "Hypothesis": "H2 · Stress and quality",
            "Test": "Pearson correlation",
            "Evidence": f"r = {r_stress:.4f}; p = {p_text(p_stress)}",
            "Decision": h2_status
        },
        {
            "Hypothesis": "H3 · Disorder group differences",
            "Test": "One-way ANOVA",
            "Evidence": (
                f"Quality p = {p_text(p_anova_q)}; "
                f"Duration p = {p_text(p_anova_d)}"
            ),
            "Decision": h3_status
        }
    ])

    st.dataframe(
        hypothesis_table,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Conclusion")

    st.markdown(
        '<div class="research-card"><h3>Sleep quality is connected to lifestyle and sleep patterns.</h3>'
        'Across this 1,000-record dataset, sleep duration has a strong positive association '
        'with reported sleep quality, while stress has a strong negative association. '
        'Physical activity has a weaker positive association. The sleep-disorder groups '
        'also show differences in sleep duration and quality. These findings describe '
        'patterns and associations in this dataset; they do not prove that one factor causes another.'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Statistical results update when sidebar filters are changed. "
        "For the full-sample findings, leave all filters selected."
    )


# --------------------------- FOOTER ------------------------

st.markdown("---")

st.markdown(
    '<div style="text-align:center;color:#625A55;padding:12px;">'
    '<b style="color:#641C32;">🌙 Somnia Insights</b><br>'
    'Understanding Sleep · Exploring Health · Improving Lifestyle'
    '<br><small>Built with Streamlit, Pandas, Plotly and SciPy</small></div>',
    unsafe_allow_html=True
)