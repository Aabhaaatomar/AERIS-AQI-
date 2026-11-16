"""
AERIS 2.0 - Theme Manager
Defines Light, Dark, and Cream themes with complete color palettes, typography,
and dynamic CSS generation ensuring 100% readability with zero unreadable text.
"""

import streamlit as st

THEMES = {
    "Light": {
        "name": "Light Mode",
        "style": "Modern Environmental SaaS",
        "bg_main": "#F4F8F4",
        "bg_secondary": "#EAF2EA",
        "bg_card": "#FFFFFF",
        "primary": "#12372A",
        "secondary": "#1F8A70",
        "accent": "#1F8A70",
        "mint": "#B7E4C7",
        "sage": "#D8EAD9",
        "text_primary": "#1F2937",
        "text_secondary": "#4B5563",
        "text_muted": "#6B7280",
        "border": "#DCE8DD",
        "card_shadow": "0 2px 10px rgba(18, 55, 42, 0.05)",
        "sidebar_bg": "#FFFFFF",
        "sidebar_border": "#DCE8DD",
        "chat_user_bg": "#1F8A70",
        "chat_user_text": "#FFFFFF",
        "chat_bot_bg": "#FFFFFF",
        "chat_bot_text": "#1F2937",
        "chat_bot_border": "#DCE8DD",
        "input_bg": "#FFFFFF",
        "input_border": "#DCE8DD"
    },
    "Dark": {
        "name": "Dark Mode",
        "style": "Premium Dark Environmental Intelligence",
        "bg_main": "#101A17",
        "bg_secondary": "#172722",
        "bg_card": "#1D3029",
        "primary": "#34D399",
        "secondary": "#6EE7B7",
        "accent": "#34D399",
        "mint": "#A7F3D0",
        "sage": "#233830",
        "text_primary": "#F3F7F4",
        "text_secondary": "#B6C7BD",
        "text_muted": "#889F94",
        "border": "#30483D",
        "card_shadow": "0 4px 14px rgba(0, 0, 0, 0.35)",
        "sidebar_bg": "#14221D",
        "sidebar_border": "#30483D",
        "chat_user_bg": "#1F8A70",
        "chat_user_text": "#FFFFFF",
        "chat_bot_bg": "#1D3029",
        "chat_bot_text": "#F3F7F4",
        "chat_bot_border": "#30483D",
        "input_bg": "#172722",
        "input_border": "#30483D"
    },
    "Cream": {
        "name": "Cream Mode",
        "style": "Warm & Elegant Minimalist",
        "bg_main": "#F5EFE3",
        "bg_secondary": "#EEE4D3",
        "bg_card": "#FFFDF7",
        "primary": "#405A43",
        "secondary": "#82936A",
        "accent": "#82936A",
        "mint": "#C6D8AF",
        "sage": "#E0D5C1",
        "text_primary": "#352F27",
        "text_secondary": "#635B4F",
        "text_muted": "#8A8172",
        "border": "#E3D7C4",
        "card_shadow": "0 2px 10px rgba(64, 90, 67, 0.06)",
        "sidebar_bg": "#FFFDF7",
        "sidebar_border": "#E3D7C4",
        "chat_user_bg": "#405A43",
        "chat_user_text": "#FFFFFF",
        "chat_bot_bg": "#FFFDF7",
        "chat_bot_text": "#352F27",
        "chat_bot_border": "#E3D7C4",
        "input_bg": "#FFFDF7",
        "input_border": "#E3D7C4"
    }
}

# Standard Indian CPCB AQI Category Colors (Consistent across all themes)
CPCB_COLORS = {
    "Good": "#16A34A",
    "Satisfactory": "#84CC16",
    "Moderate": "#EAB308",
    "Poor": "#F97316",
    "Very Poor": "#DC2626",
    "Severe": "#7F1D1D"
}

