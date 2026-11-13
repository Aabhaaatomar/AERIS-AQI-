"""
AERIS - Air Quality Intelligence System
Dataset Generator for Indian CPCB Multi-City Air Quality Telemetry
Generates realistic multi-city, multi-season daily observations compliant with
official CPCB sub-index calculation guidelines.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Official CPCB Breakpoints for Sub-index calculation
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
    if pd.isna(conc) or conc < 0:
        return 0
    breakpoints = CPCB_BREAKPOINTS[pollutant]
    for b_low, b_high, i_low, i_high in breakpoints:
        if b_low <= conc <= b_high:
            sub = i_low + ((i_high - i_low) / (b_high - b_low)) * (conc - b_low)
            return round(sub, 2)
    # Beyond highest breakpoint, linearly extrapolate up to 500 max
    b_low, b_high, i_low, i_high = breakpoints[-1]
    if conc > b_high:
        return 500.0
    return 0.0

def get_aqi_category(aqi_val):
    """Categorize AQI value into official Indian CPCB buckets."""
    if aqi_val <= 50:
        return 'Good'
    elif aqi_val <= 100:
        return 'Satisfactory'
    elif aqi_val <= 200:
        return 'Moderate'
    elif aqi_val <= 300:
        return 'Poor'
    elif aqi_val <= 400:
        return 'Very Poor'
    else:
        return 'Severe'

def generate_cpcb_dataset():
    np.random.seed(42)
    
    cities = [
        {"name": "Delhi", "base_pm25": 115, "base_pm10": 210, "base_no2": 52, "base_so2": 18, "base_co": 1.6, "base_o3": 45, "winter_factor": 2.2, "monsoon_factor": 0.45},
        {"name": "Mumbai", "base_pm25": 48, "base_pm10": 98, "base_no2": 38, "base_so2": 15, "base_co": 1.1, "base_o3": 35, "winter_factor": 1.4, "monsoon_factor": 0.50},
        {"name": "Bengaluru", "base_pm25": 36, "base_pm10": 72, "base_no2": 28, "base_so2": 10, "base_co": 0.8, "base_o3": 32, "winter_factor": 1.25, "monsoon_factor": 0.60},
        {"name": "Kolkata", "base_pm25": 82, "base_pm10": 155, "base_no2": 45, "base_so2": 22, "base_co": 1.3, "base_o3": 38, "winter_factor": 2.0, "monsoon_factor": 0.40},
        {"name": "Hyderabad", "base_pm25": 46, "base_pm10": 92, "base_no2": 32, "base_so2": 12, "base_co": 0.9, "base_o3": 36, "winter_factor": 1.35, "monsoon_factor": 0.55},
        {"name": "Chennai", "base_pm25": 42, "base_pm10": 85, "base_no2": 26, "base_so2": 11, "base_co": 0.85, "base_o3": 34, "winter_factor": 1.2, "monsoon_factor": 0.70},
        {"name": "Ahmedabad", "base_pm25": 78, "base_pm10": 160, "base_no2": 48, "base_so2": 28, "base_co": 1.4, "base_o3": 42, "winter_factor": 1.65, "monsoon_factor": 0.50},
        {"name": "Lucknow", "base_pm25": 105, "base_pm10": 195, "base_no2": 42, "base_so2": 16, "base_co": 1.5, "base_o3": 40, "winter_factor": 2.1, "monsoon_factor": 0.42},
        {"name": "Jaipur", "base_pm25": 65, "base_pm10": 150, "base_no2": 35, "base_so2": 14, "base_co": 1.0, "base_o3": 38, "winter_factor": 1.5, "monsoon_factor": 0.55},
        {"name": "Pune", "base_pm25": 45, "base_pm10": 88, "base_no2": 30, "base_so2": 13, "base_co": 0.9, "base_o3": 36, "winter_factor": 1.3, "monsoon_factor": 0.52}
    ]
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    total_days = (end_date - start_date).days + 1
    
    records = []
    
    for c in cities:
        for d in range(total_days):
            current_date = start_date + timedelta(days=d)
            month = current_date.month
            day_of_year = current_date.timetuple().tm_yday
            
            # Seasonal factor calculation
            # Nov, Dec, Jan, Feb -> Winter
            # Jul, Aug, Sep -> Monsoon (washout effect)
            # Mar, Apr, May -> Summer/Pre-monsoon (high O3, dust)
            # Oct -> Post-monsoon
            if month in [11, 12, 1, 2]:
                season_mult = c["winter_factor"] * (1.0 + 0.15 * np.cos(2 * np.pi * (day_of_year - 15) / 365))
            elif month in [6, 7, 8, 9]:
                season_mult = c["monsoon_factor"] * (1.0 + 0.1 * np.sin(2 * np.pi * (day_of_year - 180) / 365))
            elif month in [3, 4, 5]:
                season_mult = 1.05 + 0.1 * np.sin(2 * np.pi * day_of_year / 365)
            else: # October
                season_mult = 1.35
            
            # Weekly variation (weekends slightly lower industrial/traffic)
            dow = current_date.weekday()
            dow_mult = 0.92 if dow in [5, 6] else 1.02
            
            # Atmospheric random shock (representing weather inversion or high winds)
            weather_shock = np.random.lognormal(mean=0, sigma=0.18)
            
            # Base concentrations with realistic physical correlations
            pm25 = max(5.0, round(c["base_pm25"] * season_mult * dow_mult * weather_shock + np.random.normal(0, 4), 1))
            
            # PM10 is correlated with PM2.5 + road dust / construction
            pm10_ratio = np.random.uniform(1.6, 2.1)
            pm10 = max(pm25 + 5.0, round(pm25 * pm10_ratio + (15.0 if month in [3, 4, 5] else 0) + np.random.normal(0, 6), 1))
            
            # NO2 - Combustion, traffic
            no2 = max(5.0, round(c["base_no2"] * season_mult * dow_mult * (0.8 + 0.4 * weather_shock) + np.random.normal(0, 3), 1))
            
            # SO2 - Industrial, thermal power
            so2 = max(3.0, round(c["base_so2"] * (1.0 + 0.2 * (season_mult - 1.0)) * (0.85 + 0.3 * weather_shock) + np.random.normal(0, 2), 1))
            
            # CO - Incomplete combustion (traffic & heating)
            co = max(0.2, round(c["base_co"] * season_mult * dow_mult * (0.85 + 0.3 * weather_shock) + np.random.normal(0, 0.08), 2))
            
            # O3 - Higher in sunny summer months, photochemical
            o3_season = 1.35 if month in [3, 4, 5, 10] else (0.8 if month in [7, 8] else 1.0)
            o3 = max(8.0, round(c["base_o3"] * o3_season * (0.85 + 0.3 * np.random.rand()) + np.random.normal(0, 3), 1))
            
            # Compute CPCB Sub-indices
            si_pm25 = calculate_sub_index(pm25, 'PM2.5')
            si_pm10 = calculate_sub_index(pm10, 'PM10')
            si_no2 = calculate_sub_index(no2, 'NO2')
            si_so2 = calculate_sub_index(so2, 'SO2')
            si_co = calculate_sub_index(co, 'CO')
            si_o3 = calculate_sub_index(o3, 'O3')
            
            sub_indices = [si_pm25, si_pm10, si_no2, si_so2, si_co, si_o3]
            calculated_aqi = round(max(sub_indices), 1)
            
            # Identify dominant pollutant responsible for max sub-index
            pollutant_names = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
            dominant_pollutant = pollutant_names[np.argmax(sub_indices)]
            
            aqi_bucket = get_aqi_category(calculated_aqi)
            
            records.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'City': c["name"],
                'PM2.5': pm25,
                'PM10': pm10,
                'NO2': no2,
                'SO2': so2,
                'CO': co,
                'O3': o3,
                'AQI': calculated_aqi,
                'AQI_Bucket': aqi_bucket,
                'Dominant_Pollutant': dominant_pollutant
            })
            
    df = pd.DataFrame(records)
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "city_day_cpcb.csv")
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records across {len(cities)} cities saved to {output_path}")
    print("AQI Bucket breakdown:")
    print(df['AQI_Bucket'].value_counts())
    print("\nSample records:")
    print(df.head())

if __name__ == '__main__':
    generate_cpcb_dataset()
