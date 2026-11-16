"""
AERIS 2.0 - Header Component
Theme-aware branding banner with live status, environmental emblem, and crisp typography.
"""

import streamlit as st
from config import render_html
from utils.theme_manager import get_theme_colors

def render_header(title="AERIS 2.0", subtitle="Breathe Smarter. Understand Better.", location_text="Multi-City Network", status_text="Live CAAQMS Active"):
    """Render a clean, high-contrast theme-aware top header banner."""
    t = get_theme_colors()
    
    html = f"""
    <div style="background: {t['bg_card']}; border: 1px solid {t['border']}; border-radius: 16px; padding: 20px 24px; margin-bottom: 22px; box-shadow: {t['card_shadow']}; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px;">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, {t['primary']} 0%, {t['secondary']} 100%); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; box-shadow: 0 4px 12px rgba(0,0,0,0.12);">
                🍃
            </div>
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 1.45rem; font-weight: 700; color: {t['primary']}; letter-spacing: -0.5px;">
                        AERIS 2.0
                    </span>
                    <span style="background: {t['bg_secondary']}; color: {t['primary']}; border: 1px solid {t['border']}; padding: 2px 8px; border-radius: 12px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase;">
                        AI System
                    </span>
                </div>
                <div style="font-size: 0.86rem; color: {t['text_secondary']}; margin-top: 2px; font-weight: 480;">
                    {subtitle}
                </div>
            </div>
        </div>

        <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px;">
            <div style="background: {t['bg_secondary']}; border: 1px solid {t['border']}; border-radius: 10px; padding: 6px 14px; text-align: left;">
                <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.5px; color: {t['text_muted']}; font-weight: 700;">Location Focus</div>
                <div style="font-size: 0.82rem; font-weight: 600; color: {t['text_primary']};">{location_text}</div>
            </div>

            <div style="background: {t['bg_secondary']}; border: 1px solid {t['border']}; border-radius: 10px; padding: 6px 14px; text-align: left;">
                <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.5px; color: {t['text_muted']}; font-weight: 700;">System Telemetry</div>
                <div style="font-size: 0.82rem; font-weight: 600; color: {t['text_primary']}; display: flex; align-items: center; gap: 6px;">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #16A34A; display: inline-block;"></span>
                    {status_text}
                </div>
            </div>
        </div>
    </div>
    """
    render_html(html)
