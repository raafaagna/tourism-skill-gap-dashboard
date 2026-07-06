"""
Halaman 3: Analisis Kesenjangan Kompetensi Tenaga Kerja Pariwisata
- Bar chart gap score per subsektor
- Gauge chart untuk subsektor tertentu
- Tabel detail gap
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Analisis Kesenjangan | Dashboard Pariwisata", layout="wide", page_icon="📉")

from utils import inject_css, render_sidebar_header, section_title, insight_box, metric_card, page_header, PRIMARY, ACCENT, TEXT, GRID, DANGER, SUCCESS, WARNING, base_layout, format_num, format_float
from data.coverage_score import get_df_gap, GAP_SCORE

inject_css()
render_sidebar_header()

page_header(
    "Analisis Kesenjangan Kompetensi Tenaga Kerja Pariwisata",
    "Tingkat gap kompetensi per subsektor berdasarkan perbandingan demand skill vs training supply",
    "📉",
)

df_gap = get_df_gap()
max_gap_sub = df_gap.sort_values("Gap_Score", ascending=False).iloc[0]
min_gap_sub = df_gap.sort_values("Gap_Score", ascending=True).iloc[-1]
avg_gap = df_gap["Gap_Score"].mean()

# ── Metrics ────────────────────────────────────────────────────────────────
section_title("📊 Ringkasan Gap Kompetensi")
c1, c2, c3, c4 = st.columns(4)
with c1: metric_card("Gap Tertinggi", f"{format_float(max_gap_sub['Gap_Score'], 2)}%", max_gap_sub["Subsektor"], "🔴", border_color=DANGER, height="auto")
with c2: metric_card("Rata-rata Gap", f"{format_float(avg_gap, 2)}%", "Seluruh subsektor", "📊", border_color="#7bb4e8", height="auto")
with c3: metric_card("Subsektor Nol Gap", "1", "Jasa Transportasi Wisata", "✅", border_color=SUCCESS, height="auto")
with c4: metric_card("Subsektor Kritis", "2", "Gap ≥ 15,73%", "⚠️", border_color=WARNING, height="auto")


# ── Main Gap Chart ─────────────────────────────────────────────────────────
section_title("📉 Tingkat Kesenjangan Kompetensi Tenaga Kerja per Subsektor")

# Sort ascending (horizontal bar)
df_sorted = df_gap.sort_values("Gap_Score", ascending=True)

def get_bar_color(subsektor):
    sub_lower = subsektor.lower()
    if "spa" in sub_lower:
        return DANGER
    elif "mice" in sub_lower:
        return WARNING
    else:
        return "#4f9be0"

colors = [get_bar_color(sub) for sub in df_sorted["Subsektor"]]

fig_gap = go.Figure()
fig_gap.add_trace(go.Bar(
    x=df_sorted["Gap_Score"],
    y=df_sorted["Subsektor"],
    orientation="h",
    marker=dict(color=colors, line=dict(color="white", width=0.5)),
    text=[f"{format_float(v, 2)}%" for v in df_sorted["Gap_Score"]],
    textposition="outside",
    textfont=dict(size=10.5, color=TEXT, family="DM Sans"),
    hovertemplate="<b>%{y}</b><br>Gap Score: %{x:.2f}%<extra></extra>",
    width=0.65,
))

# Add threshold line at 15.73%
fig_gap.add_vline(
    x=15.73,
    line_dash="dash",
    line_color=DANGER,
    line_width=1.5,
    annotation_text="Ambang Kritis (15,73%)",
    annotation_position="bottom right",
    annotation_font=dict(size=10, color=DANGER),
)

# Add threshold line at 8.33%
fig_gap.add_vline(
    x=8.33,
    line_dash="dot",
    line_color=WARNING,
    line_width=1,
    annotation_text="Waspada (8,33%)",
    annotation_position="bottom right",
    annotation_font=dict(size=9, color=WARNING),
)

layout = base_layout("", height=480)
layout["xaxis"]["title"] = "Tingkat Kesenjangan / Gap (%)"
layout["xaxis"]["range"] = [0, 38]
layout["margin"] = dict(l=200, r=80, t=60, b=40)
layout["yaxis"]["tickfont"] = dict(size=11)
fig_gap.update_layout(**layout)

st.plotly_chart(fig_gap, width='stretch')
insight_box(
    "Subsektor <b>SPA (Sanus Per Aquam) (32,38%)</b> berada pada tingkat kritis (merah), sedangkan <b>MICE (Meeting, Incentive, Convention, and Exhibition) (15,73%)</b> berada pada tingkat waspada (kuning), menandakan kebutuhan peningkatan kurikulum pelatihan yang mendesak pada kedua subsektor tersebut. <b>Jasa Transportasi Wisata (0%)</b> adalah satu-satunya subsektor tanpa kesenjangan, sementara subsektor lainnya tergolong rendah (biru)."
)

st.markdown("<br>", unsafe_allow_html=True)



# ── Tabel Lengkap ─────────────────────────────────────────────────────────
section_title("📋 Tabel Lengkap Gap Score per Subsektor")

df_table = df_gap.sort_values("Gap_Score", ascending=False).copy()

def get_kategori(subsektor, gap):
    sub_lower = subsektor.lower()
    if gap == 0:
        return "✅ Tidak Ada Gap"
    elif "spa" in sub_lower:
        return "🔴 Kritis"
    elif "mice" in sub_lower:
        return "⚠️ Waspada"
    else:
        return "🔵 Rendah"

df_table["Kategori"] = df_table.apply(lambda row: get_kategori(row["Subsektor"], row["Gap_Score"]), axis=1)
df_table["Gap_Score"] = df_table["Gap_Score"].apply(lambda x: f"{format_float(x, 2)}%")
df_table.columns = ["Subsektor", "Gap Score", "Kategori"]
df_table = df_table.reset_index(drop=True)

def highlight_gap(row):
    if "Kritis" in row["Kategori"]:
        return ["background-color: #fdf0ee"] * len(row)
    elif "Waspada" in row["Kategori"]:
        return ["background-color: #fef9ec"] * len(row)
    elif "Tidak Ada" in row["Kategori"]:
        return ["background-color: #e8f8f0"] * len(row)
    return [""] * len(row)

styled_table = df_table.style.apply(highlight_gap, axis=1)
st.dataframe(styled_table, width='stretch', hide_index=True)

csv_df = df_table.copy()
csv_df["Kategori"] = csv_df["Kategori"].str.replace(r'^[^\w\s]+\s*', '', regex=True)
csv = csv_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Unduh Data Gap Score (CSV)",
    data=csv,
    file_name="tabel_lengkap_gap_score_subsektor.csv",
    mime="text/csv",
)
