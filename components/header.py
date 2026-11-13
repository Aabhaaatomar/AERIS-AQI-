"""
AERIS - Main Header Component
Renders the brand banner, title, dataset telemetry indicators, and filter badges.
"""

import streamlit as st
from config import COLORS

def render_header(total_records=7310, date_range="2023 - 2024", selected_city=None, cities_count=10):
    """Render top-level dashboard header with dataset metadata and environmental badge."""
    
    city_display = selected_city if selected_city and selected_city != "All Cities (National Aggregate)" else f"{cities_count} Indian Cities Monitoring Network"
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['forest']} 0%, #174A38 60%, {COLORS['emerald']} 100%);
        border-radius: 16px;
        padding: 24px 28px;
        color: white;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(18, 55, 42, 0.12);
    ">
        <!-- Subtle atmospheric background glow -->
        <div style="
            position: absolute;
            right: -20px;
            top: -30px;
            width: 220px;
            height: 220px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(183, 228, 199, 0.15) 0%, rgba(255,255,255,0) 70%);
            pointer-events: none;
        "></div>

        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px; position: relative; z-index: 1;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                    <span style="
                        background: rgba(255, 255, 255, 0.18);
                        border: 1px solid rgba(255, 255, 255, 0.25);
                        padding: 3px 10px;
                        border-radius: 20px;
                        font-size: 0.75rem;
                        font-weight: 600;
                        letter-spacing: 0.5px;
                        text-transform: uppercase;
                        color: {COLORS['mint']};
                        display: flex;
                        align-items: center;
                        gap: 5px;
                    ">
                        <span>🍃</span> AERIS PLATFORM
                    </span>
                    <span style="font-size: 0.78rem; color: rgba(255, 255, 255, 0.75);">
                        CPCB Telemetry • NAQI Standard
                    </span>
                </div>
                <h1 style="
                    margin: 0;
                    font-family: 'Poppins', sans-serif;
                    font-size: 1.85rem;
                    font-weight: 700;
                    letter-spacing: -0.5px;
                    color: #FFFFFF;
                ">
                    Air Quality Intelligence
                </h1>
                <p style="
                    margin: 4px 0 0 0;
                    font-size: 0.95rem;
                    color: rgba(255, 255, 255, 0.85);
                    font-weight: 400;
                ">
                    Monitor pollution. Understand patterns. Predict air quality.
                </p>
            </div>

            <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
                <div style="
                    background: rgba(255, 255, 255, 0.12);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                    border-radius: 10px;
                    padding: 8px 14px;
                    text-align: left;
                ">
                    <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.5px; color: {COLORS['mint']}; font-weight: 600;">Location Focus</div>
                    <div style="font-size: 0.88rem; font-weight: 600; color: #FFFFFF;">{city_display}</div>
                </div>

                <div style="
                    background: rgba(255, 255, 255, 0.12);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                    border-radius: 10px;
                    padding: 8px 14px;
                    text-align: left;
                ">
                    <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.5px; color: {COLORS['mint']}; font-weight: 600;">CPCB Dataset</div>
                    <div style="font-size: 0.88rem; font-weight: 600; color: #FFFFFF;">{total_records:,} Records ({date_range})</div>
                </div>

                <div style="
                    background: rgba(255, 255, 255, 0.12);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                    border-radius: 10px;
                    padding: 8px 14px;
                    text-align: left;
                ">
                    <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.5px; color: {COLORS['mint']}; font-weight: 600;">Status</div>
                    <div style="font-size: 0.88rem; font-weight: 600; color: #FFFFFF; display: flex; align-items: center; gap: 6px;">
                        <span style="width: 8px; height: 8px; border-radius: 50%; background: #4ADE80; display: inline-block;"></span>
                        Verified Telemetry
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
