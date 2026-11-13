"""
AERIS - UI Card Components
Custom styled HTML/CSS metric cards, badges, and Plotly gauge components
"""

import streamlit as st
import plotly.graph_objects as go
from config import COLORS, AQI_CATEGORIES, get_category_info

def render_stat_card(label, value, icon, unit="", delta=None, delta_text=""):
    """Render a premium environmental metric card."""
    delta_html = ""
    if delta is not None:
        delta_color = "#16A34A" if delta < 0 else "#DC2626"
        arrow = "↓" if delta < 0 else "↑"
        delta_html = f"""
        <div style="font-size: 0.78rem; color: {delta_color}; font-weight: 600; margin-top: 4px; display: flex; align-items: center; gap: 4px;">
            <span>{arrow} {abs(delta)}%</span>
            <span style="color: {COLORS['text_muted']}; font-weight: 480;">{delta_text}</span>
        </div>
        """
        
    html = f"""
    <div style="
        background: {COLORS['bg_card']};
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 2px 10px rgba(18, 55, 42, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 110px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: {COLORS['text_secondary']};">
                {label}
            </span>
            <div style="
                width: 34px;
                height: 34px;
                border-radius: 10px;
                background: {COLORS['bg_secondary']};
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1rem;
            ">
                {icon}
            </div>
        </div>
        <div>
            <div style="display: flex; align-items: baseline; gap: 6px;">
                <span style="font-family: 'Space Grotesk', Inter, sans-serif; font-size: 1.85rem; font-weight: 700; color: {COLORS['text_primary']};">
                    {value}
                </span>
                <span style="font-size: 0.85rem; font-weight: 500; color: {COLORS['text_muted']};">
                    {unit}
                </span>
            </div>
            {delta_html}
        </div>
    </div>
    """
    return html

def create_aqi_gauge(aqi_val):
    """Create an elegant semicircular Indian AQI gauge with official color segments."""
    val = float(aqi_val)
    cat_info = get_category_info(val)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>{cat_info['name'].upper()} AIR QUALITY</b>", 'font': {'size': 14, 'color': cat_info['color'], 'family': 'Poppins, sans-serif'}},
        number={'suffix': " AQI", 'font': {'size': 36, 'color': COLORS['forest'], 'family': 'Space Grotesk, sans-serif'}},
        gauge={
            'axis': {'range': [0, 500], 'tickwidth': 1.5, 'tickcolor': COLORS['text_muted'], 'tickvals': [0, 50, 100, 200, 300, 400, 500]},
            'bar': {'color': cat_info['color'], 'thickness': 0.28},
            'bgcolor': "white",
            'borderwidth': 1.5,
            'bordercolor': COLORS['border'],
            'steps': [
                {'range': [0, 50], 'color': '#D1FAE5'},      # Good (soft mint)
                {'range': [50, 100], 'color': '#ECFCCB'},    # Satisfactory
                {'range': [100, 200], 'color': '#FEF9C3'},   # Moderate
                {'range': [200, 300], 'color': '#FFEDD5'},   # Poor
                {'range': [300, 400], 'color': '#FEE2E2'},   # Very Poor
                {'range': [400, 500], 'color': '#FFE4E6'}    # Severe
            ],
            'threshold': {
                'line': {'color': COLORS['forest'], 'width': 4},
                'thickness': 0.75,
                'value': val
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=270,
        margin=dict(l=25, r=25, t=40, b=15),
        font={'family': "Inter, sans-serif"}
    )
    return fig

def render_category_pill(category_name, aqi_val=None):
    """Render a styled category indicator badge."""
    cat_dict = next((c for c in AQI_CATEGORIES if c['name'].lower() == category_name.lower()), AQI_CATEGORIES[0])
    color = cat_dict['color']
    icon = cat_dict['icon']
    
    val_str = f" • {aqi_val:.0f} AQI" if aqi_val is not None else ""
    
    return f"""
    <span style="
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: {color}15;
        border: 1px solid {color}40;
        color: {color};
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    ">
        <span>{icon}</span>
        <span>{cat_dict['name']}{val_str}</span>
    </span>
    """

def render_health_card(cat_info):
    """Render full health advisory card based on predicted or observed AQI."""
    color = cat_info['color']
    return f"""
    <div style="
        background: #FFFFFF;
        border-radius: 14px;
        border: 1px solid {color}30;
        box-shadow: 0 4px 16px {color}12;
        padding: 22px;
        margin-top: 14px;
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid {COLORS['border']}; padding-bottom: 12px; margin-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.6rem;">{cat_info['icon']}</span>
                <div>
                    <h4 style="margin: 0; color: {COLORS['forest']}; font-family: 'Poppins', sans-serif; font-size: 1.1rem; font-weight: 600;">
                        {cat_info['name']} Air Quality Advisory
                    </h4>
                    <span style="font-size: 0.8rem; color: {COLORS['text_muted']};">Based on Central Pollution Control Board (CPCB) Standard Guidelines</span>
                </div>
            </div>
            <div style="background: {color}15; border: 1px solid {color}40; color: {color}; padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
                Range: {cat_info['range'][0]} - {cat_info['range'][1]} AQI
            </div>
        </div>

        <p style="color: {COLORS['text_secondary']}; font-size: 0.92rem; line-height: 1.5; margin-bottom: 14px;">
            {cat_info['summary']}
        </p>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px;">
            <div style="background: {COLORS['bg_main']}; padding: 14px; border-radius: 10px; border-left: 3px solid {color};">
                <div style="font-weight: 600; font-size: 0.85rem; color: {COLORS['forest']}; margin-bottom: 4px; display: flex; align-items: center; gap: 5px;">
                    <span>👥</span> General Population
                </div>
                <div style="font-size: 0.82rem; color: {COLORS['text_secondary']}; line-height: 1.45;">
                    {cat_info['general_advisory']}
                </div>
            </div>
            <div style="background: {COLORS['bg_main']}; padding: 14px; border-radius: 10px; border-left: 3px solid #EAB308;">
                <div style="font-weight: 600; font-size: 0.85rem; color: {COLORS['forest']}; margin-bottom: 4px; display: flex; align-items: center; gap: 5px;">
                    <span>🩺</span> Sensitive Groups (Asthma, Elderly, Kids)
                </div>
                <div style="font-size: 0.82rem; color: {COLORS['text_secondary']}; line-height: 1.45;">
                    {cat_info['sensitive_advisory']}
                </div>
            </div>
        </div>

        <div style="background: {COLORS['bg_secondary']}; padding: 12px 16px; border-radius: 8px; display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.2rem;">💡</span>
            <div>
                <strong style="color: {COLORS['forest']}; font-size: 0.85rem;">Recommended Protective Action:</strong>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.85rem; margin-left: 6px;">{cat_info['action']}</span>
            </div>
        </div>
    </div>
    """
