import streamlit as st
from utils import inject_css, render_sidebar_header, page_header, section_title

st.set_page_config(
    page_title="Prioritas & Rekomendasi",
    page_icon="🎯",
    layout="wide",
)

inject_css()
render_sidebar_header()

page_header(
    title="Subsektor Prioritas & Rekomendasi Pelatihan", 
    subtitle="Subsektor prioritas dan strategi pengembangan SDM", 
    icon="🎯"
)

st.markdown("""
Berdasarkan hasil analisis kesenjangan kompetensi yang telah dilakukan, sistem mengidentifikasi **2 subsektor prioritas utama** yang memerlukan intervensi dan strategi pengembangan Sumber Daya Manusia (SDM) yang tepat sasaran.
""")

section_title("Subsektor Prioritas dan Rekomendasi Penambahan Materi Pelatihan", "🚨")

# Card for SPA (Sanus Per Aquam)
html_spa = """
<div class="rekom-card">
<div class="rekom-header" style="margin-bottom: 8px;">
<div class="rekom-gap">32,38%</div>
<div class="rekom-title">Kesenjangan Kompetensi</div>
</div>
<h3 style="margin-top: 0; margin-bottom: 16px; color: #142c50; font-size: 1.4rem;">1. SPA (Sanus Per Aquam)</h3>
<p style="margin-top: 0; margin-bottom: 16px; color: #475569; font-size: 1rem;">Direkomendasikan untuk menambahkan materi pelatihan berikut:</p>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px;">
<div style="background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px; border-left: 4px solid #3b82f6;">
<h4 style="margin: 0 0 8px 0; color: #142c50; font-size: 1.1rem;">⛑️ K3</h4>
<p style="margin: 0 0 8px 0; font-size: 0.95rem; color: #475569;"><b>Kebijakan:</b> Menyusun pelatihan K3 khusus industri SPA</p>
<div style="font-size: 0.95rem; color: #475569;"><b>Materi utama:</b>
<ul style="margin-top: 4px; margin-bottom: 0; padding-left: 18px;">
<li>Higiene & sanitasi</li>
<li>Penggunaan alat & produk</li>
<li>Pencegahan infeksi</li>
<li>Limbah</li>
<li>P3K</li>
</ul>
</div>
</div>

<div style="background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px; border-left: 4px solid #10b981;">
<h4 style="margin: 0 0 8px 0; color: #142c50; font-size: 1.1rem;">🛡️ Manajemen Risiko</h4>
<p style="margin: 0 0 8px 0; font-size: 0.95rem; color: #475569;"><b>Kebijakan:</b> Mengembangkan pelatihan manajemen risiko operasional SPA</p>
<div style="font-size: 0.95rem; color: #475569;"><b>Materi utama:</b>
<ul style="margin-top: 4px; margin-bottom: 0; padding-left: 18px;">
<li>Identifikasi risiko</li>
<li>Penanganan keluhan</li>
<li>Risiko alat & produk</li>
<li>SOP pelayanan</li>
</ul>
</div>
</div>

<div style="background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px; border-left: 4px solid #f59e0b;">
<h4 style="margin: 0 0 8px 0; color: #142c50; font-size: 1.1rem;">💆‍♀️ Perawatan SPA</h4>
<p style="margin: 0 0 8px 0; font-size: 0.95rem; color: #475569;"><b>Kebijakan:</b> Mengembangkan pelatihan teknis perawatan SPA</p>
<div style="font-size: 0.95rem; color: #475569;"><b>Materi utama:</b>
<ul style="margin-top: 4px; margin-bottom: 0; padding-left: 18px;">
<li>Body treatment</li>
<li>Facial treatment</li>
<li>Massage</li>
<li>Aromatherapy</li>
<li>Consultation & assessment</li>
</ul>
</div>
</div>
</div>
</div>
"""
st.markdown(html_spa, unsafe_allow_html=True)

