"""
Utilities: shared styling, chart templates, header component
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
import os
import base64

# ── Brand Colors ────────────────────────────────────────────────────────────
PRIMARY   = "#142c50"
ACCENT    = "#ebc26c"
BG        = "#ffffff"
LIGHT_BG  = "#f0f4f8"
TEXT      = "#1e2d3d"
SUCCESS   = "#27ae60"
WARNING   = "#ebc26c"
DANGER    = "#e74c3c"
GRID      = "#e8edf3"

SEQUENTIAL = [
    "#d4e6f8", "#a8cdf0", "#7bb4e8", "#4f9be0",
    "#2282d8", "#142c50", "#0e1f38",
]

DIVERGING = [DANGER, WARNING, SUCCESS]


# ── Global CSS ───────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'DM Sans', sans-serif !important;
            color: {TEXT};
        }}

        /* App background */
        .stApp {{
            background-color: #f0f4f8;
        }}

        /* Remove default streamlit block spacing */
        .stMarkdown, .stPlotlyChart {{
            margin-bottom: 0 !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0e1f38 0%, {PRIMARY} 100%) !important;
        }}
        [data-testid="stSidebar"] * {{
            color: #ffffff !important;
        }}
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] a {{
            font-family: 'DM Sans', sans-serif !important;
        }}
        /* Restore Material Symbols font for icons */
        /* Restore Material Symbols font GLOBALLY so icons render correctly (fixes keyboard_double_arrow_left text) */
        .material-symbols-rounded,
        .material-symbols-outlined,
        .material-icons {{
            font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        }}
        [data-testid="stSidebarNav"] a {{
            color: #b0c8e0 !important;
            font-weight: 500;
            border-radius: 8px;
            padding: 8px 12px;
            margin: 2px 0;
            transition: all 0.2s ease;
            font-size: 0.9rem;
        }}
        [data-testid="stSidebarNav"] a:hover,
        [data-testid="stSidebarNav"] a[aria-selected="true"] {{
            background: rgba(235,194,108,0.15) !important;
            color: {ACCENT} !important;
            border-left: 3px solid {ACCENT};
        }}

        /* Rename 'app' to 'Beranda' in sidebar via CSS */
        [data-testid="stSidebarNav"] ul li:nth-child(1) a span {{
            visibility: hidden;
            position: relative;
        }}
        [data-testid="stSidebarNav"] ul li:nth-child(1) a span::after {{
            content: "Beranda";
            visibility: visible;
            position: absolute;
            left: 0;
            top: 0;
            white-space: nowrap;
        }}

        /* Hide Streamlit Footer only */
        footer {{
            display: none !important;
            visibility: hidden !important;
        }}
        
        /* Make Header transparent so it doesn't leave blank space but keeps collapse button visible */
        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}

        /* Extra override to remove top gap */
        .main > div:first-child {{
            padding-top: 0 !important;
        }}

        /* Main content */
        .main .block-container {{
            padding-top: 0rem !important;
            margin-top: -55px !important;
            padding-bottom: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 100% !important;
        }}

        /* Headers */
        h1 {{ color: {PRIMARY}; font-weight: 700; font-size: 1.8rem; font-family: 'DM Sans', sans-serif !important; }}
        h2 {{ color: {PRIMARY}; font-weight: 600; font-size: 1.3rem; font-family: 'DM Sans', sans-serif !important; }}
        h3 {{ color: {PRIMARY}; font-weight: 600; font-size: 1.1rem; font-family: 'DM Sans', sans-serif !important; }}

        /* ─── Metric cards ─────────────────────────────── */
        .metric-card {{
            background: #ffffff;
            color: {TEXT};
            border-radius: 12px;
            padding: 20px 22px;
            text-align: left;
            border: 1px solid #dde4ed;
            box-shadow: 0 1px 4px rgba(20,44,80,0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            height: 100%;
        }}
        .metric-card:hover {{
            box-shadow: 0 6px 20px rgba(20,44,80,0.08);
            transform: translateY(-2px);
        }}
        .metric-card .metric-label {{
            font-size: 0.72rem;
            color: #7b8ea3;
            margin-bottom: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .metric-card .metric-value {{
            font-size: 1.9rem;
            font-weight: 800;
            color: {TEXT};
            line-height: 1.1;
        }}
        .metric-card .metric-sub {{
            font-size: 0.78rem;
            color: #94a3b8;
            margin-top: 8px;
            font-weight: 500;
        }}

        /* ─── Section title ─────────────────────────────── */
        .section-title {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: {PRIMARY};
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: -0.2px;
            padding: 0 0 10px 0;
            margin-top: 28px;
            margin-bottom: 16px;
            border-bottom: 2px solid {ACCENT};
        }}

        /* ─── Insight box ────────────────────────────────── */
        .insight-box {{
            background: #f8fafc;
            border-left: 4px solid {ACCENT};
            border-radius: 0 10px 10px 0;
            padding: 14px 18px;
            font-size: 0.87rem;
            color: {TEXT};
            margin-top: 12px;
            border: 1px solid #e1e8f0;
            border-left: 4px solid {ACCENT};
        }}
        .insight-box b {{ color: {PRIMARY}; }}

        /* ─── Chart container ────────────────────────────── */
        .chart-card {{
            background: #ffffff;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #dde4ed;
            box-shadow: 0 1px 4px rgba(20,44,80,0.04);
            margin-bottom: 0;
        }}

        /* ─── Info badge ─────────────────────────────────── */
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
        }}
        .badge-success {{ background: #e8f8f0; color: #1a7a47; }}
        .badge-warning {{ background: #fef9ec; color: #b8860b; }}
        .badge-danger  {{ background: #fdf0ee; color: #c0392b; }}

        /* ─── Custom Text Input ────────────────────────────── */
        .stTextInput div[data-baseweb="base-input"] {{
            border: 1.5px solid #a3b8cc !important;
            border-radius: 8px !important;
            background-color: #ffffff !important;
            transition: all 0.2s ease;
        }}
        .stTextInput div[data-baseweb="base-input"]:hover {{
            border-color: #7b8ea3 !important;
        }}
        .stTextInput div[data-baseweb="base-input"]:focus-within {{
            border-color: {PRIMARY} !important;
            box-shadow: 0 0 0 2px rgba(20,44,80,0.15) !important;
        }}
        .stTextInput input {{
            font-family: 'DM Sans', sans-serif !important;
            color: {TEXT} !important;
            font-size: 0.95rem !important;
            padding: 4px 6px !important;
        }}

        /* ─── Rekomendasi card ───────────────────────────── */
        .rekom-card {{
            border: 1px solid #dde4ed;
            border-radius: 12px;
            padding: 22px 24px;
            margin-bottom: 16px;
            background: #ffffff;
            box-shadow: 0 1px 4px rgba(20,44,80,0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .rekom-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(20,44,80,0.08);
        }}
        .rekom-card .rekom-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        .rekom-card .rekom-gap {{
            font-size: 1.6rem;
            font-weight: 800;
            color: {DANGER};
            font-family: 'DM Sans', sans-serif;
        }}
        .rekom-card .rekom-title {{
            font-size: 0.82rem;
            font-weight: 600;
            color: #7b8ea3;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }}

        /* ─── Simulator result card ──────────────────────── */
        .sim-result-card {{
            background: #f8fafc;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 12px;
            border: 1px solid #dde4ed;
        }}

        /* ─── Page header ────────────────────────────────── */
        .page-header {{
            background: linear-gradient(135deg, {PRIMARY} 0%, #1e4a85 100%);
            padding: 36px 40px 28px;
            margin-left: -2rem;
            margin-right: -2rem;
            margin-top: 0;
            margin-bottom: 28px;
            color: white;
            border-bottom: 3px solid {ACCENT};
        }}
        .page-header h1 {{
            color: white;
            margin: 0;
            font-size: 1.65rem;
            letter-spacing: -0.3px;
            font-weight: 700;
        }}
        .page-header .page-header-icon {{
            font-size: 2rem;
            margin-bottom: 8px;
            display: block;
        }}
        .page-header p {{
            color: #b0c4de;
            margin: 6px 0 0;
            font-size: 0.88rem;
            font-weight: 400;
        }}

        /* ─── Divider ────────────────────────────────────── */
        hr {{
            border: none;
            border-top: 1px solid {GRID};
            margin: 24px 0;
        }}

        /* ─── Dataframe styling ──────────────────────────── */
        [data-testid="stDataFrame"] {{
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #dde4ed;
        }}

        /* ─── Streamlit native widgets ───────────────────── */
        .stSelectbox > div > div,
        .stTextInput > div > div {{
            border-radius: 8px;
            border-color: #dde4ed;
            font-family: 'DM Sans', sans-serif !important;
        }}
        .stButton > button {{
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 600;
            border-radius: 8px;
        }}

        /* ─── Streamlit info/success/warning/error ───────── */
        [data-testid="stAlert"] {{
            border-radius: 10px;
            font-family: 'DM Sans', sans-serif;
        }}

        /* ─── Tabs ───────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px 8px 0 0;
            padding: 8px 18px;
            font-weight: 600;
            font-family: 'DM Sans', sans-serif;
        }}

        /* Remove extra blank space from plotly charts container */
        [data-testid="stPlotlyChart"] > div {{
            border-radius: 12px;
            overflow: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Plotly Base Template ─────────────────────────────────────────────────────
def base_layout(title="", height=420):
    return dict(
        title=dict(
            text=title,
            font=dict(size=14, color=PRIMARY, family="DM Sans"),
            x=0.0,
            xanchor="left",
        ),
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="DM Sans", size=12, color=TEXT),
        margin=dict(l=20, r=20, t=50 if title else 20, b=20),
        xaxis=dict(
            gridcolor="rgba(0,0,0,0)",
            linecolor="#e1e8f0",
            tickfont=dict(size=11, family="DM Sans"),
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor="#f0f4f8",
            linecolor="#e1e8f0",
            tickfont=dict(size=11, family="DM Sans"),
            zeroline=False,
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor=GRID,
            borderwidth=1,
            font=dict(size=11, family="DM Sans"),
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor=PRIMARY,
            font=dict(family="DM Sans", size=12),
        ),
    )


# ── Helper UI Components ─────────────────────────────────────────────────────
def metric_card(label: str, value: str, sub: str = "", icon: str = "", border_color: str = "#e2e8f0"):
    st.markdown(
        f"""
        <div class="metric-card" style="border-top: 3px solid {border_color};">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{icon} {value}</div>
            {"<div class='metric-sub'>"+sub+"</div>" if sub else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, icon: str = ""):
    prefix = f"{icon} " if icon else ""
    st.markdown(
        f'<div class="section-title">{prefix}{title}</div>',
        unsafe_allow_html=True,
    )


