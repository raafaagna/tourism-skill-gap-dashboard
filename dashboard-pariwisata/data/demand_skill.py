"""
Data Pemetaan Demand Skill per Subsektor
Nilai = persentase bobot kebutuhan skill dalam subsektor tersebut
"""

import pandas as pd
import numpy as np

SUBSEKTORS = [
    "Daya Tarik Wisata",
    "Jasa Informasi Pariwisata",
    "Jasa Konsultan Pariwisata",
    "Jasa Makanan dan Minuman",
    "Jasa Perjalanan Wisata",
    "Jasa Pramuwisata",
    "Jasa Transportasi Wisata",
    "Kawasan Pariwisata",
    "Penyediaan Akomodasi",
    "Penyelenggara Kegiatan Hiburan & Rekreasi",
    "Penyelenggaraan Acara (MICE)",
    "SPA",
]

# Top 15 Demand Skill berdasarkan rancangan dashboard
TOP15_SKILLS = [
    "Kejuruan Lainnya",
    "Pemanduan Wisata",
    "Perawatan SPA",
    "Pelayanan Pelanggan",
    "Kerja Sama Tim dan Kepemimpinan",
    "Pengolahan Makanan",
    "Perencanaan Bisnis",
    "Manajemen Dapur",
    "Manajemen Event",
    "Penyajian Makanan dan Minuman",
    "Operasional Wisata",
    "Administrasi dan Pelaporan",
    "Komunikasi",
    "Pengelolaan Lingkungan",
    "Pengembangan SDM",
]

# Matrix bobot (%) demand skill per subsektor — disesuaikan dari chart rancangan
# Baris = subsektor, Kolom = top 15 skills
DEMAND_MATRIX = {
    "Daya Tarik Wisata":                         [42.9,  2.9,  0.0,  2.9, 11.4,  8.6, 17.1,  0.0,  0.0,  0.0,  0.0,  2.9,  2.9,  0.0,  8.6],
    "Jasa Informasi Pariwisata":                 [12.5,  0.0,  0.0,  0.0, 12.5, 50.0,  0.0,  0.0,  0.0,  0.0, 12.5,  0.0, 12.5,  0.0,  0.0],
    "Jasa Konsultan Pariwisata":                 [33.3,  0.0,  0.0, 14.8, 11.1,  3.7, 14.8,  3.7,  0.0,  0.0,  0.0,  3.7,  7.4,  0.0,  7.4],
    "Jasa Makanan dan Minuman":                  [13.1,  0.0,  0.0, 11.6,  3.0, 18.1, 10.1, 20.1,  0.5,  9.5,  0.0,  4.0,  4.5,  3.5,  2.0],
    "Jasa Perjalanan Wisata":                    [29.4,  1.6,  0.0,  8.7, 21.4,  0.0,  7.9,  4.0,  0.8,  0.0, 11.1,  6.3,  1.6,  3.2,  4.0],
    "Jasa Pramuwisata":                          [13.8, 50.5,  0.2,  5.8,  4.3,  0.5,  1.4,  1.9,  0.5,  0.0,  6.0,  3.1,  3.6,  5.8,  2.4],
    "Jasa Transportasi Wisata":                  [ 0.0, 14.3,  0.0, 28.6,  0.0,  0.0, 14.3,  0.0,  0.0,  0.0, 14.3, 14.3,  0.0,  0.0, 14.3],
    "Kawasan Pariwisata":                        [ 4.8,  9.5,  0.0, 14.3,  7.1,  0.0, 16.7,  0.0,  2.4,  2.4, 23.8,  7.1,  0.0,  9.5,  2.4],
    "Penyediaan Akomodasi":                      [29.1,  0.0,  0.0, 11.9,  3.8, 16.5,  3.8,  5.0,  0.0, 15.7,  1.5,  4.6,  2.3,  2.3,  3.4],
    "Penyelenggara Kegiatan Hiburan & Rekreasi": [10.4, 49.4,  1.3,  7.8,  9.1,  0.0,  2.6,  3.9,  0.0,  0.0,  3.9,  1.3,  3.9,  5.2,  1.3],
    "Penyelenggaraan Acara (MICE)":              [28.1,  0.0,  0.0,  3.1, 18.8,  3.1,  9.9,  0.5, 30.2,  0.0,  0.0,  1.6,  3.1,  0.0,  1.6],
    "SPA":                                       [19.7,  0.0, 66.1,  4.7,  2.1,  0.0,  2.1,  0.0,  0.0,  0.0,  0.9,  0.4,  2.1,  0.4,  1.3],
}


