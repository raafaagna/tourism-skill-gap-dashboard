"""
Halaman 5: Simulator Pelatihan (NLP-based)
Menggunakan cosine similarity dari sentence-transformers untuk mensimulasikan
dampak penambahan materi pelatihan baru terhadap gap score setiap subsektor.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import (
    inject_css, render_sidebar_header, page_header,
    section_title, insight_box, base_layout,
    PRIMARY, ACCENT, TEXT, SUCCESS, DANGER, WARNING,
)
from data.demand_skill import SUBSEKTORS

st.set_page_config(
    page_title="Simulator Pelatihan | Dashboard Pariwisata",
    page_icon="🧪",
    layout="wide",
)

inject_css()
render_sidebar_header()

page_header(
    title="Simulator Pelatihan",
    subtitle="Simulasi dampak penambahan materi pelatihan baru terhadap kesenjangan kompetensi (gap score)",
    icon="🧪",
)

st.markdown(
    "Masukkan judul materi pelatihan baru. Sistem akan menggunakan **kecerdasan buatan (NLP)** "
    "untuk menghitung kesamaan semantik dengan setiap *demand skill*, lalu menghitung ulang "
    "gap score secara real-time."
)

# ── Saran Materi ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="background:#f8fafc; border:1px solid #e1e8f0; border-left:4px solid #ebc26c;
                padding:16px; border-radius:8px; margin: 16px 0 20px 0;">
        <h4 style="margin-top:0; color:#142c50; font-size:1.0rem;">💡 Saran Penambahan Materi Pelatihan</h4>
        <p style="font-size:0.88rem; color:#475569; margin-bottom:10px;">
            Berdasarkan prioritas analisis kesenjangan, cobalah simulasikan judul-judul berikut:
        </p>
        <div style="display:flex; gap:24px; flex-wrap:wrap;">
            <div style="flex:1; min-width:240px;">
                <strong style="color:#142c50; font-size:0.88rem;">A) Untuk Subsektor SPA:</strong>
                <ul style="font-size:0.84rem; color:#475569; padding-left:16px; margin-top:4px; line-height:1.6;">
                    <li>Anatomi Dasar dan Fisiologi Terapan</li>
                    <li>Pelatihan Higiene, Sanitasi, dan K3 Khusus SPA</li>
                    <li>Mixologi Bahan Alami dan Aromaterapi</li>
                </ul>
            </div>
            <div style="flex:1; min-width:240px;">
                <strong style="color:#142c50; font-size:0.88rem;">B) Untuk Subsektor MICE:</strong>
                <ul style="font-size:0.84rem; color:#475569; padding-left:16px; margin-top:4px; line-height:1.6;">
                    <li>Manajemen Event Hybrid &amp; Teknologi Event</li>
                    <li>Manajemen Acara Berkelanjutan</li>
                    <li>Manajemen Risiko Masif dan Pengendalian Kerumunan</li>
                </ul>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Input ─────────────────────────────────────────────────────────────────────
module_input = st.text_input(
    "📚 Judul Materi Pelatihan Baru",
    placeholder="Contoh: Pelatihan SPA Dasar & Higiene",
    help="Masukkan judul modul pelatihan. Sistem AI akan menghitung kecocokan semantiknya.",
)

col_btn, _ = st.columns([1.5, 4.5])
with col_btn:
    run = st.button("🚀 Jalankan Simulasi", type="primary", width='stretch')

# ── Hasil ─────────────────────────────────────────────────────────────────────
if run:
    title = module_input.strip()
    if not title:
        st.warning("⚠️ Silakan masukkan judul materi pelatihan terlebih dahulu.")
        st.stop()

    with st.spinner("🤖 Model NLP sedang menganalisis kesamaan semantik..."):
        try:
            from data.nlp_simulator import simulate_nlp
            result = simulate_nlp(title)
        except ImportError as e:
            st.error(f"Paket NLP belum terinstall: {e}. Jalankan: `pip install sentence-transformers torch`")
            st.stop()

    skills_detail  = result["skills_detail"]
    improved_skills = result["improved_skills"]
    gap_before     = result["gap_before"]
    gap_after      = result["gap_after"]
    delta          = result["delta"]

    st.success(f"✅ Simulasi selesai untuk materi: **\"{title}\"**")

    # ── 1. Skill yang Terdeteksi ──────────────────────────────────────────────
    section_title("🔍 Demand Skill yang Paling Mirip dengan Materi Ini", icon="")

    # Ambil top-10 skill berdasarkan similarity score tertinggi
    top_skills = sorted(skills_detail.items(), key=lambda x: x[1]["sim"], reverse=True)[:10]

    rows = []
    for skill, d in top_skills:
        sim_pct = d["sim"]
        if sim_pct >= 80:
            level = "🟢 Sangat Mirip (≥80%)"
        elif sim_pct >= 40:
            level = "🟡 Cukup Mirip (40–80%)"
        else:
            level = "⚪ Rendah (<40%)"
        old_label = {1.0: "✅ Fully", 0.5: "⚠️ Partial", 0.0: "❌ Not Covered"}.get(d["old"], "-")
        new_label = {1.0: "✅ Fully", 0.5: "⚠️ Partial", 0.0: "❌ Not Covered"}.get(d["final"], "-")
        rows.append({
            "Demand Skill": skill,
            "Similarity (%)": f"{sim_pct:.1f}%",
            "Level Kecocokan": level,
            "Coverage Lama": old_label,
            "Coverage Baru": new_label,
            "Meningkat?": "✔️ Ya" if d["improved"] else "—",
        })

    df_skills = pd.DataFrame(rows)
    st.dataframe(df_skills, width='stretch', hide_index=True)

    if improved_skills:
        st.markdown(
            f"<div style='font-size:0.88rem; color:#475569; margin-top:6px;'>"
            f"💡 <b>{len(improved_skills)} demand skill</b> mengalami peningkatan coverage "
            f"berkat materi ini.</div>",
            unsafe_allow_html=True,
        )
    else:
        insight_box(
            "Model tidak menemukan demand skill yang memiliki kemiripan semantik cukup tinggi "
            "untuk meningkatkan coverage score. Gap score tidak berubah."
        )

    st.markdown("---")

    # ── 2. Dampak Gap Score Semua Subsektor ──────────────────────────────────
    section_title("📉 Dampak pada Gap Score Seluruh Subsektor", icon="")

    subs_sorted = sorted(SUBSEKTORS, key=lambda s: gap_before.get(s, 0), reverse=True)
    before_vals = [round(gap_before.get(s, 0), 2) for s in subs_sorted]
    after_vals  = [round(gap_after.get(s, 0), 2)  for s in subs_sorted]
    delta_vals  = [round(delta.get(s, 0), 2)       for s in subs_sorted]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Gap Sebelum (%)",
        x=subs_sorted,
        y=before_vals,
        marker_color=DANGER,
        text=[f"{v}%" for v in before_vals],
        textposition="outside",
        textfont=dict(size=9, family="DM Sans"),
    ))
    fig.add_trace(go.Bar(
        name="Gap Sesudah (%)",
        x=subs_sorted,
        y=after_vals,
        marker_color="#2ecc71",
        text=[f"{v}%" for v in after_vals],
        textposition="outside",
        textfont=dict(size=9, family="DM Sans"),
    ))

    layout = base_layout("", height=480)
    layout.update(dict(
        barmode="group",
        yaxis_title="Gap Score (%)",
        xaxis=dict(tickangle=-30, tickfont=dict(size=10)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=140),
    ))
    fig.update_layout(**layout)
    st.plotly_chart(fig, width='stretch')

    # ── 3. Tabel Ringkasan Delta ──────────────────────────────────────────────
    section_title("📋 Ringkasan Perubahan Gap Score", icon="")

    rows_gap = []
    for sub in subs_sorted:
        b = round(gap_before.get(sub, 0), 2)
        a = round(gap_after.get(sub, 0), 2)
        d = round(b - a, 2)
        rows_gap.append({
            "Subsektor": sub,
            "Gap Sebelum (%)": f"{b:.2f}%",
            "Gap Sesudah (%)": f"{a:.2f}%",
            "Perubahan (%)": f"−{d:.2f}%" if d > 0 else ("0.00%" if d == 0 else f"+{abs(d):.2f}%"),
            "Dampak": "✅ Berkurang" if d > 0 else ("⬜ Tidak Berubah" if d == 0 else "⚠️ Naik"),
        })

    def color_row(row):
        if "Berkurang" in row["Dampak"]:
            return ["background-color:#e8f8f0"] * len(row)
        elif "Tidak Berubah" in row["Dampak"]:
            return [""] * len(row)
        return ["background-color:#fdf0ee"] * len(row)

    df_gap_tbl = pd.DataFrame(rows_gap)
    st.dataframe(
        df_gap_tbl.style.apply(color_row, axis=1),
        width='stretch',
        hide_index=True,
    )

    # ── 4. Insight Teks ──────────────────────────────────────────────────────
    impacted = [(s, delta.get(s, 0)) for s in SUBSEKTORS if delta.get(s, 0) > 0]
    impacted.sort(key=lambda x: x[1], reverse=True)

    if impacted:
        st.markdown("---")
        section_title("💡 Kesimpulan Simulasi", icon="")
        top_sub, top_d = impacted[0]
        insight_box(
            f"Penambahan materi pelatihan <b>\"{title}\"</b> berpotensi memberikan dampak terbesar "
            f"pada subsektor <b>{top_sub}</b>, dengan penurunan gap score sebesar "
            f"<b style='color:{SUCCESS};'>−{top_d:.2f}%</b> "
            f"(dari {gap_before.get(top_sub, 0):.2f}% menjadi {gap_after.get(top_sub, 0):.2f}%). "
            f"Secara keseluruhan, {len(impacted)} dari {len(SUBSEKTORS)} subsektor mengalami perbaikan."
        )
