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

from utils import inject_css, render_sidebar_header, get_base64_image

inject_css()
render_sidebar_header()

# ── Landing Page ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #0e1f38 0%, #142c50 60%, #1e4a85 100%);
                border-radius: 16px; padding: 52px 40px; margin-bottom: 24px; text-align: center;
                box-shadow: 0 8px 32px rgba(20,44,80,0.18); border-bottom: 3px solid #ebc26c;">
        <div style="font-size: 3rem; margin-bottom: 14px; line-height: 1;">🏝️</div>
        <h1 style="color: white; font-size: 2.1rem; margin: 0 0 10px; font-weight: 800; letter-spacing: -0.5px; font-family: 'DM Sans', sans-serif;">
            Dashboard Analisis Kesenjangan Kompetensi<br>Tenaga Kerja Pariwisata Indonesia
        </h1>
        <p style="color: #b0c4de; font-size: 1rem; margin: 0 0 28px; font-weight: 400;">
            Simulator Pelatihan &amp; Pemetaan Kebutuhan SDM Pariwisata 38 Provinsi
        </p>
        <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
            <span style="background: rgba(235,194,108,0.15); color: #ebc26c; border: 1px solid rgba(235,194,108,0.3);
                         padding: 7px 18px; border-radius: 30px; font-size: 0.83rem; font-weight: 600;">
                📊 12 Subsektor
            </span>
            <span style="background: rgba(235,194,108,0.15); color: #ebc26c; border: 1px solid rgba(235,194,108,0.3);
                         padding: 7px 18px; border-radius: 30px; font-size: 0.83rem; font-weight: 600;">
                🗺️ 38 Provinsi
            </span>
            <span style="background: rgba(235,194,108,0.15); color: #ebc26c; border: 1px solid rgba(235,194,108,0.3);
                         padding: 7px 18px; border-radius: 30px; font-size: 0.83rem; font-weight: 600;">
                📚 36 Demand Skill
            </span>
            <span style="background: rgba(235,194,108,0.15); color: #ebc26c; border: 1px solid rgba(235,194,108,0.3);
                         padding: 7px 18px; border-radius: 30px; font-size: 0.83rem; font-weight: 600;">
                🔬 Data Kemenpar × Kemnaker
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Load images as base64
img_bromo = get_base64_image("assets/bromo.png")
img_wakatobi = get_base64_image("assets/wakatobi.jpg")
img_mandalika = get_base64_image("assets/mandalika.png")
img_borobudur = get_base64_image("assets/candi-borobudur.jpg")
img_labuan = get_base64_image("assets/labuan-bajo.jpg")

st.markdown(
    f"""
    <div style="display: flex; gap: 12px; margin-bottom: 32px; justify-content: space-between;">
        <div style="flex: 1; aspect-ratio: 4/3; border-radius: 12px; background: url('data:image/jpeg;base64,{img_borobudur}') center/cover; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></div>
        <div style="flex: 1; aspect-ratio: 4/3; border-radius: 12px; background: url('data:image/png;base64,{img_mandalika}') center/cover; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></div>
        <div style="flex: 1; aspect-ratio: 4/3; border-radius: 12px; background: url('data:image/jpeg;base64,{img_labuan}') center/cover; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></div>
        <div style="flex: 1; aspect-ratio: 4/3; border-radius: 12px; background: url('data:image/png;base64,{img_bromo}') center/cover; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></div>
        <div style="flex: 1; aspect-ratio: 4/3; border-radius: 12px; background: url('data:image/jpeg;base64,{img_wakatobi}') center/cover; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div style="margin-bottom: 24px; margin-top: 12px;">
    <div style="font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#ebc26c;margin-bottom:8px;">LATAR BELAKANG</div>
    <h2 style="color: #111827; font-size: 2.2rem; font-weight: 800; margin: 0 0 12px 0; font-family: 'DM Sans', sans-serif;">Mengapa dashboard ini penting?</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); margin-bottom: 36px; display: flex; align-items: center; gap: 24px;">
        <div style="font-size: 3rem;">💡</div>
        <p style="color: #6b7280; font-size: 1.05rem; line-height: 1.6; margin: 0;">
            Pesatnya perkembangan sektor pariwisata menuntut kesiapan SDM yang sangat adaptif. Adanya indikasi <b><i>skills mismatch</i></b> antara kurikulum pelatihan saat ini dengan kebutuhan nyata di industri membuat analisis berbasis data menjadi sangat krusial untuk mencegah pengangguran struktural.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 24px; margin-top: 24px;">
    <div style="font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#ebc26c;margin-bottom:8px;">TUJUAN DASHBOARD</div>
    <h2 style="color: #111827; font-size: 2.2rem; font-weight: 800; margin: 0 0 12px 0; font-family: 'DM Sans', sans-serif;">Apa yang ingin dicapai?</h2>
</div>
""", unsafe_allow_html=True)

