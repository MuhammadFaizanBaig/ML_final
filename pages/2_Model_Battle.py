import os
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Model Battle - AQI Intelligence",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED GLASSMORPHISM STYLING ---
st.markdown("""
<style>
    /* Hide Streamlit default sidebar and header */
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
    
    /* Custom Glass Panel */
    .glass-panel {
        background: rgba(15, 23, 42, 0.55);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .champion-badge {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(147, 51, 234, 0.3) 100%);
        border: 1px solid rgba(147, 51, 234, 0.5);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🚀 TOP NAVIGATION BAR
# ==========================================
nav_brand, nav_items = st.columns([2, 2.5])

with nav_brand:
    st.markdown("<h3 style='margin-top:8px; font-weight:800; color:#ffffff;'>AQI<span style='color:#3b82f6;'>ECOSUITE</span></h3>", unsafe_allow_html=True)

with nav_items:
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Home", use_container_width=True):
            st.switch_page("Home.py")
    with c2:
        if st.button("Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
    with c3:
        st.button("Model Battle", type="primary", use_container_width=True)

st.markdown("<hr style='border:0; height:1px; background:rgba(255,255,255,0.15); margin:10px 0 25px 0;'>", unsafe_allow_html=True)

# ==========================================
# 🧠 MODEL LOADING SYSTEM
# ==========================================
@st.cache_resource
def load_models_and_metrics():
    model_names = [
        "Linear Regression", "Ridge Regression", "Decision Tree", 
        "Random Forest", "AdaBoost", "Gradient Boosting"
    ]
    loaded_models = {}
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)

    # Search paths for models folder
    for name in model_names:
        formatted_name = name.lower().replace(' ', '_') + "_model.pkl"
        paths = [
            os.path.join("models", formatted_name),
            os.path.join(parent_dir, "models", formatted_name),
            formatted_name
        ]
        for p in paths:
            if os.path.exists(p):
                try:
                    loaded_models[name] = joblib.load(p)
                    break
                except Exception:
                    continue

    # Metrics file load
    metrics_paths = ["models/evaluation_metrics.pkl", os.path.join(parent_dir, "models/evaluation_metrics.pkl")]
    metrics = {}
    for mp in metrics_paths:
        if os.path.exists(mp):
            try:
                metrics = joblib.load(mp)
                break
            except Exception:
                continue

    return loaded_models, metrics

all_models, evaluation_metrics = load_models_and_metrics()

# Error handling if models missing
if not all_models:
    st.error("🚨 Models `.pkl` files detect nahi ho sakein! Baraye meherbani `models/` folder verify karein.")
    st.stop()

# ==========================================
# ⚔️ MAIN INTERFACE
# ==========================================
st.markdown("## ⚔️ The Battle of ML Regressors")
st.caption("Adjust chemical pollutant sliders on the left to see real-time AQI prediction responses across 6 ML algorithms.")

col_control, col_results = st.columns([1.1, 2], gap="large")

with col_control:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#60a5fa; margin-top:0;'>🎛️ Chemical Pollutant Sliders</h4>", unsafe_allow_html=True)
    st.write("Modify real-time atmospheric metrics:")
    
    co_val = st.slider("CO AQI Value", min_value=0, max_value=200, value=25)
    ozone_val = st.slider("Ozone AQI Value", min_value=0, max_value=200, value=35)
    no2_val = st.slider("NO2 AQI Value", min_value=0, max_value=200, value=15)
    pm25_val = st.slider("PM2.5 AQI Value", min_value=0, max_value=500, value=80)

    # DataFrame conversion
    input_data = pd.DataFrame([{
        'CO AQI Value': co_val,
        'Ozone AQI Value': ozone_val,
        'NO2 AQI Value': no2_val,
        'PM2.5 AQI Value': pm25_val
    }])
    st.markdown('</div>', unsafe_allow_html=True)

with col_results:
    battle_results = []
    
    for name, model in all_models.items():
        pred = model.predict(input_data)[0]
        model_metrics = evaluation_metrics.get(name, {"RMSE": None, "R2_Score": None})
        
        r2 = model_metrics.get('R2_Score') if isinstance(model_metrics, dict) else None
        rmse = model_metrics.get('RMSE') if isinstance(model_metrics, dict) else None
        
        battle_results.append({
            "ML Model Algorithm": name,
            "Predicted AQI": round(pred, 2),
            "Accuracy ($R^2$)": f"{r2 * 100:.1f}%" if r2 is not None else "N/A",
            "Error (RMSE)": round(rmse, 2) if rmse is not None else "N/A",
            "Raw_RMSE": rmse if rmse is not None else 999
        })
    
    results_df = pd.DataFrame(battle_results)
    
    # Sort by RMSE for lowest error rate
    results_df = results_df.sort_values(by="Raw_RMSE", ascending=True)
    
    # Top Performing Champion Model
    best_model_name = results_df.iloc[0]["ML Model Algorithm"]
    best_pred = results_df.iloc[0]["Predicted AQI"]

    st.markdown(f"""
    <div class="champion-badge">
        <span style="color:#a855f7; font-size:12px; font-weight:700; text-transform:uppercase;">🏆 Top Performing Algorithm</span>
        <h3 style="margin:5px 0 0 0; color:#ffffff;">{best_model_name} → <span style="color:#60a5fa;">{best_pred} AQI</span></h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Live Model Comparison Leaderboard")
    
    display_df = results_df.drop(columns=["Raw_RMSE"])
    st.dataframe(
        display_df, 
        use_container_width=True, 
        hide_index=True
    )

    st.write("")

    # Visual Comparison Bar Chart
    fig_comp = px.bar(
        results_df,
        x="ML Model Algorithm",
        y="Predicted AQI",
        color="Predicted AQI",
        text="Predicted AQI",
        color_continuous_scale="Purples",
        title="Real-Time Predicted AQI Comparison Across Models"
    )
    fig_comp.update_layout(
        template="plotly_dark",
        height=330,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_comp, use_container_width=True)