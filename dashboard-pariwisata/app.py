"""
Dashboard Analisis Kesenjangan Kompetensi Tenaga Kerja Pariwisata Indonesia
dan Simulator Pelatihan

Kelompok 8 SDC SD-A2
FTMM – Universitas Airlangga × Kementerian Pariwisata RI
"""

import streamlit as st

st.set_page_config(
    page_title="Dashboard Kompetensi Pariwisata Indonesia",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Dashboard Analisis Kesenjangan Kompetensi Tenaga Kerja Pariwisata Indonesia | Kelompok 8 SDC SD-A2 FTMM Unair × Kemenpar",
    },
)

from utils import inject_css, render_sidebar_header

inject_css()
render_sidebar_header()

# ── Landing Page ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #142c50 0%, #1e4a85 100%);
                border-radius: 16px; padding: 56px 40px; margin-bottom: 32px; text-align: center;
                box-shadow: 0 8px 32px rgba(20,44,80,0.15);">
        <div style="font-size: 3.5rem; margin-bottom: 16px; line-height: 1;">🏝️</div>
        <h1 style="color: white; font-size: 2.2rem; margin: 0 0 12px; font-weight: 800; letter-spacing: -0.5px;">
            Dashboard Analisis Kesenjangan Kompetensi<br>Tenaga Kerja Pariwisata Indonesia
        </h1>
        <p style="color: #cbd5e1; font-size: 1.05rem; margin: 0 0 32px; font-weight: 400;">
            Simulator Pelatihan &amp; Pemetaan Kebutuhan SDM Pariwisata 38 Provinsi
        </p>
        <div style="display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.1); color: #ffffff; border: 1px solid rgba(255,255,255,0.2);
                         padding: 8px 20px; border-radius: 30px; font-size: 0.85rem; font-weight: 600; backdrop-filter: blur(4px);">
                📊 12 Subsektor
            </span>
            <span style="background: rgba(255,255,255,0.1); color: #ffffff; border: 1px solid rgba(255,255,255,0.2);
                         padding: 8px 20px; border-radius: 30px; font-size: 0.85rem; font-weight: 600; backdrop-filter: blur(4px);">
                🗺️ 38 Provinsi
            </span>
            <span style="background: rgba(255,255,255,0.1); color: #ffffff; border: 1px solid rgba(255,255,255,0.2);
                         padding: 8px 20px; border-radius: 30px; font-size: 0.85rem; font-weight: 600; backdrop-filter: blur(4px);">
                📚 36 Demand Skill
            </span>
            <span style="background: rgba(255,255,255,0.1); color: #ffffff; border: 1px solid rgba(255,255,255,0.2);
                         padding: 8px 20px; border-radius: 30px; font-size: 0.85rem; font-weight: 600; backdrop-filter: blur(4px);">
                🔬 Data Kemenpar × Kemnaker
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Navigation Cards ──────────────────────────────────────────────────────────
st.markdown("### 📂 Navigasi Dashboard")
st.markdown("Pilih halaman melalui menu sidebar kiri, atau klik ringkasan di bawah ini:")

cols = st.columns(5)
pages = [
    ("🧑‍💼", "Profil Tenaga Kerja", "Sebaran, proyeksi, dan kebutuhan pembinaan SDM per provinsi", "#/1_Profil_Tenaga_Kerja"),
    ("🗂️", "Pemetaan Kompetensi", "Demand skill per subsektor & coverage pelatihan", "#/2_Pemetaan_Kompetensi"),
    ("📉", "Analisis Kesenjangan", "Gap score per subsektor dan coverage tiap skill", "#/3_Analisis_Kesenjangan"),
    ("🎯", "Prioritas & Rekomendasi", "Subsektor prioritas dan strategi pengembangan SDM", "#/4_Prioritas_Rekomendasi"),
    ("🧪", "Simulator Pelatihan", "Simulasi dampak penambahan materi pelatihan baru", "#/5_Simulator_Pelatihan"),
]

for col, (icon, title, desc, _) in zip(cols, pages):
    with col:
        st.markdown(
            f"""
            <div style="border: 1.5px solid #dde4ed; border-radius: 12px; padding: 18px 14px;
                        text-align: center; height: 160px; background: white;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.06); cursor: default;">
                <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
                <div style="font-size: 0.87rem; font-weight: 700; color: #142c50; margin-bottom: 6px;">{title}</div>
                <div style="font-size: 0.76rem; color: #666; line-height: 1.4;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <hr>
    <p style="text-align:center; font-size:0.78rem; color:#999;">
    Dashboard ini merupakan project mata kuliah Sains Data Consulting (SDC) — 
    Program Studi Teknologi Sains Data, FTMM Universitas Airlangga × Kementerian Pariwisata RI &nbsp;|&nbsp; Kelompok 8 SDC SD-A2
    </p>
    """,
    unsafe_allow_html=True,
)