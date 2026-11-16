"""
AERIS 2.0 - UI Card Components
Theme-aware HTML/CSS metric cards, badges, and Plotly gauge components
Ensures 100% contrast readability across Light, Dark, and Cream themes.
"""

import streamlit as st
import plotly.graph_objects as go
from config import AQI_CATEGORIES, get_category_info, render_html
from utils.theme_manager import get_theme_colors

def clean_html_str(raw_html):
    """Clean HTML string so Markdown never converts indented lines into code blocks."""
    return "\n".join(line.strip() for line in raw_html.splitlines() if line.strip())

def render_stat_card(label, value, icon, unit="", delta=None, delta_text=""):
    """Render a premium environmental metric card with full theme awareness."""
    t = get_theme_colors()
    
    delta_html = ""
    if delta is not None:
        delta_color = "#16A34A" if delta < 0 else "#DC2626"
        arrow = "↓" if delta < 0 else "↑"
        delta_html = f"""
        <div style="font-size: 0.78rem; color: {delta_color}; font-weight: 600; margin-top: 4px; display: flex; align-items: center; gap: 4px;">
            <span>{arrow} {abs(delta)}%</span>
            <span style="color: {t['text_muted']}; font-weight: 480;">{delta_text}</span>
        </div>
        """
        
    html = f"""
    <div style="background: {t['bg_card']}; border-radius: 14px; padding: 18px 20px; border: 1px solid {t['border']}; box-shadow: {t['card_shadow']}; display: flex; flex-direction: column; justify-content: space-between; min-height: 110px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: {t['text_secondary']};">
                {label}
            </span>
            <div style="width: 36px; height: 36px; border-radius: 10px; background: {t['bg_secondary']}; display: flex; align-items: center; justify-content: center; font-size: 1.15rem; border: 1px solid {t['border']};">
                {icon}
            </div>
        </div>
        <div>
            <div style="display: flex; align-items: baseline; gap: 6px;">
                <span style="font-family: 'Space Grotesk', Inter, sans-serif; font-size: 1.85rem; font-weight: 700; color: {t['text_primary']};">
                    {value}
                </span>
                <span style="font-size: 0.82rem; font-weight: 600; color: {t['text_muted']};">
                    {unit}
                </span>
            </div>
            {delta_html}
        </div>
    </div>
    """
    return clean_html_str(html)

