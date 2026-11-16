"""
AERIS 2.0 - Historical Data Service
Queries the multi-city CPCB dataset (2023–2024), computes municipal summaries,
cross-city comparisons, seasonal dynamics, and pollutant correlations.
"""

import os
import pandas as pd
import numpy as np
import streamlit as st

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "city_day_cpcb.csv")

@st.cache_data
def load_historical_dataset():
    """Load and cache the Indian CPCB historical dataset."""
    if not os.path.exists(DATA_PATH):
        try:
            from data.generate_dataset import generate_cpcb_dataset
            generate_cpcb_dataset()
        except Exception:
            return pd.DataFrame()
            
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return pd.DataFrame()

def get_city_list():
    df = load_historical_dataset()
    if df.empty:
        return []
    return sorted(df['City'].unique().tolist())

def get_city_historical_summary(city_name):
    """Compute aggregate statistical summary for a specific city."""
    df = load_historical_dataset()
    if df.empty:
        return None
        
    sub = df[df['City'].str.lower() == city_name.strip().lower()]
    if sub.empty:
        return None
        
    total_days = len(sub)
    avg_aqi = round(float(sub['AQI'].mean()), 1)
    max_aqi = round(float(sub['AQI'].max()), 1)
    min_aqi = round(float(sub['AQI'].min()), 1)
    
    # Category percentages
    cat_counts = sub['AQI_Bucket'].value_counts()
    clean_days = int(cat_counts.get('Good', 0) + cat_counts.get('Satisfactory', 0))
    clean_pct = round((clean_days / total_days) * 100, 1)
    
    severe_days = int(cat_counts.get('Very Poor', 0) + cat_counts.get('Severe', 0))
    severe_pct = round((severe_days / total_days) * 100, 1)
    
    pollutant_means = {
        'PM2.5': round(float(sub['PM2.5'].mean()), 1),
        'PM10': round(float(sub['PM10'].mean()), 1),
        'NO2': round(float(sub['NO2'].mean()), 1),
        'SO2': round(float(sub['SO2'].mean()), 1),
        'CO': round(float(sub['CO'].mean()), 2),
        'O3': round(float(sub['O3'].mean()), 1)
    }
    
    # Dominant pollutant
    dominant = sub['Dominant_Pollutant'].mode()[0] if 'Dominant_Pollutant' in sub.columns else 'PM2.5'
    
    return {
        "city": sub['City'].iloc[0],
        "total_days": total_days,
        "avg_aqi": avg_aqi,
        "max_aqi": max_aqi,
        "min_aqi": min_aqi,
        "clean_air_percentage": clean_pct,
        "severe_air_percentage": severe_pct,
        "dominant_pollutant": dominant,
        "pollutant_means": pollutant_means
    }

def compare_two_cities_historical(city1, city2):
    """Compare two cities across historical records."""
    s1 = get_city_historical_summary(city1)
    s2 = get_city_historical_summary(city2)
    if not s1 or not s2:
        return None
    return {
        "city1": s1,
        "city2": s2,
        "aqi_difference": round(s1["avg_aqi"] - s2["avg_aqi"], 1),
        "cleaner_city": s1["city"] if s1["avg_aqi"] < s2["avg_aqi"] else s2["city"],
        "more_polluted_city": s1["city"] if s1["avg_aqi"] > s2["avg_aqi"] else s2["city"]
    }

def get_overall_rankings():
    """Rank cities by historical average AQI."""
    df = load_historical_dataset()
    if df.empty:
        return []
    ranks = df.groupby('City')['AQI'].agg(['mean', 'max', 'min']).reset_index()
    ranks = ranks.sort_values(by='mean', ascending=False)
    ranks['mean'] = ranks['mean'].round(1)
    ranks['max'] = ranks['max'].round(1)
    ranks['min'] = ranks['min'].round(1)
    return ranks.to_dict('records')
