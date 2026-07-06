"""
NLP-based Simulator Pelatihan
Menggunakan Sentence Transformers untuk kecocokan semantik (pemahaman konteks)
antara judul materi pelatihan baru dengan daftar demand skill.
"""

import streamlit as st
from data.gap_score import (
    get_base_gap_scores,
    get_original_similarities_and_coverages,
    get_demand_frequency_per_subsektor,
    get_all_demand_skills,
    get_all_subsektors
)


@st.cache_resource(show_spinner="⏳ Memuat model Deep Learning (Sentence-Transformers)...")
def _load_nlp_model():
    """
    Muat model SentenceTransformer dan hitung embedding awal untuk demand skills.
    Karena menggunakan model deep learning, load awal akan sedikit memakan waktu.
    """
    from sentence_transformers import SentenceTransformer, util
    
    # Model paraphrase multilingual cocok untuk padanan teks campuran Indonesia-Inggris
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    ALL_DEMAND_SKILLS = get_all_demand_skills()
    
    # Pre-compute embeddings for demand skills (hanya dihitung sekali dan di-cache)
    skills_embeddings = model.encode(ALL_DEMAND_SKILLS, convert_to_tensor=True)
    
    return model, skills_embeddings, util.cos_sim


def hitung_similarity(new_module_title: str):
    """
    Hitung cosine similarity antara modul baru dengan setiap demand skill
    secara hybrid: Exact/Keyword Match (berprioritas) + Semantic Embedding (fallback).
    Returns: dict { skill: similarity_score (0.0–1.0) }
    """
    model, skills_embeddings, cos_sim = _load_nlp_model()
    ALL_DEMAND_SKILLS = get_all_demand_skills()
    from data.simulator_data import SINONIM

    # 1. Semantic Embedding Score
    query_embedding = model.encode(new_module_title, convert_to_tensor=True)
    sims = cos_sim(query_embedding, skills_embeddings)[0]
    raw_scores = {skill: max(0.0, float(sims[i])) for i, skill in enumerate(ALL_DEMAND_SKILLS)}
    
    # 2. Hybrid Logic: Prioritaskan keyword / sinonim spesifik dari pakar domain
    lowered_title = new_module_title.lower()
    final_scores = {}
    
    for skill, sem_score in raw_scores.items():
        is_exact = skill.lower() in lowered_title or lowered_title in skill.lower()
        is_synonym = False
        
        # Cek apakah judul mengandung sinonim yang dikhususkan untuk skill ini
        for kw, mapped_skill in SINONIM.items():
            if mapped_skill == skill and kw in lowered_title:
                is_synonym = True
                break
                
        if is_exact or is_synonym:
            # Jika terdeteksi secara eksplisit oleh pakar, berikan nilai kemiripan absolut yang tinggi
            final_scores[skill] = 0.85
        else:
            # Jika tidak terdeteksi eksplisit, gunakan semantic AI dengan threshold ketat
            # Threshold 0.45 menyaring "noise" seperti kata umum 'Operasional', 'Manajemen', 'Pelatihan'
            if sem_score >= 0.45:
                final_scores[skill] = sem_score
            else:
                final_scores[skill] = 0.0
                
    return final_scores


def simulate_nlp(new_module_title: str):
    """
    Jalankan simulasi penuh:
      1. Hitung similarity Sentence-Transformers (semantik) modul baru vs demand skill.
      2. Tambahkan similarity score baru ke original similarity score.
      3. Tentukan coverage baru berdasarkan skor total (> 0.8 -> 1, > 0.4 -> 0.5).
      4. Hitung ulang gap score per subsektor.
    """
    new_sim_scores = hitung_similarity(new_module_title)
    original_data = get_original_similarities_and_coverages()
    demand_freq = get_demand_frequency_per_subsektor()
    gap_before = get_base_gap_scores()
    
    skills_detail = {}
    updated_coverage = {}
    
    # --- Hitung ulang coverage score per demand skill ---
    for skill, data in original_data.items():
        old_sim = data['sim']
        old_cov = data['cov']
        new_sim = new_sim_scores.get(skill, 0.0)
        
        # Terapkan threshold untuk mengeliminasi noise dari model semantic
        # (Nilai < 0.35 umumnya dianggap kurang relevan secara konteks)
        if new_sim < 0.35:
            new_sim = 0.0
        
        # Tambahkan score lama dan baru
        total_sim = old_sim + new_sim
        
        # Tentukan coverage berdasarkan total_sim
        if total_sim > 0.8:
            new_cov = 1.0
        elif total_sim > 0.4:
            new_cov = 0.5
        else:
            new_cov = 0.0
            
        final_cov = max(old_cov, new_cov)
        updated_coverage[skill] = final_cov
        
        skills_detail[skill] = {
            "old": old_cov,
            "new": new_cov,
            "final": final_cov,
            "sim": total_sim * 100, # dalam persen untuk UI
            "sim_raw": total_sim,
            "improved": final_cov > old_cov,
        }

    # --- Hitung ulang gap score per subsektor ---
    gap_after = {}
    for sub, freq_dict in demand_freq.items():
        total_demand = sum(freq_dict.values())
        
        if total_demand == 0:
            gap_after[sub] = gap_before.get(sub, 0.0)
            continue
            
        total_cov = 0.0
        for skill, freq in freq_dict.items():
            skill_cov = updated_coverage.get(skill, 0.0)
            total_cov += (skill_cov * freq)
            
        pct_coverage = (total_cov / total_demand) * 100
        gap_after[sub] = 100.0 - pct_coverage

    delta = {
        sub: round(gap_before.get(sub, 0.0) - gap_after.get(sub, 0.0), 2)
        for sub in get_all_subsektors()
    }

    improved_skills = [s for s, d in skills_detail.items() if d["improved"]]

    return {
        "skills_detail": skills_detail,
        "improved_skills": improved_skills,
        "gap_before": gap_before,
        "gap_after": gap_after,
        "delta": delta,
    }
