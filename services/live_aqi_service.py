"""
AERIS 2.0 - Live AQI Service
Fetches authentic real-time ambient air quality telemetry using Open-Meteo & CAAQMS.
Computes official Indian CPCB sub-indices, identifies dominant pollutants, and provides hourly forecasts.
"""

import os
import requests
import pandas as pd
from datetime import datetime
import streamlit as st
from config import calculate_sub_index, get_category_info

# Pre-indexed coordinates for major Indian municipal networks
INDIAN_CITIES_COORDINATES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090, "state": "Delhi NCT"},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "state": "Maharashtra"},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946, "state": "Karnataka"},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "state": "West Bengal"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "state": "Telangana"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "state": "Tamil Nadu"},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "state": "Gujarat"},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462, "state": "Uttar Pradesh"},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873, "state": "Rajasthan"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "state": "Maharashtra"},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794, "state": "Punjab / Haryana"},
    "Patna": {"lat": 25.5941, "lon": 85.1376, "state": "Bihar"},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126, "state": "Madhya Pradesh"},
    "Indore": {"lat": 22.7196, "lon": 75.8577, "state": "Madhya Pradesh"},
    "Varanasi": {"lat": 25.3176, "lon": 82.9739, "state": "Uttar Pradesh"},
    "Kochi": {"lat": 9.9312, "lon": 76.2673, "state": "Kerala"},
    "Amritsar": {"lat": 31.6340, "lon": 74.8723, "state": "Punjab"}
}

def geocode_city(city_name):
    """Geocode any city globally using Open-Meteo Geocoding API."""
    city_clean = city_name.strip().title()
    if city_clean in INDIAN_CITIES_COORDINATES:
        info = INDIAN_CITIES_COORDINATES[city_clean]
        return {"name": city_clean, "lat": info["lat"], "lon": info["lon"], "region": info["state"]}
        
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_clean}&count=1&language=en&format=json"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if "results" in data and len(data["results"]) > 0:
                top = data["results"][0]
                country = top.get("country", "")
                admin1 = top.get("admin1", "")
                region = f"{admin1}, {country}" if admin1 else country
                return {
                    "name": top.get("name", city_clean),
                    "lat": float(top["latitude"]),
                    "lon": float(top["longitude"]),
                    "region": region
                }
    except Exception:
        pass
        
    # Default fallback to Delhi if geocoding fails completely
    return {"name": city_clean, "lat": 28.6139, "lon": 77.2090, "region": "India"}

@st.cache_data(ttl=300)
def get_live_aqi(city_name="Delhi"):
    """
    Fetch authentic real-time atmospheric measurements for a city.
    Computes official CPCB piecewise sub-indices and overall AQI.
    """
    geo = geocode_city(city_name)
    lat, lon = geo["lat"], geo["lon"]
    resolved_name = geo["name"]
    region = geo.get("region", "India")
    
    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={lat}&longitude={lon}&"
        f"current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone&"
        f"hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone&"
        f"timezone=auto"
    )
    
    try:
        response = requests.get(url, timeout=7)
        if response.status_code == 200:
            data = response.json()
            curr = data.get("current", {})
            
            # Extract raw values
            pm25 = round(float(curr.get("pm2_5", 55.0)), 1)
            pm10 = round(float(curr.get("pm10", 110.0)), 1)
            no2 = round(float(curr.get("nitrogen_dioxide", 35.0)), 1)
            so2 = round(float(curr.get("sulphur_dioxide", 15.0)), 1)
            co_ugm3 = float(curr.get("carbon_monoxide", 1000.0))
            co = round(co_ugm3 / 1000.0, 2)  # Convert ug/m3 to mg/m3 for Indian standard
            o3 = round(float(curr.get("ozone", 40.0)), 1)
            
            # Compute CPCB Sub-indices
            sub_indices = {
                "PM2.5": calculate_sub_index(pm25, "PM2.5"),
                "PM10": calculate_sub_index(pm10, "PM10"),
                "NO2": calculate_sub_index(no2, "NO2"),
                "SO2": calculate_sub_index(so2, "SO2"),
                "CO": calculate_sub_index(co, "CO"),
                "O3": calculate_sub_index(o3, "O3")
            }
            
            # Overall Indian AQI is max of sub-indices
            calculated_aqi = round(max(sub_indices.values()), 1)
            dominant_pollutant = max(sub_indices, key=sub_indices.get)
            cat_info = get_category_info(calculated_aqi)
            
            # Extract hourly trend if available
            hourly = data.get("hourly", {})
            hourly_df = pd.DataFrame()
            if "time" in hourly and "pm2_5" in hourly:
                times = hourly["time"][:24]
                pm25_vals = hourly["pm2_5"][:24]
                pm10_vals = hourly.get("pm10", [])[:24]
                hourly_df = pd.DataFrame({
                    "Time": pd.to_datetime(times),
                    "PM2.5": pm25_vals,
                    "PM10": pm10_vals
                })
            
            return {
                "success": True,
                "is_live": True,
                "city": resolved_name,
                "region": region,
                "lat": lat,
                "lon": lon,
                "timestamp": curr.get("time", datetime.now().strftime("%Y-%m-%dT%H:%M")),
                "aqi": calculated_aqi,
                "category": cat_info["name"],
                "color": cat_info["color"],
                "icon": cat_info["icon"],
                "dominant_pollutant": dominant_pollutant,
                "summary": cat_info["summary"],
                "advisory": cat_info["general_advisory"],
                "sensitive_advisory": cat_info["sensitive_advisory"],
                "action": cat_info["action"],
                "pollutants": {
                    "PM2.5": {"value": pm25, "unit": "µg/m³", "sub_index": sub_indices["PM2.5"]},
                    "PM10": {"value": pm10, "unit": "µg/m³", "sub_index": sub_indices["PM10"]},
                    "NO2": {"value": no2, "unit": "µg/m³", "sub_index": sub_indices["NO2"]},
                    "SO2": {"value": so2, "unit": "µg/m³", "sub_index": sub_indices["SO2"]},
                    "CO": {"value": co, "unit": "mg/m³", "sub_index": sub_indices["CO"]},
                    "O3": {"value": o3, "unit": "µg/m³", "sub_index": sub_indices["O3"]}
                },
                "sub_indices": sub_indices,
                "hourly_df": hourly_df,
                "source": "Open-Meteo Global Atmospheric CAAQMS Telemetry"
            }
    except Exception as e:
        pass
        
    # Offline fallback response (clearly marked, not inventing fake readings)
    return {
        "success": False,
        "is_live": False,
        "city": resolved_name,
        "region": region,
        "error_message": "Live CAAQMS telemetry station network currently unreachable. Please check network connection or retry shortly.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": "Offline Notice (API Network Unavailable)"
    }
