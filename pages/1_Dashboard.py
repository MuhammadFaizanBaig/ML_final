import os
import glob
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(
    page_title="AQI Dashboard - Global Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
<style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], header[data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1350px;
    }
    .stApp {
        background: linear-gradient(180deg, rgba(11, 17, 32, 0.85) 0%, rgba(11, 17, 32, 0.95) 100%),
                    url('https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?auto=format&fit=crop&w=1920&q=80') !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }
    .kpi-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #60a5fa;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# --- Top Navigation Bar ---
nav_brand, nav_items = st.columns([2, 2.5])
with nav_brand:
    st.markdown("<h3 style='margin-top:8px; font-weight:800; color:#ffffff;'>AQI<span style='color:#3b82f6;'>ECOSUITE</span></h3>", unsafe_allow_html=True)

with nav_items:
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Home", use_container_width=True):
            st.switch_page("Home.py")
    with c2:
        st.button("Dashboard", type="primary", use_container_width=True)
    with c3:
        if st.button("Model Battle", use_container_width=True):
            st.switch_page("pages/2_Model_Battle.py")

st.markdown("<hr style='border:0; height:1px; background:rgba(255,255,255,0.15); margin:10px 0 25px 0;'>", unsafe_allow_html=True)

# --- DYNAMIC DATA LOADING ---
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)

    search_paths = [
        "air_quality_global.csv",
        "air_quality_global",
        os.path.join(parent_dir, "air_quality_global.csv"),
        os.path.join(parent_dir, "air_quality_global"),
        os.path.join(parent_dir, "data", "air_quality_global.csv"),
        "AQI_Data.csv",
        os.path.join(parent_dir, "AQI_Data.csv")
    ]

    possible_csvs = glob.glob(os.path.join(parent_dir, "**", "*.csv"), recursive=True)
    search_paths.extend(possible_csvs)

    for path in search_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                cols = {str(c).lower().strip(): c for c in df.columns}
                
                country_col = cols.get('country', 'Country')
                city_col = cols.get('city', 'City')
                aqi_col = cols.get('aqi value', cols.get('aqi_value', cols.get('aqi', 'AQI Value')))
                cat_col = cols.get('aqi category', cols.get('aqi_category', cols.get('category', 'AQI Category')))

                df.rename(columns={
                    country_col: 'Country', 
                    city_col: 'City', 
                    aqi_col: 'AQI Value',
                    cat_col: 'AQI Category'
                }, inplace=True)
                return df
            except Exception:
                continue

    return pd.DataFrame()

df = load_data()

# --- HEADER SECTION ---
st.markdown("## 📊 Global Air Quality Analytics")
st.caption("Filter by countries or cities to analyze detailed environmental metrics.")

if df.empty:
    st.error("⚠️ `air_quality_global.csv` read nahi ho saki. Apni file yahan upload karein:")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        cols = {str(c).lower().strip(): c for c in df.columns}
        country_col = cols.get('country', 'Country')
        city_col = cols.get('city', 'City')
        aqi_col = cols.get('aqi value', cols.get('aqi_value', cols.get('aqi', 'AQI Value')))
        cat_col = cols.get('aqi category', cols.get('aqi_category', cols.get('category', 'AQI Category')))
        df.rename(columns={
            country_col: 'Country', 
            city_col: 'City', 
            aqi_col: 'AQI Value',
            cat_col: 'AQI Category'
        }, inplace=True)
        st.rerun()

if not df.empty:
    # --- FILTERS SECTION ---
    st.markdown("### 🔍 Filter Locations & Countries")

    col_f1, col_f2 = st.columns(2)

    all_countries = sorted([str(c) for c in df['Country'].dropna().unique()])
    
    with col_f1:
        selected_countries = st.multiselect(
            "Select Countries (Leave blank for ALL countries):",
            options=all_countries,
            default=[]
        )

    if selected_countries:
        filtered_df = df[df['Country'].isin(selected_countries)]
    else:
        filtered_df = df.copy()

    available_cities = sorted([str(c) for c in filtered_df['City'].dropna().unique()])
    with col_f2:
        selected_cities = st.multiselect(
            "Select Cities:",
            options=available_cities,
            default=[]
        )

    if selected_cities:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

    # --- KPI COUNTERS ---
    st.write("")
    k1, k2, k3, k4 = st.columns(4)

    total_countries_count = filtered_df['Country'].nunique()
    total_cities_count = filtered_df['City'].nunique()
    avg_aqi = round(filtered_df['AQI Value'].mean(), 1) if not filtered_df.empty else 0
    max_aqi = filtered_df['AQI Value'].max() if not filtered_df.empty else 0

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_countries_count}</div>
            <div class="kpi-label">Active Countries</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_cities_count}</div>
            <div class="kpi-label">Monitored Cities</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_aqi}</div>
            <div class="kpi-label">Average AQI</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{max_aqi}</div>
            <div class="kpi-label">Max AQI Level</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("---")

    # --- MAP & MAIN CHARTS SECTION ---
    
    # 1. World Choropleth Map (Country Level Aggregation)
    st.markdown("### 🌐 Global Air Quality Map")
    country_aqi = filtered_df.groupby('Country', as_index=False)['AQI Value'].mean()
    
    fig_map = px.choropleth(
        country_aqi,
        locations="Country",
        locationmode="country names",
        color="AQI Value",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Reds,
        labels={'AQI Value': 'Avg AQI'}
    )
    fig_map.update_layout(
        template="plotly_dark",
        margin={"r":0,"t":0,"l":0,"b":0},
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.write("")

    # 2. TWO ANALYTICS CHARTS (Top Polluted Countries + Category Distribution)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("### 🚨 Top Most Polluted Countries")
        top_countries = (
            filtered_df.groupby("Country")["AQI Value"]
            .mean()
            .reset_index()
            .sort_values(by="AQI Value", ascending=False)
            .head(10)
        )
        fig_bar = px.bar(
            top_countries,
            x="AQI Value",
            y="Country",
            orientation="h",
            color="AQI Value",
            color_continuous_scale="Reds",
            text_auto=".0f"
        )
        fig_bar.update_layout(
            template="plotly_dark",
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=10, r=10, t=30, b=10),
            height=380,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        st.markdown("### 🟢 AQI Category Distribution")
        if 'AQI Category' in filtered_df.columns:
            cat_counts = filtered_df['AQI Category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            
            fig_pie = px.pie(
                cat_counts,
                names="Category",
                values="Count",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_layout(
                template="plotly_dark",
                margin=dict(l=10, r=10, t=30, b=10),
                height=380,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            # Fallback histogram if Category column doesn't exist
            fig_hist = px.histogram(
                filtered_df,
                x="AQI Value",
                nbins=20,
                color_discrete_sequence=['#ef4444']
            )
            fig_hist.update_layout(
                template="plotly_dark",
                height=380,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_hist, use_container_width=True)

    # --- DATA TABLE VIEW ---
    with st.expander("📋 View Complete Filtered Data Table"):
        display_cols = [c for c in ['Country', 'City', 'AQI Value', 'AQI Category'] if c in filtered_df.columns]
        if not display_cols:
            display_cols = filtered_df.columns
        st.dataframe(filtered_df[display_cols], use_container_width=True)