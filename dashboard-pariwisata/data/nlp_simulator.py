"""
NLP-based Simulator Pelatihan
Menggunakan TF-IDF + Cosine Similarity (scikit-learn) untuk kecocokan semantik
antara judul materi pelatihan baru dengan daftar demand skill.

Catatan: Dapat diupgrade ke sentence-transformers (BERT-based) apabila disk cukup.
"""

import streamlit as st
import numpy as np
from data.coverage_score import COVERAGE_SCORE, GAP_SCORE
from data.demand_skill import SUBSEKTORS, TOP15_SKILLS, DEMAND_MATRIX


# ── Semua demand skill yang dihitung ─────────────────────────────────────────
ALL_DEMAND_SKILLS = list(COVERAGE_SCORE.keys())


# ── Sinonim / Ekspansi kosakata Indonesia → Inggris untuk TF-IDF ─────────────
# Memperkaya query agar TF-IDF lebih akurat menangani padanan kata
EXPANSI = {
    "spa": "spa massage perawatan pijat wellness terapi treatment",
    "higiene": "hygiene sanitasi kebersihan sanitize",
    "sanitasi": "sanitation hygiene kebersihan",
    "k3": "keselamatan kesehatan kerja safety health occupational",
    "keselamatan": "k3 safety occupational health keselamatan kerja",
    "aromaterapi": "aroma therapy aromaterapi essential oil",
    "mixologi": "mixology cocktail bahan alami herbal",
    "anatomi": "anatomy fisiologi physiology tubuh body",
    "fisiologi": "physiology anatomy fisiologi tubuh",
    "event": "acara event mice konferensi exhibition",
    "mice": "meeting incentive convention exhibition acara event",
    "manajemen": "management pengelolaan administrasi",
    "risiko": "risk management manajemen risiko bahaya",
    "kerumunan": "crowd management massa pengendalian kerumunan",
    "hybrid": "hybrid online digital virtual event teknologi",
    "berkelanjutan": "sustainable sustainability lingkungan hijau green",
    "pelatihan": "training pendidikan pembelajaran skill kompetensi",
    "pemasaran": "marketing promosi pemasaran digital branding",
    "penjualan": "sales selling penjualan marketing",
    "dapur": "kitchen masak culinary food cooking",
    "makanan": "food cuisine kuliner masakan cooking",
    "minuman": "beverage drink minuman cocktail",
    "reservasi": "reservation booking reservasi sistem",
    "transportasi": "transportation transport driver logistik",
    "destinasi": "destination wisata tourism pariwisata",
    "lingkungan": "environment alam nature sustainable ecology",
    "keuangan": "finance keuangan accounting akuntansi",
    "inventori": "inventory stok warehouse logistik",
    "bahasa inggris": "english language bahasa communication",
    "front office": "front office receptionist hotel check in",
    "housekeeping": "housekeeping cleaning kebersihan room",
    "ticketing": "ticketing tiket booking reservation",
    "branding": "branding brand identity pemasaran marketing",
    "analitik": "analytics data analisis statistics",
    "komputer": "computer it teknologi software",
    "kepemimpinan": "leadership pemimpin management team",
    "teamwork": "team kerja sama collaboration grup",
    "pertolongan pertama": "first aid p3k emergency keselamatan",
    "pramuwisata": "tour guide pemandu wisata guide",
    "pariwisata": "tourism wisata travel hospitality",
}


