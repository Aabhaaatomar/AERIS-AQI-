"""
AERIS 2.0 - Chat Interface Component
Provides modern, visually stunning chat UI with:
- Welcome banner with tagline
- 6 Clickable suggestion cards
- User messages aligned right, AI responses aligned left
- Formatted markdown, tables, badges, and source attributions
- Chat input bar and conversation controls
"""

import streamlit as st
from utils.theme_manager import get_theme_colors, get_current_theme
from config import render_html

SUGGESTED_QUESTIONS = [
    {
        "icon": "🌍",
        "title": "Check AQI in my city",
        "prompt": "What is the current live AQI in Delhi and is it safe to go outside?"
    },
    {
        "icon": "🌫️",
        "title": "Why is pollution increasing?",
        "prompt": "Why does air pollution spike in North Indian cities during winter months?"
    },
    {
        "icon": "📊",
        "title": "Compare two cities",
        "prompt": "Compare the air quality and pollution levels between Delhi and Mumbai."
    },
    {
        "icon": "🧪",
        "title": "Understand air pollutants",
        "prompt": "What is PM2.5, why is it so hazardous, and what are its safe CPCB limits?"
    },
    {
        "icon": "🏭",
        "title": "Major pollution contributors",
        "prompt": "Which pollutants and sources contribute most to poor air quality in Indian metros?"
    },
    {
        "icon": "🔮",
        "title": "Predict AQI",
        "prompt": "Predict AQI using PM2.5 = 95, PM10 = 180, NO2 = 45, SO2 = 20, CO = 1.4, O3 = 40"
    }
]

def render_welcome_screen(colors):
    """Render the welcome banner and suggested question cards."""
    # Leaf badge & Welcome headline
    render_html(f"""
    <div style="text-align: center; padding: 25px 20px 20px 20px; margin-bottom: 25px; border-radius: 16px; background: {colors['bg_secondary']}; border: 1px solid {colors['border']};">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 56px; height: 56px; border-radius: 16px; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); font-size: 1.8rem; margin-bottom: 12px; box-shadow: {colors['card_shadow']};">
            🌿
        </div>
        <h2 style="font-family: 'Poppins', 'Manrope', sans-serif; font-size: 1.75rem; font-weight: 700; color: {colors['primary']}; margin: 0 0 6px 0; letter-spacing: -0.4px;">
            Hello! I'm AERIS 2.0
        </h2>
        <p style="font-size: 0.98rem; color: {colors['text_secondary']}; max-width: 620px; margin: 0 auto; line-height: 1.5;">
            Your personal AI-powered air quality assistant. Ask me anything about real-time city AQI, atmospheric pollutants, predictive estimates, or health precautions.
        </p>
    </div>
    """)
    
    st.markdown(f"<div style='font-weight: 600; font-size: 0.9rem; color: {colors['text_secondary']}; margin-bottom: 12px;'>💡 Suggested Questions to Get Started:</div>", unsafe_allow_html=True)
    
    # Render suggestion cards in 3 columns x 2 rows
    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3, c1, c2, c3]
    
    for idx, item in enumerate(SUGGESTED_QUESTIONS):
        with cols[idx]:
            button_label = f"{item['icon']} {item['title']}"
            if st.button(button_label, key=f"sug_btn_{idx}", use_container_width=True):
                st.session_state["pending_prompt"] = item["prompt"]
                st.rerun()

def render_chat_message(role, content, colors):
    """Render a single message with theme styling and alignment."""
    if role == "user":
        # Right aligned user bubble
        render_html(f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 16px;">
            <div style="max-width: 80%; background: {colors['chat_user_bg']}; color: {colors['chat_user_text']}; padding: 12px 18px; border-radius: 18px 18px 4px 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); font-size: 0.95rem; line-height: 1.5;">
                <div style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.85; margin-bottom: 4px;">
                    You
                </div>
                <div>{content}</div>
            </div>
        </div>
        """)
    else:
        # Left aligned assistant bubble with AERIS emblem
        # Render assistant container
        with st.container():
            render_html(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <div style="width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); display: flex; align-items: center; justify-content: center; font-size: 0.95rem;">
                    🌿
                </div>
                <span style="font-weight: 700; font-size: 0.85rem; color: {colors['primary']}; letter-spacing: 0.2px;">
                    AERIS AI Assistant
                </span>
                <span style="font-size: 0.72rem; padding: 2px 8px; border-radius: 10px; background: {colors['bg_secondary']}; color: {colors['text_muted']}; border: 1px solid {colors['border']}; font-weight: 600;">
                    NAQI Intelligence
                </span>
            </div>
            """)
            
            # Use st.markdown for assistant content to preserve full markdown/table/code formatting
            with st.container(border=True):
                st.markdown(content)
                
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
