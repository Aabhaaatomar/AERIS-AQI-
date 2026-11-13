"""
AERIS - Overview View
High-level environmental telemetry analytics, KPI cards, and aggregate visualizations.
"""

import streamlit as st
import pandas as pd
from config import COLORS, render_html
from components.cards import render_stat_card
from components.charts import (
    plot_aqi_distribution,
    plot_aqi_category_donut,
    plot_city_aqi_ranking,
    plot_pollutant_concentration_comparison,
    plot_aqi_trend
)

def render_overview(df):
    render_html("""
    <div style="margin-bottom: 16px;">
        <h2 style="margin: 0; font-family: 'Poppins', sans-serif; font-size: 1.4rem; color: #12372A; font-weight: 600;">
            National Air Quality Overview
        </h2>
        <p style="margin: 3px 0 0 0; color: #4A6258; font-size: 0.88rem;">
            Synthesized telemetry across 10 major Indian municipal monitoring networks (2023–2024).
        </p>
    </div>
    """)
    
    # Filter Row (City Selector)
    cities = ["All Cities (National Aggregate)"] + sorted(df['City'].unique().tolist())
    selected_city = st.selectbox("Filter Telemetry by City / Region:", cities, index=0)
    
    if selected_city != "All Cities (National Aggregate)":
        filtered_df = df[df['City'] == selected_city].copy()
    else:
        filtered_df = df.copy()
        
    # Compute Key KPI Statistics
    avg_aqi = filtered_df['AQI'].mean()
    max_aqi = filtered_df['AQI'].max()
    min_aqi = filtered_df['AQI'].min()
    total_obs = len(filtered_df)
    
    # City-level metrics if aggregate
    city_means = df.groupby('City')['AQI'].mean()
    most_polluted = city_means.idxmax()
    cleanest_city = city_means.idxmin()
    
    # 5 KPI Cards in responsive columns
    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        render_html(render_stat_card(
            label="Average AQI",
            value=f"{avg_aqi:.1f}",
            icon="📊",
            unit="Index"
        ))
        
    with c2:
        render_html(render_stat_card(
            label="Peak Recorded AQI",
            value=f"{max_aqi:.0f}",
            icon="🚨",
            unit="Max"
        ))
        
    with c3:
        render_html(render_stat_card(
            label="Minimum AQI",
            value=f"{min_aqi:.0f}",
            icon="🌱",
            unit="Min"
        ))
        
    with c4:
        render_html(render_stat_card(
            label="Monitored Days",
            value=f"{total_obs:,}",
            icon="📅",
            unit="Records"
        ))
        
    with c5:
        if selected_city == "All Cities (National Aggregate)":
            render_html(render_stat_card(
                label="Most Impacted City",
                value=most_polluted,
                icon="🏭",
                unit=f"({city_means[most_polluted]:.0f} AQI)"
            ))
        else:
            pct_good_sat = ((filtered_df['AQI_Bucket'].isin(['Good', 'Satisfactory'])).sum() / total_obs) * 100
            render_html(render_stat_card(
                label="Clean Air Share",
                value=f"{pct_good_sat:.1f}%",
                icon="🍃",
                unit="Good/Sat"
            ))
            
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # Row 1 of Charts: Trend over time
    with st.container(border=True):
        fig_trend = plot_aqi_trend(df, city=selected_city)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Row 2 of Charts: Distribution & Categories
    col_dist, col_donut = st.columns([1.3, 1])
    
    with col_dist:
        with st.container(border=True):
            fig_dist = plot_aqi_distribution(filtered_df)
            st.plotly_chart(fig_dist, use_container_width=True)
        
    with col_donut:
        with st.container(border=True):
            fig_donut = plot_aqi_category_donut(filtered_df)
            st.plotly_chart(fig_donut, use_container_width=True)
        
    # Row 3 of Charts: City Ranking & Pollutant Comparison
    col_rank, col_poll = st.columns([1.1, 1.1])
    
    with col_rank:
        with st.container(border=True):
            fig_rank = plot_city_aqi_ranking(df)
            st.plotly_chart(fig_rank, use_container_width=True)
        
    with col_poll:
        with st.container(border=True):
            fig_poll = plot_pollutant_concentration_comparison(filtered_df)
            st.plotly_chart(fig_poll, use_container_width=True)
