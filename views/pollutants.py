"""
AERIS - Pollutant Insights View
Detailed scientific breakdown of key atmospheric criteria pollutants under Indian NAQI.
"""

import streamlit as st
import plotly.graph_objects as go
from config import COLORS, POLLUTANT_INFO, CPCB_BREAKPOINTS, apply_aeris_theme, render_html

def render_pollutants(df):
    render_html("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; font-family: 'Poppins', sans-serif; font-size: 1.45rem; color: #12372A; font-weight: 700;">
            Pollutant Chemical Profiles & Environmental Insights
        </h2>
        <p style="margin: 4px 0 0 0; color: #4A6258; font-size: 0.92rem;">
            Deep-dive into the physical chemistry, emissions vectors, epidemiological effects, and regulatory thresholds.
        </p>
    </div>
    """)
    
    pollutant_keys = list(POLLUTANT_INFO.keys())
    
    # Custom pill selector
    selected_p = st.selectbox(
        "Select Criteria Pollutant to Inspect:",
        pollutant_keys,
        index=0
    )
    
    info = POLLUTANT_INFO[selected_p]
    
    # Header Card for Pollutant
    render_html(f"""
    <div style="background: linear-gradient(135deg, {COLORS['forest']} 0%, #1B4D3E 100%); border-radius: 14px; padding: 22px 26px; color: white; margin-bottom: 20px; box-shadow: 0 4px 14px rgba(18,55,42,0.08);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="background: rgba(255,255,255,0.18); padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; color: {COLORS['mint']};">
                    CRITERIA AIR POLLUTANT
                </span>
                <h2 style="margin: 6px 0 0 0; font-family: 'Poppins', sans-serif; font-size: 1.6rem; color: #FFFFFF;">
                    {info['name']}
                </h2>
            </div>
            <div style="background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.22); border-radius: 10px; padding: 10px 18px; text-align: right;">
                <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; color: {COLORS['mint']}; font-weight: 600;">CPCB Safe Threshold</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 700; color: #FFFFFF;">{info['safe_limit_24h']}</div>
            </div>
        </div>
        <p style="margin: 14px 0 0 0; font-size: 0.92rem; color: rgba(255,255,255,0.88); line-height: 1.55;">
            {info['description']}
        </p>
    </div>
    """)
    
    # 2 Columns: Sources & Health Impacts
    col_left, col_right = st.columns(2)
    
    with col_left:
        render_html(f"""
        <div style="background: #FFFFFF; border-radius: 14px; padding: 20px; border: 1px solid #E2EBE2; box-shadow: 0 2px 10px rgba(18,55,42,0.03); height: 100%;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                <span style="font-size: 1.3rem;">🏭</span>
                <h4 style="margin: 0; color: {COLORS['forest']}; font-family: 'Poppins', sans-serif; font-size: 1.05rem;">
                    Primary Emission Sources
                </h4>
            </div>
            <p style="color: {COLORS['text_secondary']}; font-size: 0.88rem; line-height: 1.55; margin-bottom: 14px;">
                {info['primary_sources']}
            </p>
            <div style="background: {COLORS['bg_main']}; padding: 12px; border-radius: 8px; font-size: 0.8rem; color: {COLORS['text_muted']};">
                <strong>Chemical & Physical Dynamics:</strong><br>{info['chemical_nature']}
            </div>
        </div>
        """)
        
    with col_right:
        render_html(f"""
        <div style="background: #FFFFFF; border-radius: 14px; padding: 20px; border: 1px solid #E2EBE2; box-shadow: 0 2px 10px rgba(18,55,42,0.03); height: 100%;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                <span style="font-size: 1.3rem;">🫁</span>
                <h4 style="margin: 0; color: {COLORS['forest']}; font-family: 'Poppins', sans-serif; font-size: 1.05rem;">
                    Physiological & Health Consequences
                </h4>
            </div>
            <p style="color: {COLORS['text_secondary']}; font-size: 0.88rem; line-height: 1.55; margin-bottom: 14px;">
                {info['health_impacts']}
            </p>
            <div style="background: {COLORS['bg_secondary']}; padding: 12px; border-radius: 8px; font-size: 0.8rem; color: {COLORS['forest']}; font-weight: 500;">
                <strong>Regulatory Exposure Monitoring:</strong> Regular continuous sampling is mandatory under CPCB National Ambient Air Quality Standards (NAAQS).
            </div>
        </div>
        """)
        
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # Dataset Distribution Chart for selected pollutant
    with st.container(border=True):
        p_series = df[selected_p]
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=p_series,
            nbinsx=40,
            marker=dict(color=COLORS['emerald'], line=dict(color=COLORS['forest'], width=1)),
            hovertemplate=f'{selected_p}: %{{x}} {info["unit"]}<br>Count: %{{y}} days<extra></extra>'
        ))
        
        mean_val = p_series.mean()
        median_val = p_series.median()
        fig_hist.add_vline(x=mean_val, line_dash="dash", line_color=COLORS['forest'], line_width=2, annotation_text=f"Mean: {mean_val:.1f} {info['unit']}", annotation_position="top right")
        fig_hist.add_vline(x=median_val, line_dash="dot", line_color=COLORS['aqi_poor'], line_width=1.5, annotation_text=f"Median: {median_val:.1f} {info['unit']}", annotation_position="top left")
        
        fig_hist.update_layout(
            title=f"<b>Empirical Concentration Distribution: {selected_p} Across Dataset Observations</b>",
            xaxis_title=f"{info['name']} ({info['unit']})",
            yaxis_title="Observation Days",
            bargap=0.04
        )
        st.plotly_chart(apply_aeris_theme(fig_hist), use_container_width=True)
    
    # CPCB Breakpoints Table for this pollutant
    breakpoints = CPCB_BREAKPOINTS[selected_p]
    categories = ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe']
    cat_colors = [COLORS['aqi_good'], COLORS['aqi_satisfactory'], COLORS['aqi_moderate'], COLORS['aqi_poor'], COLORS['aqi_very_poor'], COLORS['aqi_severe']]
    
    table_rows = ""
    for idx, (b_low, b_high, i_low, i_high) in enumerate(breakpoints):
        cat_name = categories[idx]
        col = cat_colors[idx]
        table_rows += f"""
        <tr style="border-bottom: 1px solid #E2EBE2;">
            <td style="padding: 10px 14px; font-weight: 600; color: {col};">
                <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: {col}; margin-right: 8px;"></span>
                {cat_name}
            </td>
            <td style="padding: 10px 14px; font-family: 'Space Grotesk', sans-serif; font-weight: 600; color: {COLORS['text_primary']};">
                {b_low} – {b_high} {info['unit']}
            </td>
            <td style="padding: 10px 14px; font-family: 'Space Grotesk', sans-serif; color: {COLORS['forest']}; font-weight: 700;">
                {i_low} – {i_high}
            </td>
        </tr>
        """
        
    with st.container(border=True):
        st.markdown(f"#### Official CPCB Breakpoint Grid for {selected_p}")
        render_html(f"""
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.88rem;">
            <thead>
                <tr style="background: {COLORS['bg_main']}; border-bottom: 2px solid {COLORS['border']};">
                    <th style="padding: 10px 14px; color: {COLORS['forest']};">AQI Category</th>
                    <th style="padding: 10px 14px; color: {COLORS['forest']};">{selected_p} Concentration Range ({info['unit']})</th>
                    <th style="padding: 10px 14px; color: {COLORS['forest']};">Resulting Sub-Index Range</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """)
