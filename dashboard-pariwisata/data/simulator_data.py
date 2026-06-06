"""
Data Simulator Pelatihan
Memetakan materi pelatihan terhadap demand skill & subsektor yang terpengaruh
"""

import pandas as pd
from data.coverage_score import COVERAGE_SCORE, GAP_SCORE

# Pemetaan skill ke subsektor yang menggunakannya (bobot > 0)
SKILL_TO_SUBSEKTOR = {
    "Pemanduan Wisata": ["Jasa Pramuwisata", "Daya Tarik Wisata", "Jasa Perjalanan Wisata"],
    "Pariwisata Berkelanjutan": ["Daya Tarik Wisata", "Kawasan Pariwisata", "Jasa Pramuwisata"],
    "Pengelolaan Lingkungan": ["Kawasan Pariwisata", "Daya Tarik Wisata"],
    "Manajemen Risiko": ["Jasa Perjalanan Wisata", "Kawasan Pariwisata", "Penyediaan Akomodasi"],
    "Pelayanan Pelanggan": [
        "Daya Tarik Wisata", "Jasa Makanan dan Minuman", "Penyediaan Akomodasi",
        "Jasa Transportasi Wisata", "SPA",
    ],
    "Komunikasi": [
        "Jasa Informasi Pariwisata", "Jasa Konsultan Pariwisata", "Jasa Pramuwisata",
    ],
    "Sistem Reservasi": ["Penyediaan Akomodasi", "Jasa Perjalanan Wisata"],
    "Administrasi dan Pelaporan": [
        "Jasa Konsultan Pariwisata", "Jasa Informasi Pariwisata", "Penyelenggaraan Acara (MICE)",
    ],
    "Perawatan SPA": ["SPA"],
    "Kejuruan Lainnya": ["Daya Tarik Wisata"],
    "Kesehatan dan Keselamatan Kerja (K3)": [
        "Jasa Transportasi Wisata", "Kawasan Pariwisata", "Penyelenggara Kegiatan Hiburan & Rekreasi",
        "SPA", "Jasa Makanan dan Minuman",
    ],
    "Pertolongan Pertama dan Penyelamatan": ["Kawasan Pariwisata", "Daya Tarik Wisata"],
    "Kerja Sama Tim dan Kepemimpinan": [
        "Penyelenggaraan Acara (MICE)", "Penyelenggara Kegiatan Hiburan & Rekreasi", "Jasa Pramuwisata",
    ],
    "Pengembangan Paket Wisata": ["Jasa Perjalanan Wisata", "Jasa Informasi Pariwisata"],
    "Operasional Wisata": ["Jasa Perjalanan Wisata", "Jasa Pramuwisata"],
    "Pengembangan SDM": ["Jasa Konsultan Pariwisata", "Kawasan Pariwisata"],
    "Perencanaan Bisnis": ["Jasa Konsultan Pariwisata", "Jasa Perjalanan Wisata"],
    "Riset Pasar dan Branding": ["Jasa Konsultan Pariwisata", "Jasa Informasi Pariwisata"],
    "Manajemen Keuangan": ["Penyediaan Akomodasi", "Jasa Perjalanan Wisata", "Jasa Konsultan Pariwisata"],
    "Penyajian Makanan dan Minuman": ["Jasa Makanan dan Minuman", "Penyediaan Akomodasi"],
    "Pengolahan Makanan": ["Jasa Makanan dan Minuman"],
    "Pemasaran dan Promosi": [
        "Daya Tarik Wisata", "Jasa Perjalanan Wisata", "Kawasan Pariwisata",
        "Penyediaan Akomodasi",
    ],
    "Manajemen Dapur": ["Jasa Makanan dan Minuman"],
    "Higiene dan Sanitasi": ["Jasa Makanan dan Minuman", "SPA", "Penyediaan Akomodasi"],
    "Analisis Data": ["Jasa Konsultan Pariwisata", "Jasa Informasi Pariwisata"],
    "Pengelolaan Destinasi": ["Kawasan Pariwisata", "Daya Tarik Wisata"],
    "Manajemen Event": [
        "Penyelenggaraan Acara (MICE)",
        "Penyelenggara Kegiatan Hiburan & Rekreasi",
    ],
    "Manajemen Halal": ["Jasa Makanan dan Minuman", "Penyediaan Akomodasi"],
    "Sistem Informasi": ["Jasa Informasi Pariwisata", "Penyediaan Akomodasi"],
    "Manajemen Inventori": ["Jasa Makanan dan Minuman", "Penyediaan Akomodasi"],
    "Bahasa Inggris": [
        "Jasa Pramuwisata", "Jasa Perjalanan Wisata", "Penyediaan Akomodasi",
        "Jasa Informasi Pariwisata",
    ],
    "Ticketing": ["Jasa Perjalanan Wisata", "Jasa Transportasi Wisata"],
    "Penjualan": ["Jasa Perjalanan Wisata", "Daya Tarik Wisata"],
    "Pengoperasian Komputer": ["Jasa Informasi Pariwisata", "Penyelenggaraan Acara (MICE)"],
    "Front Office": ["Penyediaan Akomodasi"],
    "Housekeeping": ["Penyediaan Akomodasi"],
}

