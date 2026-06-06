"""
Data Coverage Score & Gap Score per Demand Skill dan Subsektor
Sumber: Hasil analisis SKKNI vs Materi Pelatihan Kemnaker
"""

import pandas as pd

# ── Coverage Score per Demand Skill ───────────────────────────────────────
COVERAGE_SCORE = {
    "Pemanduan Wisata": 1.0,
    "Pariwisata Berkelanjutan": 1.0,
    "Pengelolaan Lingkungan": 1.0,
    "Manajemen Risiko": 0.5,
    "Pelayanan Pelanggan": 1.0,
    "Komunikasi": 1.0,
    "Sistem Reservasi": 1.0,
    "Administrasi dan Pelaporan": 1.0,
    "Perawatan SPA": 0.5,
    "Kejuruan Lainnya": 1.0,
    "Kesehatan dan Keselamatan Kerja (K3)": 0.0,
    "Pertolongan Pertama dan Penyelamatan": 1.0,
    "Kerja Sama Tim dan Kepemimpinan": 1.0,
    "Pengembangan Paket Wisata": 1.0,
    "Operasional Wisata": 1.0,
    "Pengembangan SDM": 1.0,
    "Perencanaan Bisnis": 1.0,
    "Riset Pasar dan Branding": 0.5,
    "Manajemen Keuangan": 1.0,
    "Penyajian Makanan dan Minuman": 1.0,
    "Pengolahan Makanan": 1.0,
    "Pemasaran dan Promosi": 1.0,
    "Manajemen Dapur": 1.0,
    "Higiene dan Sanitasi": 0.5,
    "Analisis Data": 0.5,
    "Pengelolaan Destinasi": 1.0,
    "Manajemen Event": 0.5,
    "Manajemen Halal": 0.5,
    "Sistem Informasi": 1.0,
    "Manajemen Inventori": 1.0,
    "Bahasa Inggris": 1.0,
    "Ticketing": 0.5,
    "Penjualan": 0.5,
    "Pengoperasian Komputer": 1.0,
    "Front Office": 1.0,
    "Housekeeping": 0.5,
}

COVERAGE_LABEL = {
    1.0: "Fully Covered",
    0.5: "Partially Covered",
    0.0: "Not Covered",
}

COVERAGE_COLOR = {
    1.0: "#2ecc71",
    0.5: "#ebc26c",
    0.0: "#e74c3c",
}


def get_df_coverage():
    df = pd.DataFrame(
        [(k, v, COVERAGE_LABEL[v]) for k, v in COVERAGE_SCORE.items()],
        columns=["Demand Skill", "Score", "Status"],
    ).sort_values("Score", ascending=False)
    return df


# ── Gap Score per Subsektor ────────────────────────────────────────────────
# Gap = (Jumlah Demand Skill - Total Coverage) / Jumlah Demand Skill
# dalam persen (%)
GAP_SCORE = {
    "SPA": 32.38,
    "Penyelenggaraan Acara (MICE)": 15.73,
    "Jasa Informasi Pariwisata": 8.33,
    "Jasa Konsultan Pariwisata": 6.52,
    "Jasa Makanan dan Minuman": 5.58,
    "Jasa Perjalanan Wisata": 4.21,
    "Penyelenggara Kegiatan Hiburan & Rekreasi": 3.33,
    "Kawasan Pariwisata": 2.88,
    "Jasa Pramuwisata": 2.71,
    "Penyediaan Akomodasi": 2.43,
    "Daya Tarik Wisata": 1.32,
    "Jasa Transportasi Wisata": 0.00,
}


def get_df_gap():
    df = pd.DataFrame(
        list(GAP_SCORE.items()), columns=["Subsektor", "Gap_Score"]
    ).sort_values("Gap_Score", ascending=True)
    return df