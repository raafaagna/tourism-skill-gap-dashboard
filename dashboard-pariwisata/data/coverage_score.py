"""
Data Coverage Score & Gap Score per Demand Skill dan Subsektor
Sumber: Hasil analisis SKKNI vs Materi Pelatihan Kemnaker
(Kini dinamis mengambil dari Excel via gap_score.py)
"""

import pandas as pd
import streamlit as st
from data.gap_score import get_original_similarities_and_coverages, get_base_gap_scores

_orig_data = get_original_similarities_and_coverages()
COVERAGE_SCORE = {skill: d['cov'] for skill, d in _orig_data.items()}
GAP_SCORE = get_base_gap_scores()

COVERAGE_LABEL = {
    1.0: "Fully Covered",
    0.5: "Partially Covered",
    0.0: "Not Covered",
}

COVERAGE_COLOR = {
    1.0: "#2ecc71",
    0.5: "#ebc26c",
    0.0: "#e74c3c",
}

@st.cache_data
def get_df_coverage():
    data = []
    for skill, d in _orig_data.items():
        cov = d['cov']
        sim = d['sim']
        status = COVERAGE_LABEL.get(cov, "Unknown")
        sim_pct = f"{sim * 100:.2f}%"
        data.append((skill, cov, sim_pct, status))
        
    df = pd.DataFrame(
        data,
        columns=["Demand Skill", "Score", "Similarity (%)", "Status"],
    ).sort_values("Score", ascending=False)
    return df

@st.cache_data
def get_df_gap():
    df = pd.DataFrame(
        list(GAP_SCORE.items()), columns=["Subsektor", "Gap_Score"]
    ).sort_values("Gap_Score", ascending=True)
    return df