# Kata kunci sinonim untuk fuzzy matching sederhana (tanpa ML)
SINONIM = {
    "k3": "Kesehatan dan Keselamatan Kerja (K3)",
    "keselamatan": "Kesehatan dan Keselamatan Kerja (K3)",
    "kesehatan kerja": "Kesehatan dan Keselamatan Kerja (K3)",
    "spa": "Perawatan SPA",
    "pijat": "Perawatan SPA",
    "wellness": "Perawatan SPA",
    "anatomi": "Perawatan SPA",
    "fisiologi": "Perawatan SPA",
    "aromaterapi": "Perawatan SPA",
    "mixologi": "Perawatan SPA",
    "event": "Manajemen Event",
    "mice": "Manajemen Event",
    "acara": "Manajemen Event",
    "halal": "Manajemen Halal",
    "bahasa inggris": "Bahasa Inggris",
    "english": "Bahasa Inggris",
    "reservasi": "Sistem Reservasi",
    "booking": "Sistem Reservasi",
    "front office": "Front Office",
    "housekeeping": "Housekeeping",
    "ticketing": "Ticketing",
    "dapur": "Manajemen Dapur",
    "memasak": "Pengolahan Makanan",
    "food": "Penyajian Makanan dan Minuman",
    "sanitasi": "Higiene dan Sanitasi",
    "hygiene": "Higiene dan Sanitasi",
    "promosi": "Pemasaran dan Promosi",
    "marketing": "Pemasaran dan Promosi",
    "digital marketing": "Pemasaran dan Promosi",
    "branding": "Riset Pasar dan Branding",
    "riset": "Riset Pasar dan Branding",
    "data": "Analisis Data",
    "analitik": "Analisis Data",
    "komputer": "Pengoperasian Komputer",
    "it": "Sistem Informasi",
    "sistem informasi": "Sistem Informasi",
    "keuangan": "Manajemen Keuangan",
    "finance": "Manajemen Keuangan",
    "akuntansi": "Manajemen Keuangan",
    "inventori": "Manajemen Inventori",
    "stok": "Manajemen Inventori",
    "pramuwisata": "Pemanduan Wisata",
    "pemandu": "Pemanduan Wisata",
    "tour guide": "Pemanduan Wisata",
    "paket wisata": "Pengembangan Paket Wisata",
    "tour package": "Pengembangan Paket Wisata",
    "destinasi": "Pengelolaan Destinasi",
    "lingkungan": "Pengelolaan Lingkungan",
    "sustainable": "Pariwisata Berkelanjutan",
    "berkelanjutan": "Pariwisata Berkelanjutan",
    "ekologi": "Pariwisata Berkelanjutan",
    "komunikasi": "Komunikasi",
    "presentation": "Komunikasi",
    "pertolongan pertama": "Pertolongan Pertama dan Penyelamatan",
    "p3k": "Pertolongan Pertama dan Penyelamatan",
    "first aid": "Pertolongan Pertama dan Penyelamatan",
    "leadership": "Kerja Sama Tim dan Kepemimpinan",
    "teamwork": "Kerja Sama Tim dan Kepemimpinan",
    "kepemimpinan": "Kerja Sama Tim dan Kepemimpinan",
    "risiko": "Manajemen Risiko",
    "risk": "Manajemen Risiko",
    "kerumunan": "Manajemen Risiko",
    "sdm": "Pengembangan SDM",
    "hrm": "Pengembangan SDM",
    "bisnis": "Perencanaan Bisnis",
    "business plan": "Perencanaan Bisnis",
    "operasional": "Operasional Wisata",
    "penjualan": "Penjualan",
    "sales": "Penjualan",
    "layanan pelanggan": "Pelayanan Pelanggan",
    "customer service": "Pelayanan Pelanggan",
    "transportasi": "Jasa Transportasi Wisata",
}


