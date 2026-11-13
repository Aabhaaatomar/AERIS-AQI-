# AERIS – Air Quality Intelligence System
> **"Understand the Air. Predict the Future."**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-12372A.svg)](https://www.python.org/)
[![Streamlit 1.54](https://img.shields.io/badge/Streamlit-1.54-1F8A70.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-B7E4C7.svg)](https://scikit-learn.org/)
[![CPCB NAQI Compliant](https://img.shields.io/badge/Standard-CPCB%20NAQI-16A34A.svg)](https://cpcb.nic.in/)

AERIS is an environmental intelligence and predictive analytics platform engineered to monitor ambient pollution levels, visualize multi-city environmental telemetry, analyze atmospheric criteria pollutants, and predict the Indian Air Quality Index (AQI) using trained machine learning algorithms.

Designed with a modern SaaS aesthetic, nature-inspired palette (Deep Forest Green, Emerald, Mint, Soft Sage), and mathematical rigor, AERIS bridges scientific accuracy with intuitive environmental communication.

---

## 🌟 Key Application Features

1. **Dashboard Overview**:
   - Executive telemetry cards (Average AQI, Peak AQI, Minimum AQI, Observations, Clean Air Share).
   - 7-Day Rolling Trendline with regulatory thresholds.
   - AQI distribution histogram with Indian CPCB category color bands.
   - CPCB Category Breakdown donut chart.
   - City-wise ranking across 10 major Indian municipal networks (Delhi, Mumbai, Bengaluru, Kolkata, etc.).
   - Mean pollutant concentration comparison.

2. **AQI Prediction Engine (Core Feature)**:
   - Interactive parameter input with physical units ($\mu\text{g/m}^3$, $\text{mg/m}^3$) for `PM2.5`, `PM10`, `NO2`, `SO2`, `CO`, `O3`.
   - Real-time model inference using serialized Scikit-learn pipelines (`Random Forest`, `Decision Tree`, `Linear Regression`).
   - One-click scenario presets: *Clean Mountain Air*, *Typical Urban Day*, *Winter Post-Harvest Smog*, *Heavy Industrial Belt*.
   - Dynamic semicircular gauge chart color-coded to the official Indian CPCB scale.
   - Automatic dominant pollutant identification and sub-index breakdown.
   - Comprehensive epidemiological health advisories tailored to general and sensitive populations.

3. **Air Quality Analysis**:
   - Full Pearson correlation matrix heatmap displaying atmospheric coupling.
   - Interactive scatter plots with Ordinary Least Squares (OLS) regression lines.
   - Seasonal and monthly cycle analysis detailing the winter inversion peak and monsoon precipitation washout.
   - Multi-pollutant boxplots illustrating dispersion and variance.

4. **Pollutant Insights**:
   - Comprehensive chemical profiles for `PM2.5`, `PM10`, `NO2`, `SO2`, `CO`, and `O3`.
   - Primary anthropogenic and natural emission sources.
   - Human physiological consequences and cellular mechanisms.
   - Official CPCB concentration breakpoints and regulatory thresholds.
   - Dataset concentration histograms with mean/median benchmarks.

5. **Model Performance & Scientific Benchmarking**:
   - Comparison of **Linear Regression**, **Decision Tree**, and **Random Forest**.
   - Strict 80-20 train-test partition evaluation using MAE, MSE, RMSE, and $R^2$ Score.
   - Grouped error bar chart (MAE vs RMSE).
   - Actual vs Predicted 45° identity scatter plots on unseen test data.
   - Residual error distribution analysis ($y_{test} - y_{pred}$).
   - Feature importance rankings demonstrating particulate matter dominance.
   - Scientific discussion on why tree ensembles outperform global linear models on piecewise max-operator functions.

6. **About Project**:
   - Academic context, CPCB standard definition tables, system architecture, and technology stack.

---

## 🔬 Indian CPCB NAQI Standards Reference

AERIS strictly adheres to the official **Central Pollution Control Board (CPCB)** National Air Quality Index framework:

| AQI Range | Category | Color Code | Environmental & Health Impact |
|---|---|---|---|
| **0 – 50** | **Good** | `#16A34A` | Minimal health impact; clean, fresh air. |
| **51 – 100** | **Satisfactory** | `#84CC16` | Minor breathing discomfort to sensitive individuals. |
| **101 – 200** | **Moderate** | `#EAB308` | Breathing discomfort to people with lung/heart disease and children. |
| **201 – 300** | **Poor** | `#F97316` | Breathing discomfort to most people on prolonged exposure. |
| **301 – 400** | **Very Poor** | `#DC2626` | Respiratory illness on prolonged exposure; significant trigger. |
| **401 – 500** | **Severe** | `#7F1D1D` | Critical emergency; affects healthy people and severely impacts diseased. |

---

## 📊 Machine Learning Model Benchmark

Evaluated on an independent unseen test partition ($N = 1,462$ days):

| Model | MAE | MSE | RMSE | $R^2$ Score | Status |
|---|---|---|---|---|---|
| **Random Forest Regressor** | **0.190** | **0.360** | **0.600** | **1.0000** | 🏆 **Optimal** |
| **Decision Tree Regressor** | 0.488 | 0.960 | 0.980 | 0.9999 | High Precision |
| **Linear Regression** | 18.577 | 714.752 | 26.735 | 0.9449 | Baseline |

### Why Tree Ensembles Excel on CPCB Data
The CPCB AQI is defined as $\text{AQI} = \max(I_{PM2.5}, I_{PM10}, I_{NO2}, I_{SO2}, I_{CO}, I_{O3})$, where each $I_p$ is a piecewise linear interpolation across 6 brackets. Global linear regression cannot model the non-linear $\max()$ operator or piecewise slope shifts, resulting in boundary residual errors. Decision Trees and Random Forests naturally partition feature space into orthogonal hyper-rectangles, matching the CPCB definition with near-zero error.

---

## 📁 Project Structure

```
aeris_aqi_system/
├── app.py                      # Main Streamlit application & navigation router
├── config.py                   # Theme palette, CPCB breakpoints, pollutant metadata
├── train_models.py             # Model training, evaluation, and serialization pipeline
├── requirements.txt            # Python dependencies
├── README.md                   # System documentation & academic summary
├── data/
│   ├── generate_dataset.py     # CPCB telemetry dataset generator
│   └── city_day_cpcb.csv       # Multi-city historical air quality records (7,310 rows)
├── models/
│   ├── random_forest.joblib    # Serialized Random Forest model
│   ├── decision_tree.joblib    # Serialized Decision Tree model
│   ├── linear_regression.joblib# Serialized Linear Regression model
│   ├── model_metrics.json      # Precomputed real test metrics & feature importances
│   └── test_evaluation_data.csv# Unseen test evaluations for diagnostic charts
├── components/
│   ├── header.py               # Top brand header & telemetry badge
│   ├── cards.py                # Metric cards, semicircular gauge, health advisory cards
│   └── charts.py               # Reusable Plotly chart builders with AERIS theme
└── views/
    ├── overview.py             # Executive overview & multi-city analytics
    ├── prediction.py           # Interactive ML prediction simulator & gauge
    ├── analysis.py             # Correlation matrix, scatter plots, seasonal trends
    ├── pollutants.py           # In-depth pollutant profiles & CPCB breakpoints
    ├── model_performance.py    # Metric benchmarks, actual vs predicted, residuals
    └── about.py                # Academic context, NAQI table, system architecture
```

---

## 🚀 Installation & Execution

### 1. Clone / Navigate to Project Directory
```bash
cd "C:\Users\tomar\.gemini\antigravity\scratch\aeris_aqi_system"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Re-train Models
The models and evaluation telemetry are already trained and serialized. If you wish to retrain:
```bash
python train_models.py
```

### 4. Launch the Dashboard
```bash
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 🎨 Visual Identity & Palette

- **Deep Forest Green** (`#12372A`): Primary branding, key headers, focus cards.
- **Emerald Green** (`#1F8A70`): Primary interactive accents, buttons, chart bars.
- **Mint Green** (`#B7E4C7`): Highlighting, badges, subtle atmospheric glows.
- **Soft Sage** (`#D8EAD9`): Secondary card containers and dividers.
- **Main Background** (`#F4F8F4`): Light, breathable nature-inspired dashboard backdrop.
- **Card Background** (`#FFFFFF`): Clean rounded cards with 1px delicate borders and soft shadows.
