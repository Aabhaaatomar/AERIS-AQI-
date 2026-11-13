"""
AERIS - Air Quality Intelligence System
Model Training and Evaluation Pipeline
Trains Linear Regression, Decision Tree, and Random Forest Regressors on Indian CPCB data.
Saves models with joblib and exports real evaluation metrics to JSON and CSV.
"""

import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = r"C:\Users\tomar\.gemini\antigravity\scratch\aeris_aqi_system\data\city_day_cpcb.csv"
MODELS_DIR = r"C:\Users\tomar\.gemini\antigravity\scratch\aeris_aqi_system\models"

FEATURES = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
TARGET = 'AQI'

def train_and_evaluate():
    print("Loading dataset from:", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    
    # Clean data (drop any NaNs if any)
    df_clean = df.dropna(subset=FEATURES + [TARGET])
    
    X = df_clean[FEATURES]
    y = df_clean[TARGET]
    
    print(f"Dataset shape: {X.shape}, Features: {FEATURES}")
    
    # 80-20 Train-Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    
    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(max_depth=10, min_samples_leaf=4, random_state=42),
        'Random Forest': RandomForestRegressor(n_estimators=120, max_depth=15, min_samples_leaf=2, random_state=42, n_jobs=-1)
    }
    
    metrics = {}
    test_eval_df = pd.DataFrame({'Actual_AQI': y_test.values})
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        mae = float(mean_absolute_error(y_test, y_pred))
        mse = float(mean_squared_error(y_test, y_pred))
        rmse = float(np.sqrt(mse))
        r2 = float(r2_score(y_test, y_pred))
        
        metrics[name] = {
            'MAE': round(mae, 3),
            'MSE': round(mse, 3),
            'RMSE': round(rmse, 3),
            'R2': round(r2, 4)
        }
        
        # Save model predictions to evaluation dataframe
        safe_name = name.lower().replace(' ', '_')
        test_eval_df[f'Pred_{safe_name}'] = np.round(y_pred, 2)
        test_eval_df[f'Residual_{safe_name}'] = np.round(y_test.values - y_pred, 2)
        
        # Save individual model
        save_file = f"{MODELS_DIR}/{safe_name}.joblib"
        joblib.dump(model, save_file)
        print(f"Saved {name} to {save_file}")
        print(f"   -> MAE: {mae:.3f}, RMSE: {rmse:.3f}, R2: {r2:.4f}")
    
    # Feature importances
    rf_model = models['Random Forest']
    dt_model = models['Decision Tree']
    lr_model = models['Linear Regression']
    
    feature_analysis = {
        'features': FEATURES,
        'rf_importances': [round(float(v), 4) for v in rf_model.feature_importances_],
        'dt_importances': [round(float(v), 4) for v in dt_model.feature_importances_],
        'lr_coefficients': [round(float(v), 4) for v in lr_model.coef_],
        'lr_intercept': round(float(lr_model.intercept_), 4)
    }
    
    # Determine best model based on R2 and RMSE
    best_model_name = max(metrics.keys(), key=lambda k: metrics[k]['R2'])
    
    summary = {
        'features': FEATURES,
        'target': TARGET,
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'metrics': metrics,
        'best_model': best_model_name,
        'feature_analysis': feature_analysis,
        'feature_ranges': {
            feat: {
                'min': float(df_clean[feat].min()),
                'max': float(df_clean[feat].max()),
                'mean': float(df_clean[feat].mean()),
                'median': float(df_clean[feat].median()),
                'std': float(df_clean[feat].std())
            } for feat in FEATURES
        }
    }
    
    # Save metrics JSON
    metrics_path = f"{MODELS_DIR}/model_metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(summary, f, indent=4)
    print(f"Saved metrics summary to {metrics_path}")
    
    # Save evaluation test sample (first 400 points for crisp interactive visual rendering)
    eval_csv_path = f"{MODELS_DIR}/test_evaluation_data.csv"
    test_eval_df.to_csv(eval_csv_path, index=False)
    print(f"Saved test evaluation data ({len(test_eval_df)} rows) to {eval_csv_path}")

if __name__ == '__main__':
    train_and_evaluate()
