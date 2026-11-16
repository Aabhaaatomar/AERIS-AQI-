"""
AERIS 2.0 - Prediction Service
Handles machine learning model inference, parameter extraction from natural language,
CPCB category resolution, and model metadata.
"""

import os
import re
import sys
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from config import calculate_sub_index, get_category_info

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(BASE_DIR, "models")

@st.cache_resource
def get_trained_models():
    """Load serialized models from disk once and cache in memory."""
    models = {}
    model_files = {
        'Random Forest': 'random_forest.joblib',
        'Decision Tree': 'decision_tree.joblib',
        'Linear Regression': 'linear_regression.joblib'
    }
    
    # Auto-train fallback if models are missing
    rf_path = os.path.join(MODELS_DIR, 'random_forest.joblib')
    if not os.path.exists(rf_path):
        try:
            if BASE_DIR not in sys.path:
                sys.path.insert(0, BASE_DIR)
            from train_models import train_and_evaluate
            train_and_evaluate()
        except Exception as e:
            st.error(f"Error training models: {e}")
            
    for label, fname in model_files.items():
        path = os.path.join(MODELS_DIR, fname)
        if os.path.exists(path):
            models[label] = joblib.load(path)
            
    return models

def predict_aqi(pm25, pm10, no2, so2, co, o3, model_name="Random Forest"):
    """
    Run prediction using the trained Scikit-learn model.
    Returns predicted AQI, category, sub-indices, and dominant pollutant.
    """
    models = get_trained_models()
    
    # Normalize model name lookup
    target_key = "Random Forest"
    for k in models.keys():
        if model_name.lower() in k.lower():
            target_key = k
            break
            
    model = models.get(target_key)
    if model is None and len(models) > 0:
        model = list(models.values())[0]
        target_key = list(models.keys())[0]
        
    if model is None:
        return {"success": False, "error": "No trained ML model available."}
        
    features = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
    input_df = pd.DataFrame([[pm25, pm10, no2, so2, co, o3]], columns=features)
    
    raw_pred = model.predict(input_df)[0]
    predicted_aqi = max(0.0, min(500.0, round(float(raw_pred), 1)))
    
    sub_indices = {
        'PM2.5': calculate_sub_index(pm25, 'PM2.5'),
        'PM10': calculate_sub_index(pm10, 'PM10'),
        'NO2': calculate_sub_index(no2, 'NO2'),
        'SO2': calculate_sub_index(so2, 'SO2'),
        'CO': calculate_sub_index(co, 'CO'),
        'O3': calculate_sub_index(o3, 'O3')
    }
    dominant_pollutant = max(sub_indices, key=sub_indices.get)
    cat_info = get_category_info(predicted_aqi)
    
    return {
        "success": True,
        "model_used": target_key,
        "predicted_aqi": predicted_aqi,
        "category": cat_info["name"],
        "color": cat_info["color"],
        "icon": cat_info["icon"],
        "dominant_pollutant": dominant_pollutant,
        "dominant_sub_index": sub_indices[dominant_pollutant],
        "sub_indices": sub_indices,
        "summary": cat_info["summary"],
        "general_advisory": cat_info["general_advisory"],
        "sensitive_advisory": cat_info["sensitive_advisory"],
        "action": cat_info["action"],
        "inputs": {
            "PM2.5": pm25, "PM10": pm10, "NO2": no2, "SO2": so2, "CO": co, "O3": o3
        }
    }

def extract_pollutants_from_text(text):
    """
    Intelligently extracts numerical values for PM2.5, PM10, NO2, SO2, CO, O3
    from conversational user messages like:
    'predict AQI for PM2.5 = 80, PM10 = 150, NO2 = 40, SO2 = 20, CO = 1.2 and O3 = 35'
    """
    patterns = {
        'PM2.5': r'(?:pm\s*2\.?5|pm25)[\s:=]+([0-9]+(?:\.[0-9]+)?)',
        'PM10': r'(?:pm\s*10|pm10)[\s:=]+([0-9]+(?:\.[0-9]+)?)',
        'NO2': r'(?:no\s*2|no2)[\s:=]+([0-9]+(?:\.[0-9]+)?)',
        'SO2': r'(?:so\s*2|so2)[\s:=]+([0-9]+(?:\.[0-9]+)?)',
        'CO': r'(?:co)[\s:=]+([0-9]+(?:\.[0-9]+)?)',
        'O3': r'(?:o\s*3|o3|ozone)[\s:=]+([0-9]+(?:\.[0-9]+)?)'
    }
    
    extracted = {}
    text_lower = text.lower()
    for param, pat in patterns.items():
        m = re.search(pat, text_lower)
        if m:
            try:
                extracted[param] = float(m.group(1))
            except ValueError:
                pass
                
    return extracted
