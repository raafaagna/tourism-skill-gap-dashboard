"""
Halaman 1: Profil Tenaga Kerja Pariwisata Indonesia
- Map chart sebaran per provinsi
- Proyeksi nasional 2024-2029
- Growth rate per provinsi
- Top 10 kebutuhan pembinaan SDM
- Ringkasan statistik
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Profil Tenaga Kerja | Dashboard Pariwisata", layout="wide", page_icon="🧑‍💼")

from utils import inject_css, render_sidebar_header, section_title, insight_box, metric_card, page_header, PRIMARY, ACCENT, BG, LIGHT_BG, TEXT, GRID, SEQUENTIAL, base_layout
from data.tenaga_kerja import get_df_provinsi, get_df_proyeksi, get_df_growth, get_df_top10_pembinaan, SUMMARY

inject_css()
render_sidebar_header()

page_header(
    "Profil Tenaga Kerja Pariwisata Indonesia",
    "Sebaran, proyeksi, dan kebutuhan pembinaan SDM pariwisata seluruh provinsi",
    "🧑‍💼",
)

# ── Summary Metrics ────────────────────────────────────────────────────────
section_title("📊 Ringkasan Nasional", "")
c1, c2, c3, c4, c5 = st.columns(5)
with c1: metric_card("Total TK 2024", "24,887,456", "IRTS Nasional")
with c2: metric_card("Total TK 2029", "30,007,770", "Proyeksi 5 Tahun")
with c3: metric_card("Growth 2024–2029", "20.57%", "CAGR Nasional", "📈")
with c4: metric_card("Total Provinsi", "38", "Seluruh Indonesia", "🗺️")
with c5: metric_card("Subsektor", "12", "Sektor Pariwisata", "🏨")

st.markdown("<br>", unsafe_allow_html=True)

# ── Map Chart ──────────────────────────────────────────────────────────────
section_title("🗺️ Sebaran Tenaga Kerja Pariwisata per Provinsi (2025)")

df_prov = get_df_provinsi()

@st.cache_data
def load_geojson():
    import urllib.request, json
    url_geojson = "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson"
    try:
        req = urllib.request.Request(url_geojson, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            # Override id bawaan dengan string provinsi agar mapping Plotly tidak salah
            for f in data.get('features', []):
                f['id'] = f['properties']['Propinsi']
            return data
    except Exception as e:
        return None

geojson_data = load_geojson()

PROV_MAP = {
    "Aceh": "DI. ACEH", "Sumatera Utara": "SUMATERA UTARA", "Sumatera Barat": "SUMATERA BARAT",
    "Riau": "RIAU", "Jambi": "JAMBI", "Sumatera Selatan": "SUMATERA SELATAN",
    "Bengkulu": "BENGKULU", "Lampung": "LAMPUNG", "Bangka Belitung": "BANGKA BELITUNG",
    "Kepulauan Riau": "KEPULAUAN RIAU", "DKI Jakarta": "DKI JAKARTA", "Jawa Barat": "JAWA BARAT",
    "Jawa Tengah": "JAWA TENGAH", "DI Yogyakarta": "DAERAH ISTIMEWA YOGYAKARTA", "Jawa Timur": "JAWA TIMUR",
    "Banten": "BANTEN", "Bali": "BALI", "NTB": "NUSATENGGARA BARAT", "NTT": "NUSA TENGGARA TIMUR",
    "Kalimantan Barat": "KALIMANTAN BARAT", "Kalimantan Tengah": "KALIMANTAN TENGAH",
    "Kalimantan Selatan": "KALIMANTAN SELATAN", "Kalimantan Timur": "KALIMANTAN TIMUR",
    "Kalimantan Utara": "KALIMANTAN UTARA", "Sulawesi Utara": "SULAWESI UTARA",
    "Sulawesi Tengah": "SULAWESI TENGAH", "Sulawesi Selatan": "SULAWESI SELATAN",
    "Sulawesi Tenggara": "SULAWESI TENGGARA", "Gorontalo": "GORONTALO", "Sulawesi Barat": "SULAWESI BARAT",
    "Maluku": "MALUKU", "Maluku Utara": "MALUKU UTARA", "Papua Barat": "PAPUA BARAT", "Papua": "PAPUA",
    "Papua Tengah": "PAPUA", "Papua Pegunungan": "PAPUA", "Papua Selatan": "PAPUA", "Papua Barat Daya": "PAPUA BARAT",
}

if geojson_data:
    df_map = df_prov.copy()
    df_map["geojson_key"] = df_map["Provinsi"].map(PROV_MAP)
    df_map = df_map.groupby("geojson_key", as_index=False).agg({
        "Jumlah_TK": "sum", "Binaan_2025": "sum"
    })
    df_map["hover"] = df_map.apply(
        lambda r: f"<b>{r['geojson_key'].title()}</b><br>TK 2025: {r['Jumlah_TK']:,}<br>Kebutuhan Binaan: {r['Binaan_2025']:,}", axis=1
    )

    fig_map = go.Figure(go.Choropleth(
        geojson=geojson_data,
        featureidkey="properties.Propinsi",
        locations=df_map["geojson_key"],
        z=df_map["Jumlah_TK"],
        colorscale=[
            [0.0, "#e2e8f0"],   # Warna dasar daratan (abu-abu terang) agar tidak mirip air
            [0.02, "#a8cdf0"],  # Biru muda untuk provinsi menengah ke bawah
            [0.15, "#4f9be0"],  # Biru untuk provinsi menengah
            [0.5, "#1e4a85"],   # Biru gelap untuk provinsi padat
            [1.0, "#142c50"]    # Biru sangat gelap untuk Jawa
        ],
        showscale=True,
        colorbar=dict(
            title=dict(text="Jumlah TK", font=dict(size=11, color=TEXT)),
            thickness=14, len=0.7, tickfont=dict(size=10),
        ),
        text=df_map["hover"],
        hovertemplate="%{text}<extra></extra>",
        marker_line_color="white",
        marker_line_width=0.5,
    ))
    fig_map.update_layout(
        geo=dict(
            fitbounds="locations", 
            visible=False,
            bgcolor="white",
            showocean=False,
        ),
        height=550,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.error("Gagal memuat data GeoJSON Peta Indonesia.")
insight_box(
    "<b>Konsentrasi TK Pariwisata</b>: Jawa Barat (5.59 juta), Jawa Timur (3.95 juta), dan Jawa Tengah (3.28 juta) "
    "mendominasi total TK pariwisata nasional. Provinsi di luar Pulau Jawa, terutama Papua dan Maluku, "
    "memiliki jumlah TK yang jauh lebih rendah namun potensi pertumbuhan yang tinggi."
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 2: Proyeksi Tenaga Kerja ──────────────────────────────────────────
section_title("📈 Proyeksi Tenaga Kerja Pariwisata Nasional (2024–2029)")
df_proj = get_df_proyeksi()

fig_proj = go.Figure()
fig_proj.add_trace(go.Scatter(
    x=df_proj["Tahun"],
    y=df_proj["Jumlah_TK"],
    mode="lines+markers+text",
    line=dict(color=PRIMARY, width=3),
    marker=dict(color=ACCENT, size=10, line=dict(color=PRIMARY, width=2)),
    text=[f"{v/1e6:.2f}M" for v in df_proj["Jumlah_TK"]],
    textposition="top center",
    textfont=dict(size=10, color=PRIMARY, family="Inter"),
    fill="tozeroy",
    fillcolor=f"rgba(20,44,80,0.07)",
    name="TK Pariwisata",
    hovertemplate="<b>%{x}</b><br>%{y:,.0f} tenaga kerja<extra></extra>",
))

layout = base_layout("", height=370)
layout["xaxis"]["tickvals"] = list(df_proj["Tahun"])
layout["yaxis"]["tickformat"] = ".2s"
layout["yaxis"]["title"] = "Jumlah Tenaga Kerja"
fig_proj.update_layout(**layout)
st.plotly_chart(fig_proj, use_container_width=True)
insight_box(
    "Proyeksi menunjukkan pertumbuhan <b>stabil ~4% per tahun</b>, "
    "dari 24,9 juta (2024) menuju 30,0 juta (2029). "
    "Pertumbuhan ini membutuhkan penyiapan kapasitas pelatihan yang memadai."
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 3: Growth Rate ────────────────────────────────────────────────────
section_title("📊 Growth Rate Tenaga Kerja per Provinsi (2024–2029)")
df_gr = get_df_growth().tail(38)

fig_gr = go.Figure()
fig_gr.add_trace(go.Bar(
    x=df_gr["Growth_Rate"],
    y=df_gr["Provinsi"],
    orientation="h",
    marker=dict(
        color=df_gr["Growth_Rate"],
        colorscale=[[0, "#9bb5d0"], [0.5, "#2282d8"], [1.0, PRIMARY]],
        showscale=False,
    ),
    text=[f"{v:.1f}%" for v in df_gr["Growth_Rate"]],
    textposition="outside",
    textfont=dict(size=9),
    hovertemplate="<b>%{y}</b><br>Growth Rate: %{x:.1f}%<extra></extra>",
))

layout = base_layout("", height=700)
layout["margin"] = dict(l=130, r=60, t=20, b=20)
layout["xaxis"]["title"] = "Growth Rate (%)"
layout["yaxis"]["tickfont"] = dict(size=9)
fig_gr.update_layout(**layout)
st.plotly_chart(fig_gr, use_container_width=True)
insight_box(
    "<b>Kepulauan Riau (48.2%)</b> dan <b>NTB (45.1%)</b> mencatat proyeksi growth tertinggi, "
    "mencerminkan potensi pengembangan pariwisata yang pesat di wilayah tersebut. "
    "Bali justru mencatat growth terendah (10.5%) karena basis TK-nya sudah besar."
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 3: Top 10 Pembinaan & Tabel ───────────────────────────────────────
col_a, col_b = st.columns([1, 1], gap="large")

with col_a:
    section_title("🏆 Top 10 Provinsi Kebutuhan Pembinaan SDM Terbesar (2029)")
    df_top10 = get_df_top10_pembinaan()

    colors = [ACCENT if i >= 7 else PRIMARY for i in range(len(df_top10))]

    fig_top10 = go.Figure()
    fig_top10.add_trace(go.Bar(
        x=df_top10["Jumlah_SDM"],
        y=df_top10["Provinsi"],
        orientation="h",
        marker=dict(color=colors[::-1]),
        text=[f"{v:,}" for v in df_top10["Jumlah_SDM"]],
        textposition="outside",
        textfont=dict(size=10, color=TEXT),
        hovertemplate="<b>%{y}</b><br>Kebutuhan Binaan: %{x:,} orang<extra></extra>",
    ))

    layout = base_layout("", height=370)
    layout["xaxis"]["title"] = "Jumlah SDM yang perlu dibina"
    layout["margin"] = dict(l=130, r=80, t=50, b=20)
    layout["yaxis"]["tickfont"] = dict(size=10)
    fig_top10.update_layout(**layout)
    st.plotly_chart(fig_top10, use_container_width=True)
    insight_box(
        "<b>Bangka Belitung</b> dan <b>Papua Barat</b> menjadi provinsi dengan kebutuhan pembinaan SDM "
        "tertinggi pada 2029. Kebutuhan ini dihitung sebesar <b>8% dari total TK IRTS</b> "
        "sebagai estimasi target pembinaan tahunan."
    )

with col_b:
    section_title("📋 Tabel Ringkasan Tenaga Kerja per Provinsi")
    df_show = df_prov[["Provinsi", "Jumlah_TK", "Growth_Rate", "TK_2029", "Binaan_2029"]].copy()
    df_show.columns = ["Provinsi", "TK 2025", "Growth (%)", "TK 2029 (Proj.)", "Binaan 2029"]
    df_show = df_show.sort_values("TK 2025", ascending=False).reset_index(drop=True)
    df_show["TK 2025"] = df_show["TK 2025"].apply(lambda x: f"{x:,}")
    df_show["Growth (%)"] = df_show["Growth (%)"].apply(lambda x: f"{x:.1f}%")
    df_show["TK 2029 (Proj.)"] = df_show["TK 2029 (Proj.)"].apply(lambda x: f"{x:,}")
    df_show["Binaan 2029"] = df_show["Binaan 2029"].apply(lambda x: f"{x:,}")

    st.dataframe(
        df_show,
        use_container_width=True,
        height=360,
        hide_index=True,
    )
    insight_box(
        "Data binaan dihitung sebesar 8% dari total TK pariwisata (IRTS) per provinsi, "
        "sesuai dengan estimasi kebutuhan pembinaan SDM yang ditetapkan Kemenpar."
    )