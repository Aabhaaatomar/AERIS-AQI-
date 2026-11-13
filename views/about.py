"""
AERIS - About Project View
System architecture, CPCB National Air Quality Index framework, methodology, and academic documentation.
"""

import streamlit as st
from config import COLORS, AQI_CATEGORIES, render_html

def render_about():
    render_html(f"""
    <div style="background: linear-gradient(135deg, {COLORS['forest']} 0%, #174A38 50%, {COLORS['emerald']} 100%); border-radius: 16px; padding: 30px; color: white; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(18,55,42,0.12);">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="font-size: 1.8rem;">🍃</span>
            <span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; color: {COLORS['mint']}; letter-spacing: 0.5px;">
                ACADEMIC ML CAPSTONE PROJECT
            </span>
        </div>
        <h1 style="margin: 0; font-family: 'Poppins', sans-serif; font-size: 2.2rem; font-weight: 700; color: #FFFFFF;">
            AERIS – Air Quality Intelligence System
        </h1>
        <p style="margin: 6px 0 0 0; font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; color: {COLORS['mint']}; font-weight: 500;">
            Understand the Air. Predict the Future.
        </p>
        <p style="margin: 14px 0 0 0; font-size: 0.95rem; color: rgba(255,255,255,0.85); max-width: 850px; line-height: 1.6;">
            A modern, production-grade environmental analytics dashboard engineered to predict the Indian Air Quality Index (AQI), 
            dissect criteria atmospheric pollutants, visualize multi-city environmental data, and benchmark supervised machine learning algorithms.
        </p>
    </div>
    """)
    
    # Section 1: CPCB National Air Quality Index Framework
    cat_cards_html = ""
    for cat in AQI_CATEGORIES:
        col = cat['color']
        cat_cards_html += f"""
        <div style="background: #F4F8F4; border-radius: 10px; padding: 14px; border-left: 4px solid {col}; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 700; color: {col}; font-size: 0.95rem;">
                    {cat['icon']} {cat['name']}
                </span>
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #12372A; font-size: 0.85rem; background: #FFFFFF; padding: 2px 8px; border-radius: 12px; border: 1px solid #E2EBE2;">
                    {cat['range'][0]}–{cat['range'][1]}
                </span>
            </div>
            <p style="margin: 0; font-size: 0.78rem; color: #4A6258; line-height: 1.4;">
                {cat['summary']}
            </p>
        </div>
        """
        
    with st.container(border=True):
        st.markdown("### 1. Indian CPCB NAQI Classification Framework")
        st.markdown("The Central Pollution Control Board (CPCB) of India defines the National Air Quality Index (NAQI) using a 6-tier classification standard. AERIS strictly conforms to these official Indian categories rather than US EPA standards:")
        render_html(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-top: 10px;">
            {cat_cards_html}
        </div>
        """)
    
    # Section 2: Technical Architecture
    with st.container(border=True):
        st.markdown("### 2. System Architecture & ML Pipeline")
        render_html(f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 10px;">
            <div style="background: {COLORS['bg_main']}; border-radius: 10px; padding: 16px; border-top: 3px solid {COLORS['forest']};">
                <div style="font-size: 1.3rem; margin-bottom: 6px;">📡</div>
                <h4 style="margin: 0 0 4px 0; font-size: 0.9rem; color: {COLORS['forest']};">1. Telemetry Ingestion</h4>
                <p style="margin: 0; font-size: 0.78rem; color: {COLORS['text_secondary']}; line-height: 1.4;">
                    Multi-city CPCB ambient sensor data (PM2.5, PM10, NO2, SO2, CO, O3) covering multi-seasonal Indian meteorology.
                </p>
            </div>
            <div style="background: {COLORS['bg_main']}; border-radius: 10px; padding: 16px; border-top: 3px solid {COLORS['emerald']};">
                <div style="font-size: 1.3rem; margin-bottom: 6px;">⚙️</div>
                <h4 style="margin: 0 0 4px 0; font-size: 0.9rem; color: {COLORS['forest']};">2. Sub-Index Engine</h4>
                <p style="margin: 0; font-size: 0.78rem; color: {COLORS['text_secondary']}; line-height: 1.4;">
                    Rigorous piecewise linear sub-index computation for individual criteria pollutants and composite max-operator calculation.
                </p>
            </div>
            <div style="background: {COLORS['bg_main']}; border-radius: 10px; padding: 16px; border-top: 3px solid {COLORS['mint']};">
                <div style="font-size: 1.3rem; margin-bottom: 6px;">🧠</div>
                <h4 style="margin: 0 0 4px 0; font-size: 0.9rem; color: {COLORS['forest']};">3. Model Training & Serialization</h4>
                <p style="margin: 0; font-size: 0.78rem; color: {COLORS['text_secondary']}; line-height: 1.4;">
                    Linear Regression, Decision Tree, and Random Forest models trained, evaluated with 4 metrics, and saved via Joblib.
                </p>
            </div>
            <div style="background: {COLORS['bg_main']}; border-radius: 10px; padding: 16px; border-top: 3px solid #16A34A;">
                <div style="font-size: 1.3rem; margin-bottom: 6px;">💻</div>
                <h4 style="margin: 0 0 4px 0; font-size: 0.9rem; color: {COLORS['forest']};">4. Environmental SaaS UI</h4>
                <p style="margin: 0; font-size: 0.78rem; color: {COLORS['text_secondary']}; line-height: 1.4;">
                    High-performance Streamlit frontend with Plotly charts, interactive prediction simulator, and advisory dashboards.
                </p>
            </div>
        </div>
        """)
    
    # Section 3: Technology Stack & Academic Credits
    col_tech, col_cred = st.columns([1.2, 1.0])
    
    with col_tech:
        with st.container(border=True):
            st.markdown("#### 🛠️ Technology Stack")
            st.markdown("""
            - **Application Framework:** Streamlit (Python)
            - **Interactive Visualization:** Plotly Graph Objects & Plotly Express
            - **Machine Learning:** Scikit-Learn (LinearRegression, DecisionTreeRegressor, RandomForestRegressor)
            - **Model Serialization:** Joblib (zero-latency in-memory cached deployment)
            - **Data Processing:** Pandas & NumPy
            - **Typography & Styling:** Poppins, Manrope, Inter, Space Grotesk via Custom CSS
            """)
        
    with col_cred:
        with st.container(border=True):
            st.markdown("#### 🎓 Academic Project Statement")
            st.markdown("""
            This project was created for an Academic Machine Learning course requirement, built to production-grade SaaS standards. 
            All performance metrics (MAE, RMSE, R²) represent empirical results computed on an independent 20% test partition.
            """)
            render_html(f"""
            <div style="background: {COLORS['bg_main']}; padding: 12px; border-radius: 8px; font-size: 0.8rem; color: {COLORS['text_muted']}; border: 1px dashed {COLORS['border']};">
                <strong>Project:</strong> AERIS – Air Quality Intelligence System<br>
                <strong>License:</strong> Academic Open-Source Educational Use
            </div>
            """)