tujuan_data = [
    ("📏", "Mengukur Kesenjangan", "Menghitung nilai gap kompetensi secara presisi antara kemampuan tenaga kerja pariwisata dengan standar kebutuhan industri saat ini."),
    ("📊", "Memvisualisasikan Data", "Menyajikan sebaran tenaga kerja, proyeksi kebutuhan, dan status pemetaan kompetensi secara interaktif di 38 provinsi."),
    ("🧪", "Mensimulasikan Kebijakan", "Menyediakan simulator berbasis AI untuk memprediksi dampak penambahan kurikulum pelatihan baru terhadap penurunan skor kesenjangan.")
]

html_tujuan = '<div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; margin-bottom: 12px;">'
for icon, title, desc in tujuan_data:
    html_tujuan += f"""<div style="flex: 1; min-width: 250px; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.02); display: flex; flex-direction: column;">
<div style="font-size: 2.2rem; margin-bottom: 16px;">{icon}</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #111827; margin-bottom: 12px; font-family: 'DM Sans', sans-serif; line-height: 1.4;">{title}</div>
<div style="font-size: 0.9rem; color: #6b7280; line-height: 1.6; flex-grow: 1;">{desc}</div>
</div>"""
html_tujuan += '</div>'
st.markdown(html_tujuan, unsafe_allow_html=True)

# ── Fitur Utama ──────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 24px; margin-top: 24px;">
    <div style="font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#ebc26c;margin-bottom:8px;">FITUR UTAMA</div>
    <h2 style="color: #111827; font-size: 2.2rem; font-weight: 800; margin: 0 0 12px 0; font-family: 'DM Sans', sans-serif;">Eksplorasi Dashboard</h2>
</div>
""", unsafe_allow_html=True)

pages = [
    ("🧑\u200d💼", "Profil Tenaga Kerja", "Sebaran, proyeksi, dan kebutuhan pembinaan SDM per provinsi"),
    ("🗂️", "Pemetaan Kompetensi", "Demand skill per subsektor & coverage pelatihan"),
    ("📉", "Analisis Kesenjangan", "Gap score per subsektor dan coverage tiap skill"),
    ("🎯", "Prioritas & Rekomendasi", "Subsektor prioritas dan strategi pengembangan SDM"),
    ("🧪", "Simulator Pelatihan", "Simulasi dampak penambahan materi pelatihan baru"),
]

html_fitur = '<div style="display: flex; gap: 20px; align-items: stretch; flex-wrap: wrap; margin-bottom: 12px;">'
for icon, title, desc in pages:
    html_fitur += f"""<div style="flex: 1; min-width: 180px; border: 1px solid #dde4ed; border-radius: 12px; padding: 20px 16px; text-align: center; background: white; box-shadow: 0 1px 4px rgba(20,44,80,0.04); display: flex; flex-direction: column;">
<div style="font-size: 1.9rem; margin-bottom: 10px;">{icon}</div>
<div style="font-size: 0.88rem; font-weight: 700; color: #142c50; margin-bottom: 6px;">{title}</div>
<div style="font-size: 0.77rem; color: #64748b; line-height: 1.45; flex-grow: 1;">{desc}</div>
</div>"""
html_fitur += '</div>'
st.markdown(html_fitur, unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 24px; margin-top: 24px;">
    <div style="font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#ebc26c;margin-bottom:8px;">SUMBER DATA & METODOLOGI</div>
    <h2 style="color: #111827; font-size: 2.2rem; font-weight: 800; margin: 0 0 12px 0; font-family: 'DM Sans', sans-serif;">Fondasi Data dan Teknologi Analisis</h2>
</div>
""", unsafe_allow_html=True)

