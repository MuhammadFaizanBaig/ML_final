import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Global AQI EcoSuite",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED UI & STYLING ---
st.markdown("""
<style>
    /* Streamlit default header aur sidebar hide karne ke liye */
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
        background: linear-gradient(180deg, rgba(11, 17, 32, 0.45) 0%, rgba(11, 17, 32, 0.70) 100%),
                    url('https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?auto=format&fit=crop&w=1920&q=80') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    .hero-banner {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.4) 0%, rgba(15, 23, 42, 0.85) 100%), 
                    url('https://images.unsplash.com/photo-1530587191325-3db32d826c18?auto=format&fit=crop&w=1000&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        padding: 45px 35px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.15;
        color: #ffffff;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #e2e8f0;
        margin-top: 15px;
        line-height: 1.6;
    }

    .module-card {
        background: rgba(15, 23, 42, 0.45);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 28px;
    }

    .status-badge {
        background: rgba(59, 130, 246, 0.3);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.5);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🚀 TOP NAVIGATION BAR (No Logout Button)
# ==========================================
nav_brand, nav_items = st.columns([2, 2.5])

with nav_brand:
    st.markdown("<h3 style='margin-top:8px; font-weight:800; letter-spacing:0.08em; color:#ffffff;'>AQI<span style='color:#3b82f6;'>ECOSUITE</span></h3>", unsafe_allow_html=True)

with nav_items:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("Home", type="primary", use_container_width=True)
    with c2:
        if st.button("Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py") # Agar yeh crash kare, to exact relative path istemal karein:
    with c3:
        if st.button("Model Battle", use_container_width=True):
            st.switch_page("pages/2_Model_Battle.py")

st.markdown("<hr style='border:0; height:1px; background:rgba(255,255,255,0.15); margin:10px 0 30px 0;'>", unsafe_allow_html=True)

# ==========================================
# 🌿 HERO BANNER SECTION
# ==========================================
st.markdown("""
<div class="hero-banner">
    <span class="status-badge">🟢 Global Atmospheric Intelligence Platform</span>
    <h1 class="hero-title" style="margin-top:20px;">Global Air Quality & Forecasting Intelligence</h1>
    <p class="hero-subtitle">
        Welcome to the command center. An advanced intelligence platform analyzing toxic air pollutants, PM2.5 trajectories, and predictive AQI forecasts across 23,000+ global cities.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ==========================================
# 📦 MODULE CARDS & NAVIGATION
# ==========================================
col_d, col_b = st.columns(2, gap="large")

with col_d:
    st.markdown("""
    <div class="module-card">
        <h3 style="color:#60a5fa; margin-top:0; font-weight:700;">📊 1. Global Analytics Dashboard</h3>
        <p style="color:#cbd5e1; font-size:14px; line-height:1.6;">
            Interactive global analytics tracking 23,000+ cities. Deep breakdown of primary air pollutants (PM2.5, NO₂, CO, O₃) with multi-country filtering.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Launch Dashboard →", key="btn_go_dash", type="primary", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

with col_b:
    st.markdown("""
    <div class="module-card">
        <h3 style="color:#c084fc; margin-top:0; font-weight:700;">⚔️ 2. Predictive Model Battle</h3>
        <p style="color:#cbd5e1; font-size:14px; line-height:1.6;">
            Real-time ML scenario simulation. Adjust chemical pollutant sliders and test 6 trained Machine Learning Regression models side-by-side.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Launch Model Battle →", key="btn_go_battle", type="primary", use_container_width=True):
        st.switch_page("pages/2_Model_Battle.py")