"""
AERIS - Air Quality Intelligence System
Configuration, Theme Palette, CPCB Standards, and Constants
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

def render_html(html_code):
    """
    Renders raw HTML safely in Streamlit without the Markdown parser
    mistakenly converting 4-space indented lines into code blocks.
    """
    clean_html = "\n".join(line.strip() for line in html_code.splitlines() if line.strip())
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# Visual Palette
# ---------------------------------------------------------
COLORS = {
    # Brand Primary
    'forest': '#12372A',
    'emerald': '#1F8A70',
    'mint': '#B7E4C7',
    'sage': '#D8EAD9',
    
    # Backgrounds
    'bg_main': '#F4F8F4',
    'bg_card': '#FFFFFF',
    'bg_secondary': '#EAF2EA',
    'border': '#E2EBE2',
    
    # Typography
    'text_primary': '#0D231C',
    'text_secondary': '#4A6258',
    'text_muted': '#7A9287',
    
    # AQI Category Accents (Indian CPCB standard)
    'aqi_good': '#16A34A',
    'aqi_satisfactory': '#84CC16',
    'aqi_moderate': '#EAB308',
    'aqi_poor': '#F97316',
    'aqi_very_poor': '#DC2626',
    'aqi_severe': '#7F1D1D'
}

# ---------------------------------------------------------
# Official CPCB Breakpoints for Sub-index calculation
# ---------------------------------------------------------
CPCB_BREAKPOINTS = {
    'PM2.5': [
        (0, 30, 0, 50),
        (30, 60, 50, 100),
        (60, 90, 100, 200),
        (90, 120, 200, 300),
        (120, 250, 300, 400),
        (250, 500, 400, 500)
    ],
    'PM10': [
        (0, 50, 0, 50),
        (50, 100, 50, 100),
        (100, 250, 100, 200),
        (250, 350, 200, 300),
        (350, 430, 300, 400),
        (430, 600, 400, 500)
    ],
    'NO2': [
        (0, 40, 0, 50),
        (40, 80, 50, 100),
        (80, 180, 100, 200),
        (180, 280, 200, 300),
        (280, 400, 300, 400),
        (400, 600, 400, 500)
    ],
    'SO2': [
        (0, 40, 0, 50),
        (40, 80, 50, 100),
        (80, 380, 100, 200),
        (380, 800, 200, 300),
        (800, 1600, 300, 400),
        (1600, 2000, 400, 500)
    ],
    'CO': [
        (0.0, 1.0, 0, 50),
        (1.0, 2.0, 50, 100),
        (2.0, 10.0, 100, 200),
        (10.0, 17.0, 200, 300),
        (17.0, 34.0, 300, 400),
        (34.0, 50.0, 400, 500)
    ],
    'O3': [
        (0, 50, 0, 50),
        (50, 100, 50, 100),
        (100, 168, 100, 200),
        (168, 208, 200, 300),
        (208, 748, 300, 400),
        (748, 1000, 400, 500)
    ]
}

def calculate_sub_index(conc, pollutant):
    """Calculate sub-index for a pollutant according to CPCB piecewise linear formula."""
    import pandas as pd
    if pd.isna(conc) or conc < 0:
        return 0.0
    breakpoints = CPCB_BREAKPOINTS[pollutant]
    for b_low, b_high, i_low, i_high in breakpoints:
        if b_low <= conc <= b_high:
            sub = i_low + ((i_high - i_low) / (b_high - b_low)) * (conc - b_low)
            return round(sub, 2)
    b_low, b_high, i_low, i_high = breakpoints[-1]
    if conc > b_high:
        return 500.0
    return 0.0

# ---------------------------------------------------------
# Indian CPCB AQI Categories & Advisories
# ---------------------------------------------------------
AQI_CATEGORIES = [
    {
        'range': (0, 50),
        'name': 'Good',
        'color': COLORS['aqi_good'],
        'icon': '🌱',
        'summary': 'Minimal health impact. Air quality is considered satisfactory, and air pollution poses little or no risk.',
        'general_advisory': 'Ideal air quality for outdoor recreation, jogging, sports, and ventilation.',
        'sensitive_advisory': 'No special precautions needed. Safe for everyone including children and elderly.',
        'action': 'Enjoy outdoor activities; keep home ventilated.'
    },
    {
        'range': (51, 100),
        'name': 'Satisfactory',
        'color': COLORS['aqi_satisfactory'],
        'icon': '🌿',
        'summary': 'Minor breathing discomfort to sensitive individuals on prolonged exposure.',
        'general_advisory': 'Air quality is acceptable for the general public. Outdoor activities are safe.',
        'sensitive_advisory': 'Individuals with severe asthma or cardiovascular sensitivities should monitor symptoms.',
        'action': 'Normal activities allowed; sensitive groups keep inhalers handy.'
    },
    {
        'range': (101, 200),
        'name': 'Moderate',
        'color': COLORS['aqi_moderate'],
        'icon': '⚠️',
        'summary': 'Breathing discomfort to people with lung disease, asthma, and heart conditions.',
        'general_advisory': 'Noticeable haze. General population experiences slight throat or eye irritation on prolonged exertion.',
        'sensitive_advisory': 'Children, seniors, and asthmatic patients should limit prolonged outdoor exertion.',
        'action': 'Reduce intense outdoor exercises during peak rush hours.'
    },
    {
        'range': (201, 300),
        'name': 'Poor',
        'color': COLORS['aqi_poor'],
        'icon': '😷',
        'summary': 'Breathing discomfort to most people on prolonged exposure. Pronounced discomfort for sensitive groups.',
        'general_advisory': 'Avoid strenuous outdoor activities. Visible smog layer often present.',
        'sensitive_advisory': 'Avoid outdoor physical activities; close windows to minimize indoor pollution.',
        'action': 'Wear N95/FFP2 masks outdoors; run indoor HEPA purifiers.'
    },
    {
        'range': (301, 400),
        'name': 'Very Poor',
        'color': COLORS['aqi_very_poor'],
        'icon': '🚨',
        'summary': 'Respiratory illness on prolonged exposure. Significant trigger for cardiac and respiratory attacks.',
        'general_advisory': 'Unhealthy for everyone. Even healthy individuals develop respiratory symptoms.',
        'sensitive_advisory': 'High risk. All sensitive groups must remain indoors in filtered air environments.',
        'action': 'Strictly minimize outdoor exposure; avoid morning jogs; use air purifiers.'
    },
    {
        'range': (401, 500),
        'name': 'Severe',
        'color': COLORS['aqi_severe'],
        'icon': '☠️',
        'summary': 'Emergency conditions. Severe health impact on healthy people and serious exacerbation for diseased patients.',
        'general_advisory': 'Hazardous air emergency. Outdoor activity should be completely prohibited.',
        'sensitive_advisory': 'Critical danger. Immediate risk of acute respiratory distress.',
        'action': 'Keep all windows shut; run high-grade air purification; wear N99 respirators if transit is unavoidable.'
    }
]

def get_category_info(aqi_value):
    """Return dictionary with category details for a given AQI."""
    aqi = float(aqi_value)
    for cat in AQI_CATEGORIES:
        low, high = cat['range']
        if low <= aqi <= high:
            return cat
    if aqi > 500:
        return AQI_CATEGORIES[-1]
    return AQI_CATEGORIES[0]

# ---------------------------------------------------------
# Detailed Pollutant Metadata
# ---------------------------------------------------------
POLLUTANT_INFO = {
    'PM2.5': {
        'name': 'Fine Particulate Matter (PM2.5)',
        'unit': 'µg/m³',
        'safe_limit_24h': '60 µg/m³ (CPCB) / 15 µg/m³ (WHO)',
        'description': 'Atmospheric particulate matter that have a diameter of less than 2.5 micrometers (about 3% the diameter of a human hair). Due to their minute size, they bypass nasal filtration and penetrate deeply into the pulmonary alveoli and enter the bloodstream.',
        'primary_sources': 'Combustion of fuels (diesel, petrol, coal), biomass and crop stubble burning, brick kilns, industrial smelters, and secondary aerosol synthesis from NOx and SOx.',
        'health_impacts': 'Aggravates asthma, decreases lung function, triggers cardiovascular events, and is classified as a Group 1 human carcinogen by the IARC.',
        'chemical_nature': 'Complex mixture of elemental carbon, organic carbon compounds, sulfates, nitrates, and trace metals.'
    },
    'PM10': {
        'name': 'Coarse Particulate Matter (PM10)',
        'unit': 'µg/m³',
        'safe_limit_24h': '100 µg/m³ (CPCB) / 45 µg/m³ (WHO)',
        'description': 'Inhalable particles with diameters of 10 micrometers or smaller. They primarily deposit in the upper respiratory tract, nasal passages, and bronchi.',
        'primary_sources': 'Road dust resuspension, construction and demolition debris, mechanical crushing, agricultural tilling, and unpaved road vehicular traffic.',
        'health_impacts': 'Causes eye, nose, and throat irritation, exacerbates chronic bronchitis, coughing, wheezing, and limits athletic exertion.',
        'chemical_nature': 'Silica, mineral dust, crustal materials, fly ash, pollen fragments, and biological spores.'
    },
    'NO2': {
        'name': 'Nitrogen Dioxide (NO2)',
        'unit': 'µg/m³',
        'safe_limit_24h': '80 µg/m³ (CPCB) / 25 µg/m³ (WHO)',
        'description': 'A pungent reddish-brown gas belonging to the group of reactive nitrogen oxides (NOx). It forms rapidly in the ambient air through the oxidation of nitric oxide (NO).',
        'primary_sources': 'High-temperature internal combustion engines (especially diesel vehicles), thermal power plants, industrial furnaces, and gas heaters.',
        'health_impacts': 'Inflames airways, increases bronchial hyper-responsiveness, worsens allergic asthma, and acts as a key chemical precursor for ground-level ozone and nitrate aerosols.',
        'chemical_nature': 'Oxidant gas contributing heavily to acid precipitation (HNO3) and photochemical smog creation.'
    },
    'SO2': {
        'name': 'Sulphur Dioxide (SO2)',
        'unit': 'µg/m³',
        'safe_limit_24h': '80 µg/m³ (CPCB) / 40 µg/m³ (WHO)',
        'description': 'A colorless, toxic gas with an intense, suffocating odor. It dissolves readily in water to form sulfurous acid.',
        'primary_sources': 'Combustion of sulfur-containing fossil fuels (coal and crude oil), coal-fired thermal power plants, petroleum refineries, and metal processing facilities.',
        'health_impacts': 'Causes rapid bronchoconstriction within minutes of inhalation, triggers acute asthmatic attacks, and causes chronic respiratory infections.',
        'chemical_nature': 'Oxidizes in the atmosphere to form sulfuric acid (H2SO4) droplets, leading to acid rain and damaging terrestrial vegetation and historical stone monuments.'
    },
    'CO': {
        'name': 'Carbon Monoxide (CO)',
        'unit': 'mg/m³',
        'safe_limit_24h': '2.0 mg/m³ (8h CPCB) / 4.0 mg/m³ (WHO)',
        'description': 'A colorless, odorless, and tasteless gas resulting from incomplete fuel combustion. It possesses an affinity for human hemoglobin ~200 times higher than oxygen.',
        'primary_sources': 'Vehicular exhaust (especially during congested stop-and-go idling), inefficient biomass stoves, open waste fires, and industrial kilns.',
        'health_impacts': 'Binds with hemoglobin to form carboxyhemoglobin (COHb), reducing oxygen transport to the brain and vital organs. Causes headaches, dizziness, impaired reflexes, and myocardial ischemia.',
        'chemical_nature': 'Carbonyl gas; relatively unreactive in the lower troposphere with an atmospheric lifetime of approximately 1-2 months.'
    },
    'O3': {
        'name': 'Ground-Level Ozone (O3)',
        'unit': 'µg/m³',
        'safe_limit_24h': '100 µg/m³ (8h CPCB) / 100 µg/m³ (WHO)',
        'description': 'A secondary atmospheric pollutant not emitted directly into the air, but synthesized through photochemical reactions between NOx and Volatile Organic Compounds (VOCs) in the presence of intense solar ultraviolet radiation.',
        'primary_sources': 'Photochemical smog reactions catalyzed by bright sunlight acting on emissions from automobiles, chemical solvents, refineries, and gasoline distribution.',
        'health_impacts': 'Powerful oxidant causing inflammation of the airways, deep alveolar cellular damage, coughing, chest tightness, and marked reductions in athletic pulmonary capacity. Highly toxic to agricultural crops and reduces crop yields.',
        'chemical_nature': 'Trioxygen allotrope with strong oxidizing potential; ambient levels peak in hot sunny afternoons and decline during evening hours.'
    }
}

# ---------------------------------------------------------
# Custom Plotly Clean SaaS Environmental Theme
# ---------------------------------------------------------
def apply_aeris_theme(fig):
    """Apply AERIS custom nature-inspired aesthetic styling to Plotly figures."""
    fig.update_layout(
        paper_bgcolor='rgba(255, 255, 255, 0)',
        plot_bgcolor='rgba(255, 255, 255, 0)',
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            color=COLORS['text_primary'],
            size=12
        ),
        title=dict(
            font=dict(
                family="Poppins, Manrope, sans-serif",
                size=15,
                color=COLORS['forest']
            ),
            x=0.01,
            xanchor='left',
            y=0.96
        ),
        margin=dict(l=45, r=25, t=55, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255, 255, 255, 0.7)',
            bordercolor=COLORS['border'],
            borderwidth=1,
            font=dict(size=11)
        ),
        hoverlabel=dict(
            bgcolor=COLORS['forest'],
            font_size=12,
            font_family="Inter, sans-serif",
            font_color="#FFFFFF"
        )
    )
    
    fig.update_xaxes(
        gridcolor='#E2EBE2',
        zerolinecolor='#CBD8CB',
        linecolor='#CBD8CB',
        tickfont=dict(color=COLORS['text_secondary'], size=11),
        title_font=dict(color=COLORS['forest'], size=12)
    )
    
    fig.update_yaxes(
        gridcolor='#E2EBE2',
        zerolinecolor='#CBD8CB',
        linecolor='#CBD8CB',
        tickfont=dict(color=COLORS['text_secondary'], size=11),
        title_font=dict(color=COLORS['forest'], size=12)
    )
    return fig