metode_data = [
    ("📚", "Data Supply (Ketersediaan)", "Memanfaatkan referensi dari kurikulum dan modul pelatihan standar yang dikeluarkan oleh Kementerian Ketenagakerjaan (Kemnaker)."),
    ("🎯", "Data Demand (Kebutuhan)", "Diambil dan diekstraksi dari Standar Kompetensi Kerja Nasional Indonesia (SKKNI) bidang pariwisata yang telah divalidasi oleh industri."),
    ("🤖", "Metodologi NLP & AI", "Menggunakan analisis komparatif kuantitatif dan algoritma <i>Natural Language Processing</i> (NLP) berbasis Cosine Similarity untuk mengukur tingkat kecocokan materi.")
]

html_metode = '<div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; margin-bottom: 12px;">'
for icon, title, desc in metode_data:
    html_metode += f"""<div style="flex: 1; min-width: 250px; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.02); display: flex; flex-direction: column;">
<div style="font-size: 2.2rem; margin-bottom: 16px;">{icon}</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #111827; margin-bottom: 12px; font-family: 'DM Sans', sans-serif; line-height: 1.4;">{title}</div>
<div style="font-size: 0.9rem; color: #6b7280; line-height: 1.6; flex-grow: 1;">{desc}</div>
</div>"""
html_metode += '</div>'
st.markdown(html_metode, unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 24px; margin-top: 24px;">
    <div style="font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#ebc26c;margin-bottom:8px;">PENGGUNA SASARAN</div>
    <h2 style="color: #111827; font-size: 2.2rem; font-weight: 800; margin: 0 0 12px 0; font-family: 'DM Sans', sans-serif;">Dashboard ini untuk siapa?</h2>
    <p style="color: #6b7280; font-size: 1.05rem; margin: 0; line-height: 1.6; max-width: 800px;">
        Dirancang untuk memenuhi kebutuhan berbagai pemangku kepentingan dalam ekosistem pengembangan dan pembinaan SDM sektor pariwisata di Indonesia.
    </p>
</div>
""", unsafe_allow_html=True)

sasaran_data = [
    ("🏛️", "Kementerian Pusat", "Pemangku kebijakan yang merumuskan standar kompetensi, program pelatihan, dan sertifikasi profesi pariwisata yang tepat sasaran."),
    ("🗺️", "Pemerintah Daerah", "Perencana pembangunan daerah yang membutuhkan data untuk memetakan kebutuhan spesifik dan intervensi pembinaan SDM di masing-masing provinsi."),
    ("🏫", "Lembaga Pelatihan", "Institusi pendidikan dan vokasi yang perlu memperbarui kurikulum agar senantiasa selaras dengan kebutuhan kompetensi nyata di industri saat ini."),
    ("🔬", "Peneliti & Akademisi", "Peneliti yang mengkaji kesenjangan kompetensi, efektivitas kebijakan, dan penerapan analisis data untuk sektor tenaga kerja pariwisata.")
]

html_sasaran = '<div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; margin-bottom: 36px;">'
for icon, title, desc in sasaran_data:
    html_sasaran += f"""<div style="flex: 1; min-width: 200px; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.02); display: flex; flex-direction: column;">
<div style="font-size: 2.2rem; margin-bottom: 16px;">{icon}</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #111827; margin-bottom: 12px; font-family: 'DM Sans', sans-serif; line-height: 1.4;">{title}</div>
<div style="font-size: 0.9rem; color: #6b7280; line-height: 1.6; flex-grow: 1;">{desc}</div>
</div>"""
html_sasaran += '</div>'
st.markdown(html_sasaran, unsafe_allow_html=True)

st.markdown(
    """
    <hr style="margin: 24px 0;">
    <p style="text-align:center; font-size:0.77rem; color:#94a3b8; margin: 0;">
    Dashboard Analisis Kesenjangan Kompetensi Tenaga Kerja Pariwisata Indonesia &nbsp;|&nbsp;
    Program Studi Teknologi Sains Data, FTMM Universitas Airlangga × Kementerian Pariwisata RI &nbsp;|&nbsp; Kelompok 8 SDC SD-A2
    </p>
    """,
    unsafe_allow_html=True,
)
