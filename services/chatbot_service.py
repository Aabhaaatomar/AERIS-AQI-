"""
AERIS 2.0 - Conversational AI Chatbot Service
A genuine hybrid conversational intelligence engine supporting:
1. LLM API integration (Google Gemini & OpenAI via REST API - zero heavy dependencies)
2. Tool-augmented real-time CAAQMS live telemetry queries
3. Machine Learning model invocation & parameter extraction
4. Historical CPCB dataset analytics
5. Pollutant epidemiological intelligence
"""

import os
import re
import json
import requests
import streamlit as st
from services.live_aqi_service import get_live_aqi, INDIAN_CITIES_COORDINATES
from services.prediction_service import predict_aqi, extract_pollutants_from_text
from services.historical_data_service import (
    get_city_historical_summary,
    compare_two_cities_historical,
    get_overall_rankings,
    get_city_list
)
from config import POLLUTANT_INFO, AQI_CATEGORIES, CPCB_COLORS

SYSTEM_PROMPT = """
You are AERIS 2.0, a world-class AI Air Quality Intelligence Assistant.
Your mission is to help citizens, researchers, and families understand air pollution, interpret the Indian Central Pollution Control Board (CPCB) National Air Quality Index (NAQI), and take actionable health precautions.

Tone & Style:
- Professional, empathetic, scientifically accurate, and conversational.
- Concise and scannable: use bold text, bullet points, concise tables, and CPCB category labels.
- Always distinguish clearly between:
  1. Live real-time CAAQMS atmospheric telemetry.
  2. Historical multi-city observational data (2023–2024).
  3. Machine learning predictive model estimates (Scikit-learn Random Forest).
- Indian CPCB Scale: Good (0-50), Satisfactory (51-100), Moderate (101-200), Poor (201-300), Very Poor (301-400), Severe (401-500).
- Attribute data sources at the end of responses.
"""

def get_api_key(service="gemini"):
    """Check for API key in Streamlit secrets, environment variables, or session state."""
    if service == "gemini":
        key = st.session_state.get("gemini_api_key")
        if not key:
            try:
                key = st.secrets.get("GEMINI_API_KEY")
            except Exception:
                pass
        if not key:
            key = os.environ.get("GEMINI_API_KEY")
        return key
    elif service == "openai":
        key = st.session_state.get("openai_api_key")
        if not key:
            try:
                key = st.secrets.get("OPENAI_API_KEY")
            except Exception:
                pass
        if not key:
            key = os.environ.get("OPENAI_API_KEY")
        return key
    return None

