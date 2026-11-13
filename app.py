"""
AERIS – Air Quality Intelligence System
Understand the Air. Predict the Future.

Main Application Controller & Layout
"""

import os
import sys
import pandas as pd
import streamlit as st

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from config import COLORS, render_html
from components.header import render_header
from views.overview import render_overview
from views.prediction import render_prediction
from views.analysis import render_analysis
from views.pollutants import render_pollutants
from views.model_performance import render_model_performance
from views.about import render_about

try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    HAS_OPTION_MENU = False

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AERIS | Air Quality Intelligence System",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Global Typography and Aesthetic Styling (Custom CSS)
# ---------------------------------------------------------
CUSTOM_CSS = f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Manrope:wght@500;600;700;800&family=Poppins:wght@500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    /* Global Body & Background */
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: {COLORS['text_primary']};
    }}

    .stApp {{
        background-color: {COLORS['bg_main']};
    }}

    /* Main Container Padding */
    .block-container {{
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1400px;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 1px solid {COLORS['border']} !important;
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding-top: 2rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }}

    /* Headers Typography */
    h1, h2, h3, h4 {{
        font-family: 'Poppins', 'Manrope', sans-serif !important;
        color: {COLORS['forest']};
        letter-spacing: -0.3px;
    }}

    /* Streamlit Buttons Custom Styling */
    .stButton>button {{
        background: {COLORS['forest']};
        color: #FFFFFF !important;
        border: 1px solid {COLORS['forest']};
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 0.5rem 1rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 6px rgba(18, 55, 42, 0.08);
    }}

    .stButton>button:hover {{
        background: {COLORS['emerald']};
        border-color: {COLORS['emerald']};
        color: #FFFFFF !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(31, 138, 112, 0.22);
    }}

    /* Primary CTA Button */
    button[kind="primary"] {{
        background: linear-gradient(135deg, {COLORS['forest']} 0%, {COLORS['emerald']} 100%) !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        padding: 0.65rem 1.2rem !important;
    }}

    button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #0d281e 0%, #176f5a 100%) !important;
        box-shadow: 0 6px 16px rgba(18, 55, 42, 0.25) !important;
    }}

    /* Selectbox, Slider, Radio Tweaks */
    .stSelectbox div[data-baseweb="select"] {{
        border-radius: 10px;
        border-color: {COLORS['border']};
    }}

    .stSlider > div > div > div > div {{
        background-color: {COLORS['emerald']} !important;
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid {COLORS['border']};
        padding-bottom: 4px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 42px;
        border-radius: 8px 8px 0 0;
        padding: 0 16px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.88rem;
        color: {COLORS['text_secondary']};
        background-color: transparent;
        border: none;
    }}

    .stTabs [aria-selected="true"] {{
        color: {COLORS['forest']} !important;
        border-bottom: 3px solid {COLORS['forest']} !important;
        background-color: transparent !important;
    }}

    /* Hide standard Streamlit header clutter */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{
        background: rgba(244, 248, 244, 0.7);
        backdrop-filter: blur(8px);
    }}
</style>
"""
render_html(CUSTOM_CSS)

# ---------------------------------------------------------
# Data Loader (Cached)
# ---------------------------------------------------------
DATA_PATH = os.path.join(current_dir, "data", "city_day_cpcb.csv")

@st.cache_data
def load_air_quality_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        return df
    st.error(f"Dataset file missing at {DATA_PATH}. Please generate it using generate_dataset.py.")
    return pd.DataFrame()

df = load_air_quality_data()

# ---------------------------------------------------------
# Sidebar Navigation & Branding
# ---------------------------------------------------------
with st.sidebar:
    # Brand Emblem & Logo
    render_html(f"""
    <div style="padding-bottom: 18px; border-bottom: 1px solid {COLORS['border']}; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, {COLORS['forest']} 0%, {COLORS['emerald']} 100%); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; box-shadow: 0 2px 8px rgba(18,55,42,0.15);">
                🍃
            </div>
            <div>
                <span style="font-family: 'Poppins', sans-serif; font-size: 1.35rem; font-weight: 700; letter-spacing: -0.5px; color: {COLORS['forest']}; display: block; line-height: 1.1;">
                    AERIS
                </span>
                <span style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.8px; color: {COLORS['text_muted']}; font-weight: 600;">
                    Air Intelligence
                </span>
            </div>
        </div>
        <div style="font-size: 0.78rem; color: {COLORS['text_secondary']}; font-style: italic; margin-top: 6px; padding-left: 2px;">
            "Understand the Air. Predict the Future."
        </div>
    </div>
    """)
    
    # Navigation items
    nav_options = [
        "Overview",
        "AQI Prediction",
        "Air Quality Analysis",
        "Pollutant Insights",
        "Model Performance",
        "About Project"
    ]
    
    if HAS_OPTION_MENU:
        selected_nav = option_menu(
            menu_title=None,
            options=nav_options,
            icons=["grid-1x2", "speedometer2", "graph-up-arrow", "droplet-half", "cpu", "info-circle"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": COLORS['emerald'], "font-size": "15px"},
                "nav-link": {
                    "font-size": "0.9rem",
                    "font-family": "Inter, sans-serif",
                    "font-weight": "500",
                    "text-align": "left",
                    "margin": "4px 0",
                    "padding": "10px 14px",
                    "border-radius": "10px",
                    "color": COLORS['text_secondary'],
                    "--hover-color": "#F4F8F4"
                },
                "nav-link-selected": {
                    "background-color": COLORS['forest'],
                    "color": "#FFFFFF",
                    "font-weight": "600",
                    "box-shadow": "0 2px 8px rgba(18,55,42,0.12)"
                }
            }
        )
    else:
        selected_nav = st.radio("Navigation Menu", nav_options, index=0)
        
    # Sidebar footer badge
    render_html(f"""
    <div style="margin-top: 40px; padding: 14px; border-radius: 10px; background: {COLORS['bg_main']}; border: 1px solid {COLORS['border']};">
        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
            <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #16A34A;"></span>
            <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: {COLORS['forest']};">
                CPCB Standard 2024
            </span>
        </div>
        <p style="margin: 0; font-size: 0.74rem; color: {COLORS['text_muted']}; line-height: 1.35;">
            Supervised ML model engine utilizing Scikit-learn pipelines with zero-latency Joblib serialization.
        </p>
    </div>
    """)

# ---------------------------------------------------------
# Main Page Router
# ---------------------------------------------------------
# Render Header on all operational views
if not df.empty:
    cities_count = df['City'].nunique()
    total_records = len(df)
else:
    cities_count = 10
    total_records = 7310

render_header(total_records=total_records, date_range="2023 - 2024", selected_city=None, cities_count=cities_count)

# Dispatch view
if selected_nav == "Overview":
    render_overview(df)
elif selected_nav == "AQI Prediction":
    render_prediction()
elif selected_nav == "Air Quality Analysis":
    render_analysis(df)
elif selected_nav == "Pollutant Insights":
    render_pollutants(df)
elif selected_nav == "Model Performance":
    render_model_performance()
elif selected_nav == "About Project":
    render_about()
