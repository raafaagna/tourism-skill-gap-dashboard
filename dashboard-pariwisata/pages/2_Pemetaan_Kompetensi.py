"""
Halaman 2: Pemetaan Kebutuhan Kompetensi Pariwisata
- Heatmap demand skill per subsektor (Top 15)
- Donut chart coverage score distribution
- Tabel coverage score lengkap
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Pemetaan Kompetensi | Dashboard Pariwisata", layout="wide", page_icon="🗂️")

from utils import inject_css, render_sidebar_header, section_title, insight_box, metric_card, page_header, PRIMARY, ACCENT, BG, TEXT, GRID, SUCCESS, WARNING, DANGER, base_layout, format_num, format_float
from data.demand_skill import get_df_demand_matrix, TOP15_SKILLS, SUBSEKTORS, get_top_skill_per_subsektor
from data.coverage_score import get_df_coverage, COVERAGE_COLOR

inject_css()
render_sidebar_header()

page_header(
    "Pemetaan Kebutuhan Kompetensi Pariwisata",
    "Demand skill per subsektor & status coverage pelatihan Kemnaker (Kementerian Ketenagakerjaan)",
    "🗂️",
)

# ── Summary Metrics ────────────────────────────────────────────────────────
df_cov = get_df_coverage()
n_full    = len(df_cov[df_cov["Score"] == 1.0])
n_partial = len(df_cov[df_cov["Score"] == 0.5])
n_none    = len(df_cov[df_cov["Score"] == 0.0])
avg_cov   = df_cov["Score"].mean() * 100

section_title("📊 Ringkasan Coverage Skill")
c1, c2, c3, c4 = st.columns(4)
with c1: metric_card("Total Demand Skill", str(len(df_cov)), "36 skill terstandarisasi", "📚", border_color=PRIMARY)
with c2: metric_card("Fully Covered", str(n_full), f"{format_float(n_full/len(df_cov)*100, 0)}% dari total", "✅", border_color=SUCCESS)
with c3: metric_card("Partially Covered", str(n_partial), f"{format_float(n_partial/len(df_cov)*100, 0)}% dari total", "⚠️", border_color=WARNING)
with c4: metric_card("Not Covered", str(n_none), f"{format_float(n_none/len(df_cov)*100, 0)}% — perlu perhatian", "❌", border_color=DANGER)


# ── Heatmap Demand Skill per Subsektor ────────────────────────────────────
section_title("🔥 Pemetaan Tingkat Demand Skill per Subsektor (Top 15)")

df_matrix = get_df_demand_matrix()

# Shorten subsektor labels
short_labels = {
    "Daya Tarik Wisata": "Daya Tarik Wisata",
    "Jasa Informasi Pariwisata": "Jasa Informasi",
    "Jasa Konsultan Pariwisata": "Jasa Konsultan",
    "Jasa Makanan dan Minuman": "Makanan & Minuman",
    "Jasa Perjalanan Wisata": "Perjalanan Wisata",
    "Jasa Pramuwisata": "Pramuwisata",
    "Jasa Transportasi Wisata": "Transportasi",
    "Kawasan Pariwisata": "Kawasan Pariwisata",
    "Penyediaan Akomodasi": "Akomodasi",
    "Penyelenggara Kegiatan Hiburan & Rekreasi": "Hiburan & Rekreasi",
    "Penyelenggaraan Acara (MICE)": "MICE (Meeting, Incentive, Convention, and Exhibition)",
    "SPA": "SPA",
}

z_values = df_matrix.values
x_labels = [s[:22] + "…" if len(s) > 22 else s for s in df_matrix.columns]
y_labels = [short_labels.get(s, s) for s in df_matrix.index]

# Build text annotations
text_vals = [[f"{format_float(v, 1)}" for v in row] for row in z_values]

fig_heat = go.Figure(data=go.Heatmap(
    z=z_values,
    x=x_labels,
    y=y_labels,
    text=text_vals,
    texttemplate="%{text}",
    textfont=dict(size=8.5, color="white", family="DM Sans"),
    colorscale=[
        [0.0, "#ebc26c"],
        [1.0, "#142c50"],
    ],
    colorbar=dict(
        title=dict(text="Bobot (%)", font=dict(size=11)),
        thickness=14,
        len=0.8,
        tickfont=dict(size=10),
    ),
    hovertemplate="<b>%{y}</b><br>Skill: %{x}<br>Bobot: %{z:.1f}%<extra></extra>",
    zmin=0,
    zmax=55,
))

fig_heat.update_layout(
    height=440,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Inter", size=11, color=TEXT),
    margin=dict(l=140, r=20, t=40, b=120),
    xaxis=dict(
        tickangle=-40,
        tickfont=dict(size=9),
        side="bottom",
    ),
    yaxis=dict(
        tickfont=dict(size=10),
        autorange="reversed",
    ),
)

st.plotly_chart(fig_heat, width='stretch')
insight_box(
    "Sebanyak <b>50,5%</b> dari subsektor <b>Jasa Pramuwisata</b> mencari tenaga kerja dengan keahlian spesifik di bidang <b>Pemanduan Wisata</b>. "
    "Sebanyak <b>66,1%</b> dari subsektor industri <b>SPA</b> mencari tenaga kerja dengan keahlian spesifik di bidang <b>Perawatan SPA</b>. "
    "Sebanyak <b>50,0%</b> dari subsektor <b>Jasa Informasi</b> mencari tenaga kerja dengan keahlian spesifik di bidang <b>Pengolahan Makanan</b>."
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Bar Chart: Top skill per subsektor ──────────────────────────────────────
section_title("🏅 Skill Utama per Subsektor")
df_top = get_top_skill_per_subsektor()

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=df_top["Bobot (%)"],
    y=[short_labels.get(s, s) for s in df_top["Subsektor"]],
    orientation="h",
    marker=dict(
        color=df_top["Bobot (%)"],
        colorscale=[[0, "#b0c4de"], [1.0, PRIMARY]],
        showscale=False,
        line=dict(color="rgba(0,0,0,0)", width=0)
    ),
    text=[f"{r['Top Skill']} ({format_float(r['Bobot (%)'], 1)}%)" for _, r in df_top.iterrows()],
    textposition="outside",
    insidetextanchor="start",
    textfont=dict(size=10, color=TEXT, family="DM Sans"),
    hovertemplate="<b>%{y}</b><br>Skill Utama: %{text}<extra></extra>",
))

layout = base_layout("", height=420)
layout["xaxis"]["title"] = "Bobot Demand (%)"
layout["xaxis"]["range"] = [0, df_top["Bobot (%)"].max() * 1.5]
layout["margin"] = dict(l=140, r=20, t=50, b=20)
layout["yaxis"]["tickfont"] = dict(size=10)
fig_bar.update_layout(**layout)
st.plotly_chart(fig_bar, width='stretch')

st.markdown("<br>", unsafe_allow_html=True)

# ── Row: Donut coverage + Tabel Coverage Score ──────────────────────────────
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    section_title("🎯 Distribusi Coverage Score Demand Skill")

    labels = ["Fully Covered", "Partially Covered", "Not Covered"]
    values = [n_full, n_partial, n_none]
    colors_donut = ["#2ecc71", "#ebc26c", "#e74c3c"]

    fig_donut = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors_donut, line=dict(color="white", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11, family="Inter", color="white"),
        hovertemplate="<b>%{label}</b><br>%{value} skill (%{percent})<extra></extra>",
    )])

    fig_donut.add_annotation(
        text=f"<span style='font-size:28px; font-weight:800; color:{PRIMARY}'>{avg_cov:.0f}%</span><br><span style='font-size:12px; color:#64748b'>Rata-rata<br>Coverage</span>",
        x=0.5, y=0.5,
        showarrow=False,
        align="center",
    )

    fig_donut.update_layout(
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter", size=12),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
        showlegend=True,
    )
    st.plotly_chart(fig_donut, width='stretch')

    insight_box(
        f"Dari 36 demand skill, <b>{n_full} skill ({format_float(n_full/36*100, 0)}%) sudah fully covered</b> dalam pelatihan Kemnaker (Kementerian Ketenagakerjaan). "
        f"<b>{n_partial} skill ({format_float(n_partial/36*100, 0)}%) baru sebagian tercakup</b>, dan "
        f"<b>K3 (Kesehatan dan Keselamatan Kerja) ({n_none} skill) sama sekali belum ada modul pelatihannya</b> — ini merupakan gap kritis yang perlu segera ditangani."
    )

with col_right:
    section_title("📋 Tabel Coverage Score Seluruh Demand Skill")

    status_filter = st.selectbox(
        "Filter berdasarkan status coverage:",
        ["Semua", "Fully Covered", "Partially Covered", "Not Covered"],
        key="cov_filter",
    )

    df_show = df_cov.copy()
    if status_filter != "Semua":
        df_show = df_show[df_show["Status"] == status_filter]
        
    # Menghapus kolom Score sesuai permintaan
    if "Score" in df_show.columns:
        df_show = df_show.drop(columns=["Score"])

    def color_status(val):
        if val == "Fully Covered":
            return "background-color: #e8f8f0; color: #1a7a47; font-weight: 600;"
        elif val == "Partially Covered":
            return "background-color: #fef9ec; color: #b8860b; font-weight: 600;"
        else:
            return "background-color: #fdf0ee; color: #c0392b; font-weight: 600;"

    styled = df_show.style.map(color_status, subset=["Status"])
    st.dataframe(styled, width='stretch', hide_index=True, height=450)
    
    csv = df_show.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Unduh Data Coverage Score (CSV)",
        data=csv,
        file_name="tabel_coverage_score_demand_skill.csv",
        mime="text/csv",
    )
