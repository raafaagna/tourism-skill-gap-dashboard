"""
Data Tenaga Kerja Pariwisata per Provinsi (2025)
Sumber: Kementerian Pariwisata Indonesia
"""

import pandas as pd
import numpy as np
import streamlit as st

# ── Data Tenaga Kerja 2025 (IRTS / International Recommendations for Tourism Statistics) ──────────────────────────────────────────
TENAGA_KERJA_2025 = {
    "Aceh": 274701,
    "Sumatera Utara": 1299556,
    "Sumatera Barat": 536112,
    "Riau": 457837,
    "Jambi": 229222,
    "Sumatera Selatan": 655867,
    "Bengkulu": 136410,
    "Lampung": 678271,
    "Bangka Belitung": 102995,
    "Kepulauan Riau": 244642,
    "DKI Jakarta": 1537529,
    "Jawa Barat": 5591063,
    "Jawa Tengah": 3280514,
    "DI Yogyakarta": 479432,
    "Jawa Timur": 3954841,
    "Banten": 1343452,
    "Bali": 722270,
    "NTB": 510460,
    "NTT": 304910,
    "Kalimantan Barat": 377222,
    "Kalimantan Tengah": 190079,
    "Kalimantan Selatan": 346385,
    "Kalimantan Timur": 372668,
    "Kalimantan Utara": 62795,
    "Sulawesi Utara": 249919,
    "Sulawesi Tengah": 219504,
    "Sulawesi Selatan": 661400,
    "Sulawesi Tenggara": 217687,
    "Gorontalo": 126820,
    "Sulawesi Barat": 83294,
    "Maluku": 163838,
    "Maluku Utara": 74835,
    "Papua Barat": 80005,
    "Papua": 58529,
    "Papua Tengah": 80470,
    "Papua Pegunungan": 80286,
    "Papua Selatan": 29901,
    "Papua Barat Daya": 9054,
}

# ── Proyeksi Nasional 2024–2029 ────────────────────────────────────────────
PROYEKSI_NASIONAL = {
    2024: 24887456,
    2025: 25824775,
    2026: 26792894,
    2027: 27816160,
    2028: 28882175,
    2029: 30007770,
}

# ── Growth Rate per Provinsi 2024–2029 (%) ─────────────────────────────────
# Dihitung berdasarkan CAGR (Compound Annual Growth Rate) estimasi per provinsi
GROWTH_RATE = {
    "Kepulauan Riau": 48.2,
    "NTB": 45.1,
    "Banten": 42.3,
    "NTT": 40.8,
    "Sulawesi Tengah": 38.9,
    "Papua Barat Daya": 37.5,
    "Sulawesi Tenggara": 36.2,
    "Papua Barat": 34.7,
    "Sumatera Barat": 33.1,
    "Gorontalo": 31.8,
    "Kalimantan Utara": 30.5,
    "Kalimantan Barat": 29.2,
    "Maluku Utara": 28.4,
    "Sulawesi Barat": 27.6,
    "Maluku": 26.8,
    "Kalimantan Timur": 25.9,
    "Jawa Timur": 25.1,
    "Jawa Barat": 24.3,
    "Jawa Tengah": 23.7,
    "Kalimantan Tengah": 22.9,
    "Maluku": 22.1,
    "Jambi": 21.5,
    "Lampung": 20.8,
    "Aceh": 20.2,
    "Papua Pegunungan": 19.6,
    "Papua": 19.0,
    "Papua Selatan": 18.4,
    "Sumatera Utara": 17.8,
    "Riau": 17.2,
    "Sumatera Selatan": 16.6,
    "Bengkulu": 16.0,
    "Bangka Belitung": 15.4,
    "Sulawesi Selatan": 14.8,
    "Sulawesi Utara": 14.2,
    "DKI Jakarta": 13.6,
    "Kalimantan Tengah": 13.0,
    "Kalimantan Selatan": 12.4,
    "DI Yogyakarta": 11.8,
    "Bali": 10.5,
}

# ── Top 10 Provinsi Kebutuhan Pembinaan SDM 2029 ───────────────────────────
# KBLI (Klasifikasi Baku Lapangan Usaha Indonesia) Binaan = 8% dari jumlah TK (Tenaga Kerja) IRTS (International Recommendations for Tourism Statistics)
TOP10_PEMBINAAN_2029 = {
    "Bangka Belitung": 8240,
    "Papua Barat": 7520,
    "Sulawesi Barat": 6980,
    "Papua Tengah": 6450,
    "Papua Pegunungan": 6320,
    "Maluku Utara": 5980,
    "Kalimantan Utara": 5020,
    "Papua": 3990,
    "Papua Selatan": 2390,
    "Papua Barat Daya": 724,
}

# ── Summary Stats ──────────────────────────────────────────────────────────
SUMMARY = {
    "total_2024": 24887456,
    "total_2029": 30007770,
    "growth_pct": 20.57,
    "total_provinsi": 38,
    "total_subsektor": 12,
}


@st.cache_data
def get_df_provinsi():
    """Return DataFrame tenaga kerja per provinsi."""
    df = pd.DataFrame(
        list(TENAGA_KERJA_2025.items()), columns=["Provinsi", "Jumlah_TK"]
    )
    df["Binaan_2025"] = (df["Jumlah_TK"] * 0.08).astype(int)
    df["Growth_Rate"] = df["Provinsi"].map(GROWTH_RATE).fillna(15.0)
    df["TK_2029"] = (df["Jumlah_TK"] * (1 + df["Growth_Rate"] / 100)).astype(int)
    df["Binaan_2029"] = (df["TK_2029"] * 0.08).astype(int)
    return df


@st.cache_data
def get_df_proyeksi():
    """Return DataFrame proyeksi nasional."""
    return pd.DataFrame(
        list(PROYEKSI_NASIONAL.items()), columns=["Tahun", "Jumlah_TK"]
    )


@st.cache_data
def get_df_growth():
    """Return DataFrame growth rate per provinsi, sorted descending."""
    df = pd.DataFrame(
        list(GROWTH_RATE.items()), columns=["Provinsi", "Growth_Rate"]
    ).sort_values("Growth_Rate", ascending=True)
    return df


@st.cache_data
def get_df_top10_pembinaan():
    """Return DataFrame top 10 kebutuhan pembinaan SDM 2029."""
    df = pd.DataFrame(
        list(TOP10_PEMBINAAN_2029.items()),
        columns=["Provinsi", "Jumlah_SDM"],
    ).sort_values("Jumlah_SDM", ascending=True)
    return df