def insight_box(text: str):
    st.markdown(
        f'<div class="insight-box">💡 {text}</div>',
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "", icon: str = ""):
    st.markdown(
        f"""
        <div class="page-header">
            {"<span class='page-header-icon'>"+icon+"</span>" if icon else ""}
            <h1>{title}</h1>
            {"<p>"+subtitle+"</p>" if subtitle else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return ""

def render_sidebar_header():
    """Render logo & identitas di sidebar."""
    with st.sidebar:
        kem_b64 = get_base64_image("assets/kemenpar.png")
        unair_b64 = get_base64_image("assets/unair.png")
        ftmm_b64 = get_base64_image("assets/ftmm.png")

        # Logo row
        logos_html = '<div style="display: flex; justify-content: center; align-items: center; gap: 14px; margin-bottom: 20px; margin-top: 8px; padding: 14px; background: rgba(255,255,255,0.06); border-radius: 10px;">'
        if kem_b64:
            logos_html += f'<img src="data:image/png;base64,{kem_b64}" style="height: 30px; width: auto; object-fit: contain;" />'
        else:
            logos_html += '<span style="font-size: 1.5rem;">🏛️</span>'
            
        if unair_b64:
            logos_html += f'<img src="data:image/png;base64,{unair_b64}" style="height: 30px; width: auto; object-fit: contain;" />'
        else:
            logos_html += '<span style="font-size: 1.5rem;">🎓</span>'
            
        if ftmm_b64:
            logos_html += f'<img src="data:image/png;base64,{ftmm_b64}" style="height: 24px; width: auto; object-fit: contain;" />'
        else:
            logos_html += '<span style="font-size: 1.5rem;">🔬</span>'
        logos_html += '</div>'

        st.markdown(logos_html, unsafe_allow_html=True)

        # Informasi dashboard
        st.markdown(
            """
            <div style='background: rgba(255,255,255,0.06); padding: 16px 18px; border-radius: 10px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.08); width: 100%; box-sizing: border-box; word-wrap: break-word;'>
                <div style='font-size:0.82rem; color:#cbd5e1; line-height:1.8;'>
                <b style='color:#ebc26c; font-size:0.88rem; display:block; margin-bottom:10px; line-height:1.4;'>Dashboard Analisis Kesenjangan Kompetensi Pariwisata</b>
                <span style='color: #7b9ab5;'>Mata Kuliah:</span> Sains Data Consulting<br>
                <span style='color: #7b9ab5;'>Prodi:</span> Teknologi Sains Data<br>
                FTMM – Universitas Airlangga<br><br>
                <span style='color: #7b9ab5;'>Mitra:</span> Kementerian Pariwisata RI<br>
                <span style='color: #7b9ab5;'>Tim:</span> Kelompok 8 SDC SD-A2
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )