import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    demand_path = os.path.join(base_dir, 'Demand Skill per Subsektor.xlsx')
    coverage_path = os.path.join(base_dir, 'Coverage Score per Demand Skill.xlsx')
    
    df_demand = pd.read_excel(demand_path)
    df_cov = pd.read_excel(coverage_path)
    
    return df_demand, df_cov

@st.cache_data
def get_base_gap_scores():
    df_demand, df_cov = load_data()
    
    # 1. Total demand skill yang dibutuhkan pada setiap subsektor
    # 2. Total coverage score per subsektor
    df = df_demand.merge(df_cov[['Demand Skill', 'Coverage Score']], on='Demand Skill', how='left')
    df['Coverage Score'] = df['Coverage Score'].fillna(0)
    df['Total Coverage'] = df['Frekuensi'] * df['Coverage Score']
    
    res = df.groupby('Subsektor').agg(
        Total_Demand=('Frekuensi', 'sum'),
        Total_Coverage=('Total Coverage', 'sum')
    ).reset_index()
    
    # 3. Persentase coverage per subsektor
    # 4. Persentase gap per subsektor (100% - %coverage)
    res['Pct_Coverage'] = (res['Total_Coverage'] / res['Total_Demand']) * 100
    res['Gap_Score'] = 100.0 - res['Pct_Coverage']
    
    gap_dict = dict(zip(res['Subsektor'], res['Gap_Score']))
    return gap_dict

@st.cache_data
def get_original_similarities_and_coverages():
    _, df_cov = load_data()
    result = {}
    for _, row in df_cov.iterrows():
        skill = row['Demand Skill']
        sim = row.get('Score Cosine Similarity', 0.0)
        cov = row['Coverage Score']
        result[skill] = {'sim': float(sim), 'cov': float(cov)}
    return result

@st.cache_data
def get_demand_frequency_per_subsektor():
    df_demand, _ = load_data()
    res = {}
    for _, row in df_demand.iterrows():
        sub = row['Subsektor']
        skill = row['Demand Skill']
        freq = row['Frekuensi']
        if sub not in res:
            res[sub] = {}
        res[sub][skill] = freq
    return res

@st.cache_data
def get_all_demand_skills():
    _, df_cov = load_data()
    return list(df_cov['Demand Skill'].unique())

@st.cache_data
def get_all_subsektors():
    df_demand, _ = load_data()
    return list(df_demand['Subsektor'].unique())