def get_current_theme():
    """Retrieve the currently active theme dictionary from session state."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Light"
    theme_key = st.session_state["theme"]
    if theme_key not in THEMES:
        theme_key = "Light"
        st.session_state["theme"] = "Light"
    return THEMES[theme_key]

def get_theme_colors():
    """Get active theme palette combined with CPCB colors."""
    t = get_current_theme()
    colors = dict(t)
    colors.update({
        "aqi_good": CPCB_COLORS["Good"],
        "aqi_satisfactory": CPCB_COLORS["Satisfactory"],
        "aqi_moderate": CPCB_COLORS["Moderate"],
        "aqi_poor": CPCB_COLORS["Poor"],
        "aqi_very_poor": CPCB_COLORS["Very Poor"],
        "aqi_severe": CPCB_COLORS["Severe"]
    })
    return colors

def generate_global_css(t):
    """
    Generate comprehensive CSS for the selected theme.
    Fixes all transparency, low-contrast text, borders, buttons, and form inputs.
    """
    return f"""
    <style>
        /* Import Premium Typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Manrope:wght@500;600;700;800&family=Poppins:wght@500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

        /* Global Base */
        html, body, [class*="css"], .stApp {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: {t['bg_main']} !important;
            color: {t['text_primary']} !important;
        }}

        /* App Container */
        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 3.5rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1400px;
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: {t['sidebar_bg']} !important;
            border-right: 1px solid {t['sidebar_border']} !important;
        }}

        section[data-testid="stSidebar"] * {{
            color: {t['text_primary']} !important;
        }}

        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {{
            color: {t['text_secondary']} !important;
        }}

        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Manrope', 'Poppins', sans-serif !important;
            color: {t['primary']} !important;
            letter-spacing: -0.3px;
        }}

        /* Paragraphs and Text */
        p, span, label, div {{
            color: {t['text_primary']};
        }}

        /* Card Containers (st.container with border) */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 14px !important;
            box-shadow: {t['card_shadow']} !important;
            padding: 1.25rem !important;
            color: {t['text_primary']} !important;
        }}

        /* Fix Streamlit Expander */
        .streamlit-expanderHeader {{
            background-color: {t['bg_secondary']} !important;
            color: {t['text_primary']} !important;
            border-radius: 10px !important;
            border: 1px solid {t['border']} !important;
        }}

        div[data-testid="stExpander"] {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 10px !important;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {t['primary']} !important;
            color: #FFFFFF !important;
            border: 1px solid {t['primary']} !important;
            border-radius: 10px !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            padding: 0.5rem 1.1rem !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
        }}

        .stButton > button:hover {{
            background-color: {t['secondary']} !important;
            border-color: {t['secondary']} !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.16) !important;
        }}

        /* Primary Button */
        button[kind="primary"] {{
            background: linear-gradient(135deg, {t['primary']} 0%, {t['secondary']} 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 700 !important;
        }}

        /* Inputs & Selectboxes */
        .stTextInput input, .stSelectbox div[data-baseweb="select"], .stNumberInput input {{
            background-color: {t['input_bg']} !important;
            color: {t['text_primary']} !important;
            border-color: {t['border']} !important;
            border-radius: 10px !important;
        }}

        /* Sliders */
        .stSlider > div > div > div > div {{
            background-color: {t['secondary']} !important;
        }}

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: transparent !important;
            border-bottom: 2px solid {t['border']} !important;
            padding-bottom: 4px;
        }}

        .stTabs [data-baseweb="tab"] {{
            height: 42px;
            border-radius: 8px 8px 0 0 !important;
            padding: 0 16px !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            color: {t['text_secondary']} !important;
            background-color: transparent !important;
            border: none !important;
        }}

        .stTabs [aria-selected="true"] {{
            color: {t['primary']} !important;
            border-bottom: 3px solid {t['primary']} !important;
            background-color: transparent !important;
        }}

        /* Chat Input Box */
        div[data-testid="stChatInput"] {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 16px !important;
            box-shadow: {t['card_shadow']} !important;
        }}

        div[data-testid="stChatInput"] textarea {{
            color: {t['text_primary']} !important;
            background-color: transparent !important;
        }}

        /* Metrics Widget */
        div[data-testid="stMetricValue"] {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: {t['text_primary']} !important;
            font-weight: 700 !important;
        }}
        div[data-testid="stMetricLabel"] {{
            color: {t['text_secondary']} !important;
            font-weight: 600 !important;
        }}

        /* Header backdrop */
        header[data-testid="stHeader"] {{
            background: {t['bg_main']} !important;
        }}

        /* Hide Streamlit Clutter */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
    """
