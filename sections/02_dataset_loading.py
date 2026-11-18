# 3. DATASET DEFINITIONS AND LOADING

from pathlib import Path

import pandas as pd
import streamlit as st


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


# Load, validate, and clean the source data.
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


# Load the dataset and calculate source-level summary values.
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