def create_aqi_gauge(aqi_val):
    """Create an elegant semicircular Indian AQI gauge with official color segments and theme-aware text."""
    t = get_theme_colors()
    val = float(aqi_val)
    cat_info = get_category_info(val)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>{cat_info['name'].upper()} AIR QUALITY</b>", 'font': {'size': 14, 'color': cat_info['color'], 'family': 'Manrope, sans-serif'}},
        number={'suffix': " AQI", 'font': {'size': 36, 'color': t['text_primary'], 'family': 'Space Grotesk, sans-serif'}},
        gauge={
            'axis': {
                'range': [0, 500], 
                'tickwidth': 1.5, 
                'tickcolor': t['text_muted'], 
                'tickvals': [0, 50, 100, 200, 300, 400, 500],
                'tickfont': {'color': t['text_secondary'], 'size': 10}
            },
            'bar': {'color': cat_info['color'], 'thickness': 0.28},
            'bgcolor': t['bg_card'],
            'borderwidth': 1.5,
            'bordercolor': t['border'],
            'steps': [
                {'range': [0, 50], 'color': '#D1FAE5'},      # Good (mint)
                {'range': [50, 100], 'color': '#ECFCCB'},    # Satisfactory
                {'range': [100, 200], 'color': '#FEF9C3'},   # Moderate
                {'range': [200, 300], 'color': '#FFEDD5'},   # Poor
                {'range': [300, 400], 'color': '#FEE2E2'},   # Very Poor
                {'range': [400, 500], 'color': '#FFE4E6'}    # Severe
            ],
            'threshold': {
                'line': {'color': t['primary'], 'width': 4},
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
        font={'family': "Inter, sans-serif", 'color': t['text_primary']}
    )
    return fig

def render_category_pill(category_name, aqi_val=None):
    """Render a styled category indicator badge."""
    t = get_theme_colors()
    cat_dict = next((c for c in AQI_CATEGORIES if c['name'].lower() == category_name.lower()), AQI_CATEGORIES[0])
    color = cat_dict['color']
    icon = cat_dict['icon']
    
    val_str = f" • {aqi_val:.0f} AQI" if aqi_val is not None else ""
    
    html = f"""
    <span style="display: inline-flex; align-items: center; gap: 6px; background: {color}18; border: 1px solid {color}50; color: {color}; padding: 4px 12px; border-radius: 999px; font-size: 0.82rem; font-weight: 700; letter-spacing: 0.3px;">
        <span>{icon}</span>
        <span>{cat_dict['name']}{val_str}</span>
    </span>
    """
    return clean_html_str(html)

def render_health_card(cat_info):
    """Render full health advisory card with theme-aware styling and high-contrast text."""
    t = get_theme_colors()
    color = cat_info['color']
    
    html = f"""
    <div style="background: {t['bg_card']}; border-radius: 14px; border: 1px solid {color}40; box-shadow: {t['card_shadow']}; padding: 22px; margin-top: 14px;">
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid {t['border']}; padding-bottom: 12px; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.6rem;">{cat_info['icon']}</span>
                <div>
                    <h4 style="margin: 0; color: {t['text_primary']}; font-family: 'Manrope', sans-serif; font-size: 1.1rem; font-weight: 700;">
                        {cat_info['name']} Air Quality Advisory
                    </h4>
                    <span style="font-size: 0.8rem; color: {t['text_secondary']};">Central Pollution Control Board (CPCB) Standard Guidelines</span>
                </div>
            </div>
            <div style="background: {color}18; border: 1px solid {color}50; color: {color}; padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
                Range: {cat_info['range'][0]} - {cat_info['range'][1]} AQI
            </div>
        </div>

        <p style="color: {t['text_primary']}; font-size: 0.92rem; line-height: 1.5; margin-bottom: 14px;">
            {cat_info['summary']}
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-bottom: 14px;">
            <div style="background: {t['bg_secondary']}; padding: 14px; border-radius: 10px; border-left: 3px solid {color}; border: 1px solid {t['border']};">
                <div style="font-weight: 700; font-size: 0.86rem; color: {t['text_primary']}; margin-bottom: 4px; display: flex; align-items: center; gap: 5px;">
                    <span>👥</span> General Population
                </div>
                <div style="font-size: 0.82rem; color: {t['text_secondary']}; line-height: 1.45;">
                    {cat_info['general_advisory']}
                </div>
            </div>
            <div style="background: {t['bg_secondary']}; padding: 14px; border-radius: 10px; border-left: 3px solid #EAB308; border: 1px solid {t['border']};">
                <div style="font-weight: 700; font-size: 0.86rem; color: {t['text_primary']}; margin-bottom: 4px; display: flex; align-items: center; gap: 5px;">
                    <span>🩺</span> Sensitive Groups (Children, Elderly, Asthmatics)
                </div>
                <div style="font-size: 0.82rem; color: {t['text_secondary']}; line-height: 1.45;">
                    {cat_info['sensitive_advisory']}
                </div>
            </div>
        </div>

        <div style="background: {t['bg_secondary']}; padding: 12px 16px; border-radius: 8px; display: flex; align-items: center; gap: 10px; border: 1px solid {t['border']};">
            <span style="font-size: 1.2rem;">💡</span>
            <div>
                <strong style="color: {t['text_primary']}; font-size: 0.86rem;">Recommended Protective Action:</strong>
                <span style="color: {t['text_secondary']}; font-size: 0.86rem; margin-left: 6px;">{cat_info['action']}</span>
            </div>
        </div>
    </div>
    """
    return clean_html_str(html)