def get_df_demand_matrix():
    df = pd.DataFrame(DEMAND_MATRIX, index=TOP15_SKILLS).T
    return df


def get_top_skill_per_subsektor():
    """Return the most demanded skill per subsektor."""
    df = get_df_demand_matrix()
    result = []
    for sub in df.index:
        top_skill = df.loc[sub].idxmax()
        top_val = df.loc[sub].max()
        result.append({"Subsektor": sub, "Top Skill": top_skill, "Bobot (%)": round(top_val, 1)})
    return pd.DataFrame(result)


# ── Rekomendasi per Subsektor Prioritas ──────────────────────────────────
REKOMENDASI = {
    "SPA": {
        "gap": "32.38%",
        "temuan": [
            "Terdapat beberapa kompetensi teknis penting yang dibutuhkan industri SPA tetapi belum tercakup dalam modul pelatihan yang tersedia.",
            "Materi pelatihan saat ini belum sepenuhnya mengakomodasi perkembangan kebutuhan kompetensi di subsektor SPA.",
        ],
        "dampak": [
            "Terjadi kesenjangan antara kompetensi yang dimiliki tenaga kerja dengan kompetensi yang dibutuhkan industri.",
            "Lulusan pelatihan berpotensi belum memenuhi standar keterampilan yang diharapkan pelaku industri SPA.",
            "Produktivitas dan kualitas layanan SPA dapat terpengaruh akibat keterbatasan kompetensi tenaga kerja.",
        ],
        "rekomendasi": [
            "Membangun kolaborasi dengan praktisi dan pelaku industri SPA dalam penyusunan kurikulum.",
            "Mengembangkan modul pelatihan baru yang berfokus pada kompetensi yang belum tercakup.",
            "Melakukan evaluasi dan pembaruan kurikulum secara berkala agar tetap selaras dengan kebutuhan industri.",
        ],
    },
    "Penyelenggaraan Acara (MICE)": {
        "gap": "15.73%",
        "temuan": [
            "Materi pelatihan MICE telah tersedia, namun belum sepenuhnya mencakup kebutuhan dan tren industri terkini.",
            "Sebagian kompetensi yang dibutuhkan industri modern masih belum terakomodasi secara optimal.",
        ],
        "dampak": [
            "Kompetensi tenaga kerja berpotensi kurang relevan dengan perkembangan industri MICE yang dinamis.",
            "Kesiapan tenaga kerja dalam menghadapi tren dan kebutuhan acara modern masih perlu ditingkatkan.",
        ],
        "rekomendasi": [
            "Menambahkan pelatihan singkat atau materi pendukung terkait tren industri MICE terkini.",
            "Melakukan pembaruan materi secara berkala agar tetap selaras dengan perkembangan industri.",
            "Meningkatkan kolaborasi dengan pelaku industri MICE untuk memastikan materi pelatihan sesuai dengan kebutuhan lapangan.",
        ],
    },
    "Jasa Informasi Pariwisata": {
        "gap": "8.33%",
        "temuan": [
            "Skill digital dan teknologi informasi pariwisata belum sepenuhnya terwakili dalam modul pelatihan.",
            "Penguasaan sistem informasi pariwisata berbasis teknologi terkini masih terbatas dalam supply pelatihan.",
        ],
        "dampak": [
            "Tenaga kerja di sektor ini berisiko kurang siap menghadapi transformasi digital pariwisata.",
            "Kualitas layanan informasi pariwisata kepada wisatawan dapat terdampak.",
        ],
        "rekomendasi": [
            "Integrasikan modul teknologi informasi dan digital tourism ke dalam kurikulum pelatihan.",
            "Adakan pelatihan khusus terkait platform digital pariwisata yang sedang berkembang.",
        ],
    },
}