def match_skill(input_text: str) -> list[str]:
    """
    Cocokkan input judul materi pelatihan ke demand skill.
    Return list of matched skill names.
    """
    lowered = input_text.lower().strip()
    matched = []

    # Exact match dalam COVERAGE_SCORE
    for skill in COVERAGE_SCORE:
        if skill.lower() == lowered:
            matched.append(skill)

    # Substring match
    if not matched:
        for skill in COVERAGE_SCORE:
            if lowered in skill.lower() or skill.lower() in lowered:
                matched.append(skill)

    # Sinonim match
    if not matched:
        for keyword, skill in SINONIM.items():
            if keyword in lowered:
                if skill not in matched:
                    matched.append(skill)

    return matched


def simulate_training(new_modules: list[str]) -> dict:
    """
    Simulasikan penambahan materi pelatihan baru.
    
    Returns:
        dict dengan before/after gap score per subsektor yang terpengaruh
    """
    # Salin data awal
    updated_coverage = dict(COVERAGE_SCORE)
    affected_skills = []
    module_skills = {}

    for module in new_modules:
        matched = match_skill(module)
        module_skills[module] = matched
        for skill in matched:
            if updated_coverage.get(skill, 1.0) < 1.0:
                updated_coverage[skill] = 1.0  # Asumsi pelatihan baru = fully covered
                if skill not in affected_skills:
                    affected_skills.append(skill)

    if not affected_skills:
        return {
            "affected_skills": [],
            "before": dict(GAP_SCORE),
            "after": dict(GAP_SCORE),
            "delta": {},
        }

    # Hitung ulang gap score per subsektor yang terpengaruh
    from data.demand_skill import DEMAND_MATRIX, TOP15_SKILLS

    affected_subsektors = set()
    for skill in affected_skills:
        subs = SKILL_TO_SUBSEKTOR.get(skill, [])
        affected_subsektors.update(subs)

    before_gap = dict(GAP_SCORE)
    after_gap = dict(GAP_SCORE)

    # Estimasi penurunan gap: proporsional terhadap bobot skill dalam subsektor
    for subsektor in affected_subsektors:
        if subsektor not in after_gap:
            continue
        reduction = 0.0
        for skill in affected_skills:
            if subsektor in SKILL_TO_SUBSEKTOR.get(skill, []):
                # Bobot penurunan = (1 - coverage_lama) * bobot_skill_dalam_subsektor / 100
                old_cov = COVERAGE_SCORE.get(skill, 1.0)
                if skill in TOP15_SKILLS and subsektor in DEMAND_MATRIX:
                    idx = TOP15_SKILLS.index(skill)
                    bobot = DEMAND_MATRIX[subsektor][idx] / 100
                    reduction += (1.0 - old_cov) * bobot * 100
        after_gap[subsektor] = max(0.0, round(after_gap[subsektor] - reduction, 2))

    delta = {
        sub: round(before_gap[sub] - after_gap[sub], 2)
        for sub in affected_subsektors
        if sub in before_gap
    }

    return {
        "affected_skills": affected_skills,
        "module_skills": module_skills,
        "before": before_gap,
        "after": after_gap,
        "delta": delta,
    }