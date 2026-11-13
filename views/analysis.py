"""
AERIS - Air Quality Analysis View
Interactive data exploration, correlation analysis, pollutant relationships, and seasonal dynamics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import COLORS, apply_aeris_theme, render_html
from components.charts import (
    plot_correlation_heatmap,
    plot_scatter_relationship
)

def render_analysis(df):
    render_html("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; font-family: 'Poppins', sans-serif; font-size: 1.45rem; color: #12372A; font-weight: 700;">
            Air Quality Data Exploration & Analytics
        </h2>
        <p style="margin: 4px 0 0 0; color: #4A6258; font-size: 0.92rem;">
            Investigate empirical distributions, cross-pollutant correlations, and atmospheric seasonal drivers.
        </p>
    </div>
    """)
    
    # Tabbed exploration
    tab_corr, tab_scatter, tab_seasonal, tab_dist = st.tabs([
        "🔗 Correlation Matrix",
        "📈 Pollutant vs AQI Relationships",
        "🌦️ Seasonal & Monthly Dynamics",
        "📊 Multi-Pollutant Distributions"
    ])
    
    with tab_corr:
        with st.container(border=True):
            render_html(f"""
            <div style="margin-bottom: 14px; color: {COLORS['text_secondary']}; font-size: 0.9rem; line-height: 1.5;">
                The Pearson correlation coefficients below reveal the atmospheric coupling between individual pollutants and the composite Indian AQI. Notice that particulate matter (<strong style="color: {COLORS['forest']};">PM2.5 and PM10</strong>) exhibits the strongest positive correlation with AQI, serving as the dominant driver of air quality deterioration across Indian metropolitan corridors.
            </div>
            """)
            fig_corr = plot_correlation_heatmap(df)
            st.plotly_chart(fig_corr, use_container_width=True)
        
    with tab_scatter:
        with st.container(border=True):
            col_sel1, col_sel2 = st.columns([1, 2])
            with col_sel1:
                selected_pollutant = st.selectbox(
                    "Select Pollutant Variable for X-Axis:",
                    ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3'],
                    index=0
                )
                
            with col_sel2:
                render_html(f"""
                <div style="font-size: 0.82rem; color: {COLORS['text_muted']}; padding-top: 26px;">
                    Trendline computed using Ordinary Least Squares (OLS) regression across representative sampled observations.
                </div>
                """)
                
            fig_scat = plot_scatter_relationship(df, x_col=selected_pollutant, y_col='AQI')
            st.plotly_chart(fig_scat, use_container_width=True)
        
    with tab_seasonal:
        with st.container(border=True):
            # Add month and season column
            df_season = df.copy()
            df_season['Date'] = pd.to_datetime(df_season['Date'])
            df_season['Month_Name'] = df_season['Date'].dt.strftime('%b')
            df_season['Month_Num'] = df_season['Date'].dt.month
            
            def assign_season(m):
                if m in [11, 12, 1, 2]: return 'Winter'
                if m in [3, 4, 5]: return 'Summer / Pre-Monsoon'
                if m in [6, 7, 8, 9]: return 'Monsoon (Washout)'
                return 'Post-Monsoon'
                
            df_season['Season'] = df_season['Month_Num'].apply(assign_season)
            
            # Monthly mean AQI bar chart
            monthly_avg = df_season.groupby(['Month_Num', 'Month_Name'])['AQI'].mean().reset_index()
            monthly_avg = monthly_avg.sort_values('Month_Num')
            
            fig_season = go.Figure()
            fig_season.add_trace(go.Bar(
                x=monthly_avg['Month_Name'],
                y=monthly_avg['AQI'],
                marker=dict(
                    color=[COLORS['aqi_very_poor'] if m in [11, 12, 1] else (COLORS['aqi_good'] if m in [7, 8] else COLORS['emerald']) for m in monthly_avg['Month_Num']],
                    line=dict(color=COLORS['forest'], width=1)
                ),
                text=[f"{v:.0f}" for v in monthly_avg['AQI']],
                textposition='outside',
                textfont=dict(size=11, family="Space Grotesk, sans-serif"),
                hovertemplate='<b>%{x}</b><br>Average AQI: %{y:.1f}<extra></extra>'
            ))
            
            fig_season.update_layout(
                title="<b>Monthly Seasonal Cycle: Mean AQI Trajectory Across India</b>",
                xaxis_title="Month of Year",
                yaxis_title="Mean Ambient AQI"
            )
            st.plotly_chart(apply_aeris_theme(fig_season), use_container_width=True)
            
            render_html(f"""
            <div style="background: {COLORS['bg_main']}; padding: 14px 18px; border-radius: 10px; border-left: 4px solid {COLORS['emerald']}; margin-top: 10px;">
                <strong style="color: {COLORS['forest']}; font-size: 0.88rem;">Key Atmospheric Insight:</strong>
                <p style="margin: 4px 0 0 0; color: {COLORS['text_secondary']}; font-size: 0.84rem; line-height: 1.45;">
                    In the Indian subcontinent, air pollution follows an acute seasonal curve. During <strong>Winter (Nov–Jan)</strong>, nocturnal boundary layer collapse, thermal inversion, and low surface wind velocities trap particulate matter near ground level. Conversely, the <strong>Southwest Monsoon (Jul–Aug)</strong> triggers dramatic precipitation washout (wet scavenging), cleansing the troposphere and reducing AQI to Good / Satisfactory levels.
                </p>
            </div>
            """)
        
    with tab_dist:
        with st.container(border=True):
            pollutants_for_box = ['PM2.5', 'PM10', 'NO2', 'SO2', 'O3']
            box_fig = go.Figure()
            
            for p in pollutants_for_box:
                box_fig.add_trace(go.Box(
                    y=df[p],
                    name=p,
                    boxmean=True,
                    marker=dict(color=COLORS['emerald'])
                ))
                
            box_fig.update_layout(
                title="<b>Concentration Variance and Outlier Distribution (Boxplots)</b>",
                xaxis_title="Atmospheric Parameter",
                yaxis_title="Concentration (µg/m³)"
            )
            st.plotly_chart(apply_aeris_theme(box_fig), use_container_width=True)