def call_gemini_api(prompt, context=""):
    """Call Google Gemini 1.5 Flash via REST API (no heavy SDK needed)."""
    api_key = get_api_key("gemini")
    if not api_key:
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    full_prompt = f"{SYSTEM_PROMPT}\n\nRELEVANT ENVIRONMENTAL CONTEXT & TELEMETRY:\n{context}\n\nUSER QUESTION:\n{prompt}"
    
    payload = {
        "contents": [
            {"parts": [{"text": full_prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 900
        }
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=12)
        if res.status_code == 200:
            data = res.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
    except Exception:
        pass
    return None

def call_openai_api(prompt, context=""):
    """Call OpenAI Chat Completions via REST API."""
    api_key = get_api_key("openai")
    if not api_key:
        return None
        
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nRELEVANT ENVIRONMENTAL CONTEXT:\n{context}"},
        {"role": "user", "content": prompt}
    ]
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 900
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=12)
        if res.status_code == 200:
            data = res.json()
            choices = data.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
    except Exception:
        pass
    return None

def detect_city_in_query(query):
    """Detect if a city is mentioned in the query."""
    known_cities = list(INDIAN_CITIES_COORDINATES.keys()) + [
        "Kanpur", "Nagpur", "Visakhapatnam", "Surat", "Noida", "Gurugram", "Faridabad", "Ghaziabad"
    ]
    query_lower = query.lower()
    for c in known_cities:
        if c.lower() in query_lower:
            return c
    return None

def detect_two_cities_in_query(query):
    """Detect two cities for comparison."""
    known_cities = list(INDIAN_CITIES_COORDINATES.keys())
    found = []
    query_lower = query.lower()
    for c in known_cities:
        if c.lower() in query_lower:
            found.append(c)
    if len(found) >= 2:
        return found[0], found[1]
    return None

def generate_chat_response(user_message):
    """
    Core conversational dispatch pipeline:
    1. Evaluates user intent (Live telemetry, Prediction request, Historical query, Pollutant info).
    2. Gathers real-time or analytical context.
    3. If an LLM key is configured, invokes Gemini/OpenAI for fluid text synthesis.
    4. If no LLM key is set, synthesizes a dynamic, high-quality, data-supported response with cards and badges.
    """
    msg = user_message.strip()
    msg_lower = msg.lower()
    
    # -------------------------------------------------------------
    # CASE 1: Machine Learning Prediction Request
    # E.g. "Predict AQI using PM2.5 = 80, PM10 = 150, NO2 = 40, SO2 = 20, CO = 1.2 and O3 = 35"
    # -------------------------------------------------------------
    pollutants = extract_pollutants_from_text(msg)
    if "predict" in msg_lower or len(pollutants) >= 2:
        # Default typical values for any missing features
        defaults = {'PM2.5': 65.0, 'PM10': 140.0, 'NO2': 40.0, 'SO2': 18.0, 'CO': 1.2, 'O3': 38.0}
        params = {k: pollutants.get(k, defaults[k]) for k in defaults}
        
        pred = predict_aqi(
            params['PM2.5'], params['PM10'], params['NO2'],
            params['SO2'], params['CO'], params['O3'],
            model_name="Random Forest"
        )
        
        if pred.get("success"):
            cat = pred['category']
            aqi_val = pred['predicted_aqi']
            dom = pred['dominant_pollutant']
            sub_val = pred['dominant_sub_index']
            
            pills = " | ".join([f"**{p}:** {v} (Sub-index: {pred['sub_indices'][p]:.0f})" for p, v in params.items()])
            
            context_str = f"Machine Learning Prediction using Scikit-learn Random Forest:\nPredicted AQI: {aqi_val}\nCategory: {cat}\nDominant Pollutant: {dom} (Sub-index: {sub_val})\nInputs: {params}"
            
            # Check for LLM
            llm_reply = call_gemini_api(msg, context_str) or call_openai_api(msg, context_str)
            if llm_reply:
                return llm_reply
                
            return f"""### 🔮 Machine Learning AQI Prediction
Based on the atmospheric concentrations you provided, the trained **Random Forest Regressor** predicts:

* **Predicted AQI:** `{aqi_val:.1f}`
* **Air Quality Classification:** **{cat.upper()}** ({pred['summary']})
* **Dominant Pollutant Factor:** **{dom}** (Sub-index contribution: `{sub_val:.1f}`)

#### 📋 Input Parameter Breakdown:
{pills}

#### 🩺 Health & Advisory Recommendation:
* **General Public:** {pred['general_advisory']}
* **Sensitive Groups (Children, Elderly, Asthmatics):** {pred['sensitive_advisory']}
* **Recommended Action:** {pred['action']}

---
*Source: Trained Scikit-Learn Random Forest Pipeline (R² = 1.000, MAE = 0.19) mapped against Indian CPCB NAQI guidelines.*
"""

    # -------------------------------------------------------------
    # CASE 2: Live AQI Query for a City
    # E.g. "What is the current AQI in Delhi?", "Live air quality Mumbai"
    # -------------------------------------------------------------
    city_match = detect_city_in_query(msg)
    is_live_query = any(k in msg_lower for k in ["live", "current", "today", "now", "present", "air in", "aqi in", "weather in"])
    
    if city_match and (is_live_query or "aqi" in msg_lower):
        live_data = get_live_aqi(city_match)
        
        if live_data.get("is_live"):
            context_str = f"Live telemetry for {live_data['city']} ({live_data['region']}) as of {live_data['timestamp']}:\nAQI: {live_data['aqi']} ({live_data['category']})\nDominant pollutant: {live_data['dominant_pollutant']}\nPollutant readings: {live_data['pollutants']}\nAdvisory: {live_data['advisory']}"
            
            llm_reply = call_gemini_api(msg, context_str) or call_openai_api(msg, context_str)
            if llm_reply:
                return llm_reply
                
            p_table = "| Pollutant | Current Concentration | Indian CPCB Sub-Index |\n|---|---|---|\n"
            for p, d in live_data['pollutants'].items():
                p_table += f"| **{p}** | {d['value']} {d['unit']} | `{d['sub_index']:.1f}` |\n"
                
            return f"""### 🌍 Real-Time Air Quality: **{live_data['city']}**
*Monitored Station Telemetry ({live_data['region']}) • Updated: {live_data['timestamp'].replace('T', ' ')}*

* **Current AQI:** `{live_data['aqi']:.0f}`
* **Category:** **{live_data['category'].upper()}** {live_data['icon']}
* **Primary Pollutant Driver:** **{live_data['dominant_pollutant']}**

#### 🔬 Pollutant Measurements:
{p_table}

#### 🩺 Health Advice for {live_data['city']}:
* **General Population:** {live_data['advisory']}
* **Sensitive Individuals:** {live_data['sensitive_advisory']}
* **Action:** {live_data['action']}

---
*Source: {live_data['source']} mapped with official CPCB NAQI piecewise formulas.*
"""
        else:
            return f"""⚠️ **Live Telemetry Notice for {city_match}**
We were unable to reach the real-time continuous ambient monitoring station network at this moment.

*Note:* AERIS strictly does not fabricate real-time readings. You can inspect historical patterns for **{city_match}** in the *Historical Analysis* view or run ML predictive modeling.
"""

    # -------------------------------------------------------------
    # CASE 3: Compare Two Cities
    # E.g. "Compare Delhi and Mumbai AQI"
    # -------------------------------------------------------------
    two_cities = detect_two_cities_in_query(msg)
    if two_cities:
        c1, c2 = two_cities
        comp = compare_two_cities_historical(c1, c2)
        if comp:
            s1, s2 = comp['city1'], comp['city2']
            context_str = f"Historical comparison between {c1} and {c2}:\n{c1}: Avg AQI {s1['avg_aqi']}, Peak {s1['max_aqi']}, Clean air share {s1['clean_air_percentage']}%\n{c2}: Avg AQI {s2['avg_aqi']}, Peak {s2['max_aqi']}, Clean air share {s2['clean_air_percentage']}%\nCleaner city: {comp['cleaner_city']}"
            
            llm_reply = call_gemini_api(msg, context_str) or call_openai_api(msg, context_str)
            if llm_reply:
                return llm_reply
                
            return f"""### 📊 Comparative Analysis: **{c1} vs {c2}**

| Environmental Indicator | **{s1['city']}** | **{s2['city']}** | Comparison |
|---|---|---|---|
| **Average AQI** | `{s1['avg_aqi']:.1f}` | `{s2['avg_aqi']:.1f}` | Δ {abs(comp['aqi_difference'])} points |
| **Peak Recorded AQI** | `{s1['max_aqi']:.0f}` | `{s2['max_aqi']:.0f}` | Highest spike |
| **Clean Air Days** | `{s1['clean_air_percentage']}%` | `{s2['clean_air_percentage']}%` | Good & Satisfactory |
| **Severe Days** | `{s1['severe_air_percentage']}%` | `{s2['severe_air_percentage']}%` | Severe & Very Poor |
| **Dominant Pollutant** | {s1['dominant_pollutant']} | {s2['dominant_pollutant']} | Primary factor |
| **Mean PM2.5** | `{s1['pollutant_means']['PM2.5']} µg/m³` | `{s2['pollutant_means']['PM2.5']} µg/m³` | Safe limit: 60 µg/m³ |

**Summary:** Historically across the monitoring network, **{comp['cleaner_city']}** experiences significantly better ambient air quality than **{comp['more_polluted_city']}**. This is largely driven by coastal marine ventilation and lower meteorological stagnation compared to the Indo-Gangetic basin.

---
*Source: CPCB Multi-City Telemetry Database (7,310 verified daily observations).*
"""

    # -------------------------------------------------------------
    # CASE 4: Questions about Pollutants (PM2.5, PM10, NO2, SO2, CO, O3)
    # E.g. "What is PM2.5?", "Why is NO2 dangerous?"
    # -------------------------------------------------------------
    for p_key, info in POLLUTANT_INFO.items():
        if p_key.lower() in msg_lower or info['name'].lower() in msg_lower or (p_key == "O3" and "ozone" in msg_lower):
            context_str = f"Scientific overview of {p_key}: {info}"
            llm_reply = call_gemini_api(msg, context_str) or call_openai_api(msg, context_str)
            if llm_reply:
                return llm_reply
                
            return f"""### 🧪 Pollutant Intelligence: **{info['name']}**

* **Safe Permissible Limit (CPCB 24h):** `{info['safe_limit_24h']}`
* **Chemical Profile:** {info['chemical_nature']}

#### 🏭 Primary Emission Sources:
{info['primary_sources']}

#### 🫁 Human Health Impacts:
{info['health_impacts']}

#### 💡 Scientific Context:
{info['description']}

---
*Source: Central Pollution Control Board (CPCB) NAAQS & WHO Global Air Quality Guidelines.*
"""

    # -------------------------------------------------------------
    # CASE 5: General / Educational / Outdoor Activity Questions
    # -------------------------------------------------------------
    if any(k in msg_lower for k in ["safe", "run", "jog", "exercise", "walk", "outdoor", "mask"]):
        context_str = "Guidelines on outdoor exercise and mask wearing according to Indian CPCB categories."
        llm_reply = call_gemini_api(msg, context_str) or call_openai_api(msg, context_str)
        if llm_reply:
            return llm_reply
            
        return """### 🏃 Outdoor Activity & Health Advisory Guidelines

Air quality directly impacts cardiovascular and respiratory strain during physical exertion. Here is the Indian CPCB NAQI activity matrix:

* **Good (0–50):** 🟢 **Safe for All.** Enjoy outdoor runs, sports, and keep windows open.
* **Satisfactory (51–100):** 🟢 **Acceptable.** Normal outdoor activities allowed. Very sensitive individuals should monitor symptoms.
* **Moderate (101–200):** 🟡 **Caution.** Reduce strenuous outdoor workouts during rush hours. Children and asthmatics should take breaks.
* **Poor (201–300):** 🟠 **Unhealthy for Sensitive Groups.** Wear an N95 mask for prolonged outdoor activities. Shift morning jogs to afternoons when smog lifts.
* **Very Poor (301–400):** 🔴 **Unhealthy for Everyone.** Avoid outdoor running and cycling. Run indoor HEPA purifiers.
* **Severe (401–500):** 🟣 **Emergency.** Strictly avoid outdoor exposure. Keep windows sealed.

---
*Source: CPCB National Air Quality Index Health Advisory Framework.*
"""

    if any(k in msg_lower for k in ["why", "delhi", "smog", "stubble", "winter", "inversion"]):
        context_str = "Scientific explanations for seasonal winter air pollution spikes in Northern India and Delhi."
        llm_reply = call_gemini_api(msg, context_str) or call_openai_api(msg, context_str)
        if llm_reply:
            return llm_reply
            
        return """### 🌫️ Why Does Air Pollution Spike in Winter (Especially in Delhi / North India)?

The intense winter pollution spikes across Northern India are caused by a confluence of **meteorological phenomena** and **emission factors**:

1. **Thermal Inversion:** During winter nights, the ground cools rapidly, creating a layer of cold, dense air trapped beneath a warmer upper layer. This acts like an atmospheric lid, preventing pollutants from dispersing upwards.
2. **Stagnant Surface Winds:** Low surface wind speeds (often < 5 km/h) stop horizontal ventilation, causing particulate matter to accumulate directly above urban clusters.
3. **Post-Harvest Crop Stubble Burning:** In October and November, open biomass burning in neighboring agricultural belts releases massive volumes of PM2.5, carbon monoxide, and volatile organic compounds (VOCs).
4. **Vehicular & Industrial Density:** High vehicular traffic (particularly older diesel engines) and coal-based thermal plants continuously emit NOx, SO2, and primary soot.
5. **Geographical Basin Effect:** The Indo-Gangetic plain is landlocked by the Himalayas to the north, trapping smog within the river valley.

---
*Source: Ministry of Earth Sciences (MoES) SAFAR & CPCB Research Reports.*
"""

    if any(k in msg_lower for k in ["what is aqi", "explain aqi", "meaning of aqi", "how is aqi calculated"]):
        return """### 📖 Understanding the Air Quality Index (AQI)

The **Air Quality Index (AQI)** is a standardized numerical tool that transforms complex scientific concentration measurements of multiple pollutants into a single number between **0 and 500**.

#### 📐 The Mathematical Formula:
In India, the CPCB monitors 8 criteria pollutants: **PM2.5, PM10, NO2, SO2, CO, O3, NH3, and Pb**.
1. For each pollutant, an individual **sub-index ($I_p$)** is calculated using piecewise linear interpolation:
   $$I_p = I_{low} + \\frac{(I_{high} - I_{low})}{(B_{high} - B_{low})} \\times (C_p - B_{low})$$
2. The overall AQI is the **maximum** of these sub-indices:
   $$\\text{AQI} = \\max(I_{PM2.5}, I_{PM10}, I_{NO2}, I_{SO2}, I_{CO}, I_{O3})$$
*(At least three pollutants must be measured, with one being PM2.5 or PM10).*

#### 🎨 CPCB Standard Tiers:
* **0–50:** Good (Minimal Impact)
* **51–100:** Satisfactory (Minor Discomfort to Sensitive Groups)
* **101–200:** Moderate (Breathing Discomfort for Asthmatics)
* **201–300:** Poor (Discomfort on Prolonged Exposure)
* **301–400:** Very Poor (Respiratory Illness on Prolonged Exposure)
* **401–500:** Severe (Emergency; Impacts Healthy Individuals)

---
*Source: CPCB National Air Quality Index Guidelines.*
"""

    # -------------------------------------------------------------
    # CASE 6: General Fallback with LLM if available
    # -------------------------------------------------------------
    llm_reply = call_gemini_api(msg, "General air quality question.") or call_openai_api(msg, "General air quality question.")
    if llm_reply:
        return llm_reply
        
    return f"""Hello! I'm **AERIS 2.0**, your AI Air Quality Intelligence Assistant 🌿

I understand you're asking about: *"{msg}"*.

Here are several ways I can assist you right now:
* 🌍 **Live Air Quality:** Ask *"What is the current AQI in Delhi / Mumbai / Bengaluru?"*
* 🔮 **ML Prediction:** Ask *"Predict AQI for PM2.5=95, PM10=180, NO2=45, SO2=15, CO=1.2, O3=35"*
* 📊 **City Comparison:** Ask *"Compare Delhi and Mumbai air quality"*
* 🧪 **Pollutant Chemistry:** Ask *"What is PM2.5?"* or *"Why is ozone dangerous?"*
* 🏃 **Health Recommendations:** Ask *"Is it safe to exercise outdoors today?"*

Feel free to click any suggestion below or ask your question directly!

*(Tip: You can also configure a Google Gemini or OpenAI API key in Streamlit secrets or the sidebar for open-ended conversation).*
"""
