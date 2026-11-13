"""
AERIS - Model Performance View
Evaluates Linear Regression, Decision Tree, and Random Forest Regressors using actual training telemetry.
"""

import json
import os
import pandas as pd
import streamlit as st
from config import COLORS, render_html
from components.cards import render_stat_card
from components.charts import (
    plot_model_comparison_bar,
    plot_actual_vs_predicted,
    plot_residual_distribution,
    plot_feature_importance
)

METRICS_PATH = r"C:\Users\tomar\.gemini\antigravity\scratch\aeris_aqi_system\models\model_metrics.json"
EVAL_DATA_PATH = r"C:\Users\tomar\.gemini\antigravity\scratch\aeris_aqi_system\models\test_evaluation_data.csv"

@st.cache_data
def load_performance_data():
    if not os.path.exists(METRICS_PATH) or not os.path.exists(EVAL_DATA_PATH):
        st.error("Model metrics or evaluation dataset not found. Please run train_models.py.")
        return None, None
        
    with open(METRICS_PATH, 'r') as f:
        metrics_data = json.load(f)
        
    eval_df = pd.read_csv(EVAL_DATA_PATH)
    return metrics_data, eval_df

def render_model_performance():
    metrics_data, eval_df = load_performance_data()
    if not metrics_data:
        return
        
    render_html("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; font-family: 'Poppins', sans-serif; font-size: 1.45rem; color: #12372A; font-weight: 700;">
            Machine Learning Model Performance & Validation
        </h2>
        <p style="margin: 4px 0 0 0; color: #4A6258; font-size: 0.92rem;">
            Empirical evaluation of Linear Regression, Decision Tree, and Random Forest Regressors on unseen test data.
        </p>
    </div>
    """)
    
    # Top KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_html(render_stat_card(
            label="Optimal Model",
            value=metrics_data['best_model'],
            icon="🏆",
            unit="Selected"
        ))
    with c2:
        rf_mae = metrics_data['metrics']['Random Forest']['MAE']
        render_html(render_stat_card(
            label="Lowest MAE",
            value=f"{rf_mae:.2f}",
            icon="🎯",
            unit="AQI Points"
        ))
    with c3:
        rf_r2 = metrics_data['metrics']['Random Forest']['R2']
        render_html(render_stat_card(
            label="Peak R² Score",
            value=f"{rf_r2:.4f}",
            icon="📈",
            unit="Variance Exp."
        ))
    with c4:
        render_html(render_stat_card(
            label="Test Evaluation Set",
            value=f"{metrics_data['test_samples']:,}",
            icon="🧪",
            unit="Instances"
        ))
        
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # Official Comparison Table
    table_rows = ""
    for model_name, m in metrics_data['metrics'].items():
        is_best = (model_name == metrics_data['best_model'])
        badge = """<span style="background: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; margin-left: 8px;">★ OPTIMAL</span>""" if is_best else ""
        bg_style = "background: #F4F8F4; font-weight: 600;" if is_best else ""
        
        table_rows += f"""
        <tr style="border-bottom: 1px solid #E2EBE2; {bg_style}">
            <td style="padding: 12px 16px; color: {COLORS['forest']};">
                <strong>{model_name}</strong> {badge}
            </td>
            <td style="padding: 12px 16px; font-family: 'Space Grotesk', sans-serif; color: {COLORS['text_primary']};">{m['MAE']:.3f}</td>
            <td style="padding: 12px 16px; font-family: 'Space Grotesk', sans-serif; color: {COLORS['text_primary']};">{m['MSE']:.3f}</td>
            <td style="padding: 12px 16px; font-family: 'Space Grotesk', sans-serif; color: {COLORS['text_primary']};">{m['RMSE']:.3f}</td>
            <td style="padding: 12px 16px; font-family: 'Space Grotesk', sans-serif; color: {COLORS['forest']}; font-weight: 700;">{m['R2']:.4f}</td>
        </tr>
        """
        
    with st.container(border=True):
        st.markdown("### Comprehensive Model Evaluation Benchmark")
        render_html(f"""
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.88rem;">
            <thead>
                <tr style="background: {COLORS['bg_secondary']}; border-bottom: 2px solid {COLORS['border']};">
                    <th style="padding: 12px 16px; color: {COLORS['forest']};">Machine Learning Model</th>
                    <th style="padding: 12px 16px; color: {COLORS['forest']};">Mean Absolute Error (MAE)</th>
                    <th style="padding: 12px 16px; color: {COLORS['forest']};">Mean Squared Error (MSE)</th>
                    <th style="padding: 12px 16px; color: {COLORS['forest']};">Root Mean Squared Error (RMSE)</th>
                    <th style="padding: 12px 16px; color: {COLORS['forest']};">R² Determination Score</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """)
    
    # Model Error Bar Chart
    with st.container(border=True):
        fig_comp = plot_model_comparison_bar(metrics_data['metrics'])
        st.plotly_chart(fig_comp, use_container_width=True)
    
    # Interactive Model Inspection for Scatter & Residuals
    with st.container(border=True):
        st.markdown("### Diagnostic Error & Residual Diagnostics")
        inspect_model = st.radio(
            "Select Model to Inspect in Diagnostics:",
            ["Random Forest", "Decision Tree", "Linear Regression"],
            horizontal=True,
            index=0
        )
        
        model_key_map = {
            "Random Forest": "random_forest",
            "Decision Tree": "decision_tree",
            "Linear Regression": "linear_regression"
        }
        active_key = model_key_map[inspect_model]
        
        col_act, col_res = st.columns(2)
        with col_act:
            fig_act = plot_actual_vs_predicted(eval_df, active_key)
            st.plotly_chart(fig_act, use_container_width=True)
        with col_res:
            fig_res = plot_residual_distribution(eval_df, active_key)
            st.plotly_chart(fig_res, use_container_width=True)
    
    # Feature Importance and Academic Discussion
    col_fi, col_synth = st.columns([1.1, 1.2])
    
    with col_fi:
        with st.container(border=True):
            fi_features = metrics_data['feature_analysis']['features']
            fi_importances = metrics_data['feature_analysis']['rf_importances']
            fig_fi = plot_feature_importance(fi_features, fi_importances)
            st.plotly_chart(fig_fi, use_container_width=True)
        
    with col_synth:
        with st.container(border=True):
            render_html(f"""
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 1.3rem;">🧠</span>
                    <h4 style="margin: 0; color: {COLORS['forest']}; font-family: 'Poppins', sans-serif; font-size: 1.05rem;">
                        Academic Machine Learning Discussion
                    </h4>
                </div>
                <div style="color: {COLORS['text_secondary']}; font-size: 0.86rem; line-height: 1.55;">
                    <p style="margin-top: 0;">
                        <strong>Why Tree Ensembles Dominate Linear Models on AQI:</strong><br>
                        The official Central Pollution Control Board (CPCB) Indian National Air Quality Index is mathematically formulated as:
                    </p>
                    <div style="background: {COLORS['bg_main']}; padding: 8px 12px; border-radius: 6px; font-family: 'Space Grotesk', monospace; font-size: 0.85rem; color: {COLORS['forest']}; margin-bottom: 10px;">
                        AQI = max(I_PM2.5, I_PM10, I_NO2, I_SO2, I_CO, I_O3)
                    </div>
                    <p>
                        Each sub-index <em>I_p</em> is itself a <strong>piecewise-linear step function</strong> with distinct slope changes at each regulatory threshold.
                    </p>
                    <ul style="padding-left: 18px; margin-bottom: 10px;">
                        <li><strong>Linear Regression (MAE ~18.58, R² ~0.945):</strong> Constrained by its global linearity assumption. It cannot represent the non-linear <code>max()</code> selection operator or piecewise slope inflections, producing systematic residual bias at boundary transitions.</li>
                        <li><strong>Random Forest (MAE ~0.19, R² ~1.000):</strong> As an ensemble of orthogonal decision partitions, it creates precise hyper-rectangular decision boundaries that cleanly replicate the piecewise <code>max()</code> function, achieving near-perfect predictive fidelity.</li>
                    </ul>
                </div>
            </div>
            """)