@st.cache_resource(show_spinner="⏳ Mempersiapkan model NLP (Natural Language Processing)...")
def _build_tfidf_index():
    """
    Bangun TF-IDF matrix dari semua demand skill.
    Cached satu kali — tidak perlu rebuild setiap simulasi.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    def expand(text: str) -> str:
        t = text.lower()
        extras = [t]
        for kw, expansion in EXPANSI.items():
            if kw in t:
                extras.append(expansion)
        return " ".join(extras)

    # Corpus = semua demand skill (diperluas)
    corpus = [expand(s) for s in ALL_DEMAND_SKILLS]

    vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        sublinear_tf=True,
    )
    tfidf_matrix = vectorizer.fit_transform(corpus)

    return vectorizer, tfidf_matrix, cosine_similarity


def hitung_similarity(new_module_title: str):
    """
    Hitung cosine similarity antara modul baru dengan setiap demand skill.
    Returns: dict { skill: similarity_score (0.0–1.0) }
    """
    vectorizer, tfidf_matrix, cosine_similarity = _build_tfidf_index()

    # Ekspansi query
    query = new_module_title.lower()
    for kw, expansion in EXPANSI.items():
        if kw in query:
            query += " " + expansion

    query_vec = vectorizer.transform([query])
    sims = cosine_similarity(query_vec, tfidf_matrix)[0]

    return {skill: float(sims[i]) for i, skill in enumerate(ALL_DEMAND_SKILLS)}


def simulate_nlp(new_module_title: str, threshold_full=0.35, threshold_partial=0.12):
    """
    Jalankan simulasi penuh:
      1. Hitung similarity TF-IDF modul baru vs setiap demand skill.
      2. Tentukan coverage baru (0 / 0.5 / 1.0) berdasarkan threshold.
      3. Override coverage lama jika coverage baru lebih tinggi (max).
      4. Hitung ulang gap score per subsektor:
         Gap (%) = 100 − (Total_Coverage_Baru / Total_Demand × 100)

    Returns:
        {
            "skills_detail":  { skill: {old, new, final, sim_pct, improved} },
            "improved_skills": [skill, ...],
            "gap_before":     { subsektor: pct },
            "gap_after":      { subsektor: pct },
            "delta":          { subsektor: pct_turun },
        }
    """
    sim_scores = hitung_similarity(new_module_title)

    # Normalisasi: scale agar lebih mudah dibaca (0–100%)
    # TF-IDF cosine jarang mencapai 1.0 → rescale dengan max agar persentase masuk akal
    max_sim = max(sim_scores.values()) if sim_scores else 1.0
    if max_sim == 0:
        max_sim = 1.0

    # --- Per-skill: tentukan coverage baru & bandingkan ---
    skills_detail = {}
    updated_coverage = dict(COVERAGE_SCORE)

    for skill in ALL_DEMAND_SKILLS:
        raw_sim = sim_scores.get(skill, 0.0)
        sim_pct = round((raw_sim / max_sim) * 100, 1)  # rescaled 0–100%

        # Coverage berdasarkan raw cosine similarity
        if raw_sim >= threshold_full:
            new_cov = 1.0
        elif raw_sim >= threshold_partial:
            new_cov = 0.5
        else:
            new_cov = 0.0

        old_cov = COVERAGE_SCORE.get(skill, 0.0)
        final_cov = max(old_cov, new_cov)
        updated_coverage[skill] = final_cov

        skills_detail[skill] = {
            "old": old_cov,
            "new": new_cov,
            "final": final_cov,
            "sim": sim_pct,
            "sim_raw": raw_sim,
            "improved": final_cov > old_cov,
        }

    # --- Hitung ulang gap score per subsektor ---
    gap_before = dict(GAP_SCORE)
    gap_after = {}

    for sub in SUBSEKTORS:
        weights = DEMAND_MATRIX.get(sub, [])
        total_weight = sum(weights)
        if total_weight == 0:
            gap_after[sub] = gap_before.get(sub, 0.0)
            continue

        improvement = 0.0

        for idx, skill in enumerate(TOP15_SKILLS):
            w = weights[idx] if idx < len(weights) else 0
            if w == 0:
                continue
            old_score = COVERAGE_SCORE.get(skill, 0.0)
            new_score = updated_coverage.get(skill, old_score)
            
            if new_score > old_score:
                improvement += (w / total_weight) * (new_score - old_score) * 100

        old_gap = gap_before.get(sub, 0.0)
        gap_after[sub] = round(max(0.0, old_gap - improvement), 2)

    delta = {
        sub: round(gap_before.get(sub, 0.0) - gap_after.get(sub, 0.0), 2)
        for sub in SUBSEKTORS
    }

    improved_skills = [s for s, d in skills_detail.items() if d["improved"]]

    return {
        "skills_detail": skills_detail,
        "improved_skills": improved_skills,
        "gap_before": gap_before,
        "gap_after": gap_after,
        "delta": delta,
    }