# Card for MICE
html_mice = """
<div class="rekom-card" style="margin-bottom: 0;">
<div class="rekom-header" style="margin-bottom: 8px;">
<div class="rekom-gap" style="color: #d97706;">15,73%</div>
<div class="rekom-title">Kesenjangan Kompetensi</div>
</div>
<h3 style="margin-top: 0; margin-bottom: 16px; color: #142c50; font-size: 1.4rem;">2. Penyelenggaraan Acara (MICE / Meeting, Incentive, Convention, and Exhibition)</h3>
<p style="margin-top: 0; margin-bottom: 16px; color: #475569; font-size: 1rem;">Direkomendasikan untuk menambahkan materi pelatihan berikut:</p>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px;">
<div style="background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px; border-left: 4px solid #3b82f6;">
<h4 style="margin: 0 0 8px 0; color: #142c50; font-size: 1.1rem;">⛑️ K3</h4>
<p style="margin: 0 0 8px 0; font-size: 0.95rem; color: #475569;"><b>Kebijakan:</b> Menyusun pelatihan K3 yang sesuai karakteristik subsektor</p>
<div style="font-size: 0.95rem; color: #475569;"><b>Materi utama:</b>
<ul style="margin-top: 4px; margin-bottom: 0; padding-left: 18px;">
<li>Crowd control</li>
<li>Jalur evakuasi</li>
<li>Audit struktur panggung & booth</li>
</ul>
</div>
</div>

<div style="background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px; border-left: 4px solid #10b981;">
<h4 style="margin: 0 0 8px 0; color: #142c50; font-size: 1.1rem;">📅 Manajemen Event</h4>
<p style="margin: 0 0 8px 0; font-size: 0.95rem; color: #475569;"><b>Kebijakan:</b> Mengembangkan pelatihan operasional penyelenggaraan event</p>
<div style="font-size: 0.95rem; color: #475569;"><b>Materi utama:</b>
<ul style="margin-top: 4px; margin-bottom: 0; padding-left: 18px;">
<li>Master schedule</li>
<li>Floor plan</li>
<li>Koordinasi vendor</li>
</ul>
</div>
</div>

<div style="background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px; border-left: 4px solid #f59e0b;">
<h4 style="margin: 0 0 8px 0; color: #142c50; font-size: 1.1rem;">🛡️ Manajemen Risiko</h4>
<p style="margin: 0 0 8px 0; font-size: 0.95rem; color: #475569;"><b>Kebijakan:</b> Mengembangkan pelatihan mitigasi risiko penyelenggaraan</p>
<div style="font-size: 0.95rem; color: #475569;"><b>Materi utama:</b>
<ul style="margin-top: 4px; margin-bottom: 0; padding-left: 18px;">
<li>Plan B</li>
<li>Gangguan registrasi</li>
<li>Listrik</li>
<li>Cuaca</li>
<li>Pembatalan acara</li>
</ul>
</div>
</div>

<div style="background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px; border-left: 4px solid #8b5cf6;">
<h4 style="margin: 0 0 8px 0; color: #142c50; font-size: 1.1rem;">🎫 Ticketing</h4>
<p style="margin: 0 0 8px 0; font-size: 0.95rem; color: #475569;"><b>Kebijakan:</b> Meningkatkan kompetensi pengelolaan sistem tiket digital</p>
<div style="font-size: 0.95rem; color: #475569;"><b>Materi utama:</b>
<ul style="margin-top: 4px; margin-bottom: 0; padding-left: 18px;">
<li>Self-registration</li>
<li>Payment gateway</li>
<li>Analisis data tiket</li>
</ul>
</div>
</div>

<div style="background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px; border-left: 4px solid #ef4444;">
<h4 style="margin: 0 0 8px 0; color: #142c50; font-size: 1.1rem;">📈 Penjualan</h4>
<p style="margin: 0 0 8px 0; font-size: 0.95rem; color: #475569;"><b>Kebijakan:</b> Mengembangkan kompetensi pemasaran dan bidding</p>
<div style="font-size: 0.95rem; color: #475569;"><b>Materi utama:</b>
<ul style="margin-top: 4px; margin-bottom: 0; padding-left: 18px;">
<li>Proposal sponsor</li>
<li>Penjualan booth</li>
<li>Bidding event internasional</li>
</ul>
</div>
</div>
</div>
</div>
"""
st.markdown(html_mice, unsafe_allow_html=True)
