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

# Execute sections in order in this namespace to preserve the original script behavior.
_SECTION_DIR = Path(__file__).with_name("sections")
for _section_name in (
    "01_setup_and_styles.py",
    "02_dataset_loading.py",
    "03_sidebar_filters.py",
    "04_reusable_helpers.py",
    "05_dashboard_pages.py",
    "06_navigation_footer.py",
):
    _section_path = _SECTION_DIR / _section_name
    _section_source = _section_path.read_text(encoding="utf-8")
    exec(compile(_section_source, str(_section_path), "exec"), globals())
