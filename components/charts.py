"""
AERIS 2.0 - Chart Components
High-fidelity Plotly charts dynamically styled to Light, Dark, and Cream themes.
Ensures 100% readability with zero unreadable text or transparent clashes.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import CPCB_COLORS, apply_aeris_theme
from utils.theme_manager import get_theme_colors

CAT_COLOR_MAP = CPCB_COLORS

def plot_aqi_distribution(df):
    """AQI distribution histogram with Indian CPCB color boundaries."""
    t = get_theme_colors()
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df['AQI'],
        nbinsx=45,
        marker=dict(
            color=t['secondary'],
            line=dict(color=t['primary'], width=1)
        ),
        opacity=0.85,
        name='Observations',
        hovertemplate='AQI Range: %{x}<br>Count: %{y} days<extra></extra>'
    ))
    
    bands = [
        (0, 50, 'Good', 'rgba(22, 163, 74, 0.12)'),
        (50, 100, 'Satisfactory', 'rgba(132, 204, 22, 0.12)'),
        (100, 200, 'Moderate', 'rgba(234, 179, 8, 0.12)'),
        (200, 300, 'Poor', 'rgba(249, 115, 22, 0.12)'),
        (300, 400, 'Very Poor', 'rgba(220, 38, 38, 0.12)'),
        (400, 500, 'Severe', 'rgba(127, 29, 29, 0.12)')
    ]
    for low, high, label, col in bands:
        fig.add_vrect(
            x0=low, x1=high,
            fillcolor=col,
            layer="below",
            line_width=0,
            annotation_text=label,
            annotation_position="top left",
            annotation_font=dict(size=9, color=t['text_muted'])
        )
        
    fig.update_layout(
        title="<b>AQI Distribution across Indian Monitoring Stations</b>",
        xaxis_title="Air Quality Index (AQI)",
        yaxis_title="Observation Frequency (Days)",
        bargap=0.05
    )
    return apply_aeris_theme(fig, t)

def plot_aqi_category_donut(df):
    """Donut chart showing distribution of Indian AQI categories."""
    t = get_theme_colors()
    cat_order = ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe']
    counts = df['AQI_Bucket'].value_counts()
    
    ordered_labels = [c for c in cat_order if c in counts.index]
    ordered_values = [counts[c] for c in ordered_labels]
    colors = [CAT_COLOR_MAP[c] for c in ordered_labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=ordered_labels,
        values=ordered_values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color=t['bg_card'], width=2)),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(family='Inter, sans-serif', size=11, color=t['text_primary']),
        hovertemplate='<b>%{label}</b><br>Observations: %{value:,} days (%{percent})<extra></extra>'
    )])
    
    fig.update_layout(
        title="<b>Air Quality Classification Share</b>",
        annotations=[dict(
            text="<b>CPCB</b><br>Share",
            x=0.5, y=0.5,
            font_size=13,
            font_family="Manrope, sans-serif",
            font_color=t['primary'],
            showarrow=False
        )],
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return apply_aeris_theme(fig, t)

def plot_city_aqi_ranking(df):
    """Horizontal bar chart comparing average AQI across cities."""
    t = get_theme_colors()
    city_avg = df.groupby('City')['AQI'].mean().reset_index()
    city_avg = city_avg.sort_values(by='AQI', ascending=True)
    
    def get_color(val):
        if val <= 50: return CAT_COLOR_MAP['Good']
        if val <= 100: return CAT_COLOR_MAP['Satisfactory']
        if val <= 200: return CAT_COLOR_MAP['Moderate']
        if val <= 300: return CAT_COLOR_MAP['Poor']
        if val <= 400: return CAT_COLOR_MAP['Very Poor']
        return CAT_COLOR_MAP['Severe']
        
    colors = [get_color(v) for v in city_avg['AQI']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=city_avg['City'],
        x=city_avg['AQI'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color=t['primary'], width=1)
        ),
        text=[f"{v:.1f}" for v in city_avg['AQI']],
        textposition='outside',
        textfont=dict(family='Space Grotesk, sans-serif', size=11, color=t['text_primary']),
        hovertemplate='<b>%{y}</b><br>Mean AQI: %{x:.1f}<extra></extra>'
    ))
    
    nat_mean = df['AQI'].mean()
    fig.add_vline(
        x=nat_mean,
        line_dash="dash",
        line_color=t['primary'],
        line_width=1.5,
        annotation_text=f"Network Avg: {nat_mean:.1f}",
        annotation_position="bottom right",
        annotation_font=dict(size=10, color=t['primary'])
    )
    
    fig.update_layout(
        title="<b>City-wise Mean AQI Ranking</b>",
        xaxis_title="Mean AQI Value",
        yaxis_title="Monitored City",
        xaxis=dict(range=[0, max(city_avg['AQI']) * 1.15])
    )
    return apply_aeris_theme(fig, t)

def plot_pollutant_concentration_comparison(df):
    """Comparison of mean concentrations and standard deviations across key pollutants."""
    t = get_theme_colors()
    pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'O3']
    means = [df[p].mean() for p in pollutants]
    stds = [df[p].std() for p in pollutants]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=pollutants,
        y=means,
        error_y=dict(type='data', array=stds, visible=True, color=t['text_muted']),
        marker=dict(
            color=[t['secondary'], t['primary'], t['accent'], '#22c55e', '#3b82f6'],
            line=dict(color=t['border'], width=1)
        ),
        hovertemplate='<b>%{x}</b><br>Mean: %{y:.1f} µg/m³<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Mean Pollutant Concentrations (µg/m³)</b>",
        xaxis_title="Atmospheric Pollutant",
        yaxis_title="Concentration (µg/m³)"
    )
    return apply_aeris_theme(fig, t)

def plot_aqi_trend(df, city=None):
    """Temporal AQI trendline with rolling average."""
    t = get_theme_colors()
    sub_df = df[df['City'] == city].copy() if (city and city != "All Cities (National Aggregate)") else df.groupby('Date')['AQI'].mean().reset_index()
    sub_df['Date'] = pd.to_datetime(sub_df['Date'])
    sub_df = sub_df.sort_values('Date')
    sub_df['Rolling_7d'] = sub_df['AQI'].rolling(window=7, min_periods=1).mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sub_df['Date'],
        y=sub_df['AQI'],
        mode='lines',
        name='Daily AQI',
        line=dict(color=t['text_muted'], width=1),
        opacity=0.45,
        hovertemplate='%{x|%b %d, %Y}<br>Daily AQI: %{y:.1f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=sub_df['Date'],
        y=sub_df['Rolling_7d'],
        mode='lines',
        name='7-Day Rolling Trend',
        line=dict(color=t['primary'], width=2.5),
        hovertemplate='%{x|%b %d, %Y}<br>7-Day Trend: %{y:.1f}<extra></extra>'
    ))
    
    fig.add_hline(y=100, line_dash="dot", line_color=CAT_COLOR_MAP['Satisfactory'], annotation_text="Satisfactory Limit (100)", annotation_position="top left", annotation_font_size=9)
    fig.add_hline(y=200, line_dash="dot", line_color=CAT_COLOR_MAP['Poor'], annotation_text="Unhealthy/Poor (200)", annotation_position="top left", annotation_font_size=9)
    
    target_name = city if (city and city != "All Cities (National Aggregate)") else "All Monitored Cities"
    fig.update_layout(
        title=f"<b>Temporal AQI Trajectory: {target_name}</b>",
        xaxis_title="Observation Timeline",
        yaxis_title="AQI Level",
        yaxis=dict(range=[0, max(500, sub_df['AQI'].max() + 20)])
    )
    return apply_aeris_theme(fig, t)

def plot_correlation_heatmap(df):
    """Correlation matrix of all pollutants and AQI with high-contrast text."""
    t = get_theme_colors()
    cols = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'AQI']
    corr = df[cols].corr().round(2)
    
    custom_colorscale = [
        [0.0, t['bg_secondary']],
        [0.35, t['mint']],
        [0.70, t['secondary']],
        [1.0, t['primary']]
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=cols,
        y=cols,
        colorscale=custom_colorscale,
        text=corr.values,
        texttemplate="%{text}",
        textfont=dict(family="Space Grotesk, sans-serif", size=12, color=t['text_primary']),
        colorbar=dict(title="r", tickfont=dict(color=t['text_secondary'])),
        hovertemplate='Feature 1: %{y}<br>Feature 2: %{x}<br>Correlation r: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Atmospheric Pollutant Correlation Matrix</b>",
        xaxis=dict(side="bottom"),
        margin=dict(l=60, r=40, t=50, b=50)
    )
    return apply_aeris_theme(fig, t)

def plot_scatter_relationship(df, x_col, y_col='AQI'):
    """Scatter plot showing pollutant vs AQI with trendline and category shading."""
    t = get_theme_colors()
    sample_df = df.sample(min(700, len(df)), random_state=42).copy()
    
    fig = px.scatter(
        sample_df,
        x=x_col,
        y=y_col,
        color='AQI_Bucket',
        color_discrete_map=CAT_COLOR_MAP,
        opacity=0.75,
        labels={'AQI_Bucket': 'CPCB Category'},
        hover_data=['City', 'Date']
    )
    
    x_vals = sample_df[x_col].values
    y_vals = sample_df[y_col].values
    valid_mask = ~np.isnan(x_vals) & ~np.isnan(y_vals)
    if np.sum(valid_mask) > 1:
        slope, intercept = np.polyfit(x_vals[valid_mask], y_vals[valid_mask], 1)
        x_line = np.linspace(float(np.min(x_vals[valid_mask])), float(np.max(x_vals[valid_mask])), 50)
        y_line = slope * x_line + intercept
        fig.add_trace(go.Scatter(
            x=x_line,
            y=y_line,
            mode='lines',
            name=f'OLS Trend (m={slope:.2f})',
            line=dict(color=t['primary'], width=2.5, dash='dash')
        ))
    
    fig.update_traces(marker=dict(size=6, line=dict(width=0.5, color=t['bg_card'])), selector=dict(mode='markers'))
    fig.update_layout(
        title=f"<b>Empirical Relationship: {x_col} vs {y_col}</b>",
        xaxis_title=f"{x_col} Concentration",
        yaxis_title="Calculated AQI"
    )
    return apply_aeris_theme(fig, t)

def plot_model_comparison_bar(metrics_dict):
    """Bar chart comparing MAE and RMSE across ML models."""
    t = get_theme_colors()
    models = list(metrics_dict.keys())
    maes = [metrics_dict[m]['MAE'] for m in models]
    rmses = [metrics_dict[m]['RMSE'] for m in models]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='MAE (Mean Absolute Error)',
        x=models,
        y=maes,
        marker=dict(color=t['secondary'], line=dict(color=t['primary'], width=1)),
        text=[f"{v:.2f}" for v in maes],
        textposition='outside',
        textfont=dict(size=11, color=t['text_primary'])
    ))
    
    fig.add_trace(go.Bar(
        name='RMSE (Root Mean Squared Error)',
        x=models,
        y=rmses,
        marker=dict(color=t['accent'], line=dict(color=t['primary'], width=1)),
        text=[f"{v:.2f}" for v in rmses],
        textposition='outside',
        textfont=dict(size=11, color=t['text_primary'])
    ))
    
    fig.update_layout(
        title="<b>Error Metric Comparison Across Algorithms (Lower is Better)</b>",
        yaxis_title="Error Margin (AQI Points)",
        barmode='group',
        xaxis_title="Machine Learning Model"
    )
    return apply_aeris_theme(fig, t)

def plot_actual_vs_predicted(eval_df, model_key):
    """Actual vs Predicted AQI scatter plot with 45° perfect prediction reference line."""
    t = get_theme_colors()
    pred_col = f"Pred_{model_key}"
    sample_eval = eval_df.sample(min(500, len(eval_df)), random_state=42)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[0, 500],
        y=[0, 500],
        mode='lines',
        name='Ideal 1:1 Identity',
        line=dict(color='#DC2626', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=sample_eval['Actual_AQI'],
        y=sample_eval[pred_col],
        mode='markers',
        name='Model Predictions',
        marker=dict(
            color=t['secondary'],
            size=6,
            opacity=0.65,
            line=dict(color=t['primary'], width=0.5)
        ),
        hovertemplate='Actual AQI: %{x:.1f}<br>Predicted AQI: %{y:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Actual vs. Predicted AQI on Unseen Test Partition</b>",
        xaxis_title="Actual Ground Truth AQI",
        yaxis_title="Model Predicted AQI",
        xaxis=dict(range=[0, 520]),
        yaxis=dict(range=[0, 520])
    )
    return apply_aeris_theme(fig, t)

def plot_residual_distribution(eval_df, model_key):
    """Histogram of prediction residuals (Actual - Predicted)."""
    t = get_theme_colors()
    res_col = f"Residual_{model_key}"
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=eval_df[res_col],
        nbinsx=40,
        marker=dict(
            color=t['primary'],
            line=dict(color=t['mint'], width=1)
        ),
        opacity=0.85,
        hovertemplate='Residual Error: %{x:.2f}<br>Frequency: %{y}<extra></extra>'
    ))
    
    fig.add_vline(x=0, line_dash="solid", line_color="#DC2626", line_width=2, annotation_text="Zero Error Baseline", annotation_position="top left", annotation_font_size=10)
    
    fig.update_layout(
        title="<b>Residual Error Distribution (Actual - Predicted)</b>",
        xaxis_title="Residual Error (AQI Points)",
        yaxis_title="Count of Test Instances",
        bargap=0.05
    )
    return apply_aeris_theme(fig, t)

def plot_feature_importance(features, importances):
    """Horizontal bar chart for Random Forest feature importances."""
    t = get_theme_colors()
    fi_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    fi_df = fi_df.sort_values(by='Importance', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=fi_df['Feature'],
        x=fi_df['Importance'],
        orientation='h',
        marker=dict(
            color=t['secondary'],
            line=dict(color=t['primary'], width=1)
        ),
        text=[f"{v*100:.1f}%" for v in fi_df['Importance']],
        textposition='outside',
        textfont=dict(family='Space Grotesk, sans-serif', size=11, color=t['text_primary']),
        hovertemplate='<b>%{y}</b><br>Relative Influence: %{x:.3f} (%{text})<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Random Forest Feature Importance Weighting</b>",
        xaxis_title="Relative Feature Importance Score",
        yaxis_title="Atmospheric Parameter",
        xaxis=dict(range=[0, max(fi_df['Importance']) * 1.25])
    )
    return apply_aeris_theme(fig, t)

def plot_live_hourly_trend(hourly_df, city_name="Delhi"):
    """Line chart showing real-time 24-hour PM2.5 and PM10 trend from live telemetry."""
    t = get_theme_colors()
    if hourly_df.empty:
        return None
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hourly_df['Time'],
        y=hourly_df['PM2.5'],
        mode='lines+markers',
        name='PM2.5 (Fine)',
        line=dict(color=t['primary'], width=2.5),
        marker=dict(size=4)
    ))
    
    if 'PM10' in hourly_df.columns:
        fig.add_trace(go.Scatter(
            x=hourly_df['Time'],
            y=hourly_df['PM10'],
            mode='lines+markers',
            name='PM10 (Coarse)',
            line=dict(color=t['secondary'], width=2, dash='dot'),
            marker=dict(size=4)
        ))
        
    fig.add_hline(y=60, line_dash="dash", line_color="#EAB308", annotation_text="CPCB PM2.5 Safe Limit (60)", annotation_position="top left", annotation_font_size=9)
    
    fig.update_layout(
        title=f"<b>24-Hour Telemetry Trajectory: {city_name}</b>",
        xaxis_title="Time of Day",
        yaxis_title="Particulate Concentration (µg/m³)"
    )
    return apply_aeris_theme(fig, t)
