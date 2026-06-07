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
    title="Prioritas & Rekomendasi", 
    subtitle="Subsektor prioritas dan strategi pengembangan SDM", 
    icon="🎯"
)

st.markdown("""
Berdasarkan hasil analisis kesenjangan kompetensi yang telah dilakukan, sistem mengidentifikasi **2 subsektor prioritas utama** yang memerlukan intervensi dan strategi pengembangan Sumber Daya Manusia (SDM) yang tepat sasaran.
""")

section_title("Subsektor Prioritas", "🚨")

# Card for SPA
html_spa = """
<div class="rekom-card">
<div class="rekom-header" style="margin-bottom: 8px;">
<div class="rekom-gap">32,38%</div>
<div class="rekom-title">Kesenjangan Kompetensi</div>
</div>
<h3 style="margin-top: 0; margin-bottom: 16px; color: #142c50; font-size: 1.4rem;">1. SPA</h3>

<div style="display: flex; gap: 16px; flex-wrap: wrap;">
<div style="flex: 1; min-width: 300px; background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px;">
<div style="margin-bottom: 10px;">
<span style="background: #fdf0ee; color: #c0392b; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; border: 1px solid rgba(192,57,43,0.2);">
🔍 Temuan Sistem
</span>
</div>
<ul style="color: #475569; font-size: 0.95rem; line-height: 1.5; margin: 0; padding-left: 18px;">
<li style="margin-bottom: 4px;">Terdeteksi adanya <b>"kekosongan materi"</b> pada pasokan pelatihan.</li>
<li style="margin-bottom: 0;">Beberapa <b>keterampilan teknis esensial</b> industri SPA belum memiliki modul spesifik.</li>
</ul>
</div>
<div style="flex: 1; min-width: 300px; background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px;">
<div style="margin-bottom: 10px;">
<span style="background: #e8f8f0; color: #1a7a47; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; border: 1px solid rgba(26,122,71,0.2);">
💡 Saran Tindakan
</span>
</div>
<ul style="color: #475569; font-size: 0.95rem; line-height: 1.5; margin: 0; padding-left: 18px;">
<li style="margin-bottom: 4px;">Lakukan <b>kolaborasi segera</b> dengan praktisi industri SPA.</li>
<li style="margin-bottom: 0;">Susun <b>modul kurikulum baru</b> khusus untuk keterampilan yang belum ter-cover.</li>
</ul>
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

<div style="display: flex; gap: 16px; flex-wrap: wrap;">
<div style="flex: 1; min-width: 300px; background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px;">
<div style="margin-bottom: 10px;">
<span style="background: #fdf0ee; color: #c0392b; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; border: 1px solid rgba(192,57,43,0.2);">
🔍 Temuan Sistem
</span>
</div>
<ul style="color: #475569; font-size: 0.95rem; line-height: 1.5; margin: 0; padding-left: 18px;">
<li style="margin-bottom: 4px;">Modul pelatihan MICE (Meeting, Incentive, Convention, and Exhibition) <b>sudah tersedia</b>, namun belum optimal.</li>
<li style="margin-bottom: 0;">Materi baru <b>"menyentuh sebagian" (parsial)</b> dari tuntutan tren industri saat ini.</li>
</ul>
</div>
<div style="flex: 1; min-width: 300px; background: #f8fafc; border: 1px solid #e1e8f0; padding: 16px; border-radius: 10px;">
<div style="margin-bottom: 10px;">
<span style="background: #e8f8f0; color: #1a7a47; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; border: 1px solid rgba(26,122,71,0.2);">
💡 Saran Tindakan
</span>
</div>
<ul style="color: #475569; font-size: 0.95rem; line-height: 1.5; margin: 0; padding-left: 18px;">
<li style="margin-bottom: 4px;"><b>Tidak perlu merombak</b> kurikulum secara total.</li>
<li style="margin-bottom: 0;">Cukup tambahkan <b>pelatihan singkat (micro-learning)</b> tentang pembaruan tren event modern.</li>
</ul>
</div>
</div>
</div>
"""
st.markdown(html_mice, unsafe_allow_html=True)
