"""
AERIS - AQI Prediction View
Core interactive machine learning prediction interface using trained models.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from config import COLORS, get_category_info, POLLUTANT_INFO, calculate_sub_index, render_html
from components.cards import create_aqi_gauge, render_health_card

# Dynamic root directory resolution (works on Linux/Streamlit Cloud, Windows, Docker)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(BASE_DIR, "models")

@st.cache_resource
def load_trained_models():
    """Load serialized models from disk once and cache in memory."""
    models = {}
    model_files = {
        'Random Forest Regressor (Recommended)': 'random_forest.joblib',
        'Decision Tree Regressor': 'decision_tree.joblib',
        'Linear Regression': 'linear_regression.joblib'
    }
    
    # Check if models exist, if not auto-train on startup
    rf_path = os.path.join(MODELS_DIR, 'random_forest.joblib')
    if not os.path.exists(rf_path):
        try:
            if BASE_DIR not in sys.path:
                sys.path.insert(0, BASE_DIR)
            from train_models import train_and_evaluate
            train_and_evaluate()
        except Exception as e:
            st.error(f"Error initializing models: {e}")
            
    for label, fname in model_files.items():
        path = os.path.join(MODELS_DIR, fname)
        if os.path.exists(path):
            models[label] = joblib.load(path)
        else:
            st.warning(f"Model file missing: {fname}")
            
    return models

def render_prediction():
    models = load_trained_models()
    
    render_html("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; font-family: 'Poppins', sans-serif; font-size: 1.45rem; color: #12372A; font-weight: 700;">
            Predict Air Quality
        </h2>
        <p style="margin: 4px 0 0 0; color: #4A6258; font-size: 0.92rem;">
            Enter atmospheric pollutant measurements to estimate the Air Quality Index.
        </p>
    </div>
    """)
    
    # Presets Section
    with st.container(border=True):
        st.markdown("**⚡ Quick Scenario Presets:** Select an environmental benchmark to auto-populate parameters:")
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            if st.button("🌱 Clean Mountain Air", use_container_width=True):
                st.session_state['pred_pm25'] = 18.0
                st.session_state['pred_pm10'] = 35.0
                st.session_state['pred_no2'] = 15.0
                st.session_state['pred_so2'] = 8.0
                st.session_state['pred_co'] = 0.50
                st.session_state['pred_o3'] = 22.0
                st.rerun()
                
        with p2:
            if st.button("🏙️ Typical Urban Day", use_container_width=True):
                st.session_state['pred_pm25'] = 65.0
                st.session_state['pred_pm10'] = 140.0
                st.session_state['pred_no2'] = 45.0
                st.session_state['pred_so2'] = 18.0
                st.session_state['pred_co'] = 1.30
                st.session_state['pred_o3'] = 42.0
                st.rerun()
                
        with p3:
            if st.button("🌫️ Winter Stubble Smog", use_container_width=True):
                st.session_state['pred_pm25'] = 220.0
                st.session_state['pred_pm10'] = 380.0
                st.session_state['pred_no2'] = 85.0
                st.session_state['pred_so2'] = 32.0
                st.session_state['pred_co'] = 3.20
                st.session_state['pred_o3'] = 55.0
                st.rerun()
                
        with p4:
            if st.button("🏭 Heavy Industrial Belt", use_container_width=True):
                st.session_state['pred_pm25'] = 140.0
                st.session_state['pred_pm10'] = 290.0
                st.session_state['pred_no2'] = 120.0
                st.session_state['pred_so2'] = 95.0
                st.session_state['pred_co'] = 2.40
                st.session_state['pred_o3'] = 68.0
                st.rerun()

    # Form inputs & Model selection container
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    
    col_input, col_result = st.columns([1.1, 1.0], gap="large")
    
    with col_input:
        with st.container(border=True):
            st.markdown("### Atmospheric Pollutant Parameters")
            
            # Model selector dropdown
            available_model_names = list(models.keys())
            if not available_model_names:
                st.error("No ML models currently loaded. Please ensure training artifacts exist.")
                return
                
            selected_model_name = st.selectbox(
                "Select Machine Learning Engine:",
                available_model_names,
                index=0,
                help="Random Forest is the highest-accuracy ensemble model for non-linear CPCB breakpoints."
            )
            
            # Sliders with realistic bounds and session state defaults
            pm25 = st.slider(
                "PM2.5 — Fine Particulates (µg/m³)",
                min_value=1.0, max_value=500.0,
                value=float(st.session_state.get('pred_pm25', 68.0)),
                step=1.0,
                help="24h CPCB Standard: 60 µg/m³. Crucial driver of respiratory/cardiac index."
            )
            
            pm10 = st.slider(
                "PM10 — Coarse Particulates (µg/m³)",
                min_value=2.0, max_value=700.0,
                value=float(st.session_state.get('pred_pm10', 145.0)),
                step=1.0,
                help="24h CPCB Standard: 100 µg/m³. Road dust, construction debris, mechanical particles."
            )
            
            c_gas1, c_gas2 = st.columns(2)
            with c_gas1:
                no2 = st.slider(
                    "NO2 — Nitrogen Dioxide (µg/m³)",
                    min_value=1.0, max_value=300.0,
                    value=float(st.session_state.get('pred_no2', 42.0)),
                    step=1.0,
                    help="24h CPCB Standard: 80 µg/m³. Vehicular traffic and high-temp combustion."
                )
                
                so2 = st.slider(
                    "SO2 — Sulphur Dioxide (µg/m³)",
                    min_value=1.0, max_value=300.0,
                    value=float(st.session_state.get('pred_so2', 16.0)),
                    step=1.0,
                    help="24h CPCB Standard: 80 µg/m³. Thermal power generation and coal/crude combustion."
                )
                
            with c_gas2:
                co = st.slider(
                    "CO — Carbon Monoxide (mg/m³)",
                    min_value=0.1, max_value=30.0,
                    value=float(st.session_state.get('pred_co', 1.2)),
                    step=0.1,
                    help="8h CPCB Standard: 2.0 mg/m³. Incomplete vehicular fuel combustion."
                )
                
                o3 = st.slider(
                    "O3 — Ground-Level Ozone (µg/m³)",
                    min_value=1.0, max_value=300.0,
                    value=float(st.session_state.get('pred_o3', 38.0)),
                    step=1.0,
                    help="8h CPCB Standard: 100 µg/m³. Photochemical secondary pollutant."
                )
                
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            predict_clicked = st.button("🍃 PREDICT AQI", type="primary", use_container_width=True)
        
    with col_result:
        # Prediction execution
        active_model = models.get(selected_model_name)
        if active_model is None:
            st.error(f"Selected model '{selected_model_name}' could not be loaded.")
            return
            
        # Prepare feature vector
        features = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
        input_data = pd.DataFrame([[pm25, pm10, no2, so2, co, o3]], columns=features)
        
        # Calculate exact CPCB sub-indices for diagnostics
        sub_indices = {
            'PM2.5': calculate_sub_index(pm25, 'PM2.5'),
            'PM10': calculate_sub_index(pm10, 'PM10'),
            'NO2': calculate_sub_index(no2, 'NO2'),
            'SO2': calculate_sub_index(so2, 'SO2'),
            'CO': calculate_sub_index(co, 'CO'),
            'O3': calculate_sub_index(o3, 'O3')
        }
        dominant_p = max(sub_indices, key=sub_indices.get)
        
        # Predict using trained model
        raw_prediction = active_model.predict(input_data)[0]
        predicted_aqi = max(0.0, min(500.0, round(float(raw_prediction), 1)))
        
        cat_info = get_category_info(predicted_aqi)
        
        if predict_clicked:
            st.toast(f"AQI Predicted: {predicted_aqi:.1f} • {cat_info['name']}", icon="🍃")
        
        with st.container(border=True):
            render_html(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: {COLORS['forest']};">
                    Predicted Air Quality Assessment
                </span>
                <span style="background: {cat_info['color']}18; color: {cat_info['color']}; border: 1px solid {cat_info['color']}40; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">
                    {selected_model_name.split(' ')[0]} Engine
                </span>
            </div>
            """)
            
            # Semicircular Gauge Chart
            fig_gauge = create_aqi_gauge(predicted_aqi)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Dominant contributor identification
            render_html(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; background: {COLORS['bg_main']}; padding: 12px 16px; border-radius: 10px; border: 1px solid {COLORS['border']}; margin-top: 10px; margin-bottom: 12px;">
                <div>
                    <span style="font-size: 0.75rem; color: {COLORS['text_muted']}; text-transform: uppercase; font-weight: 600;">CPCB Category</span>
                    <div style="font-size: 1.15rem; font-weight: 700; color: {cat_info['color']}; display: flex; align-items: center; gap: 6px;">
                        <span>{cat_info['icon']}</span> {cat_info['name']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 0.75rem; color: {COLORS['text_muted']}; text-transform: uppercase; font-weight: 600;">Dominant Driver</span>
                    <div style="font-family: 'Poppins', sans-serif; font-size: 1.05rem; font-weight: 700; color: {COLORS['forest']};">
                        {dominant_p} <span style="font-size: 0.8rem; font-weight: 500; color: {COLORS['text_muted']};">({sub_indices[dominant_p]:.0f} Sub-Index)</span>
                    </div>
                </div>
            </div>
            """)
            
            # Sub-Index Badges
            pills_html = "".join([
                f"""<div style="text-align: center; background: #F4F8F4; padding: 6px; border-radius: 6px; border: 1px solid #E2EBE2;">
                    <div style="font-size: 0.68rem; color: {COLORS['text_muted']}; font-weight: 600;">{p}</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 700; color: {COLORS['forest']};">{val:.0f}</div>
                </div>""" for p, val in sub_indices.items()
            ])
            
            render_html(f"""
            <div>
                <div style="font-size: 0.72rem; color: {COLORS['text_muted']}; text-transform: uppercase; font-weight: 600; margin-bottom: 6px;">
                    Individual Pollutant Sub-Indices:
                </div>
                <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px;">
                    {pills_html}
                </div>
            </div>
            """)

    # Health Advisory Card
    render_html(render_health_card(cat_info))
    
    # Official Telemetry vs ML Estimate Disclaimer
    render_html(f"""
    <div style="background: #F9FAFB; border-radius: 10px; padding: 12px 16px; border: 1px dashed {COLORS['border']}; margin-top: 16px; display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 1.1rem;">ℹ️</span>
        <span style="font-size: 0.8rem; color: {COLORS['text_muted']}; line-height: 1.4;">
            <strong>Scientific Note:</strong> The index generated above represents an empirical estimate produced by the trained 
            <em>{selected_model_name}</em> model mapped against CPCB breakpoint standards. It does not replace certified Continuous Ambient Air Quality Monitoring Station (CAAQMS) official regulatory declarations.
        </span>
    </div>
    """)
