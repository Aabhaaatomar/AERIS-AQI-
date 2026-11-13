"""
AERIS - Chart Components
High-fidelity Plotly charts styled to the AERIS nature-inspired aesthetic.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import COLORS, AQI_CATEGORIES, apply_aeris_theme

# Map category names to their official hex colors
CAT_COLOR_MAP = {
    'Good': COLORS['aqi_good'],
    'Satisfactory': COLORS['aqi_satisfactory'],
    'Moderate': COLORS['aqi_moderate'],
    'Poor': COLORS['aqi_poor'],
    'Very Poor': COLORS['aqi_very_poor'],
    'Severe': COLORS['aqi_severe']
}

def plot_aqi_distribution(df):
    """AQI distribution histogram with Indian CPCB color boundaries."""
    fig = go.Figure()
    
    # Add histogram trace
    fig.add_trace(go.Histogram(
        x=df['AQI'],
        nbinsx=45,
        marker=dict(
            color=COLORS['emerald'],
            line=dict(color=COLORS['forest'], width=1)
        ),
        opacity=0.85,
        name='Observations',
        hovertemplate='AQI Range: %{x}<br>Count: %{y} days<extra></extra>'
    ))
    
    # Add vertical category threshold shading bands
    bands = [
        (0, 50, 'Good', 'rgba(22, 163, 74, 0.08)'),
        (50, 100, 'Satisfactory', 'rgba(132, 204, 22, 0.08)'),
        (100, 200, 'Moderate', 'rgba(234, 179, 8, 0.08)'),
        (200, 300, 'Poor', 'rgba(249, 115, 22, 0.08)'),
        (300, 400, 'Very Poor', 'rgba(220, 38, 38, 0.08)'),
        (400, 500, 'Severe', 'rgba(127, 29, 29, 0.08)')
    ]
    for low, high, label, col in bands:
        fig.add_vrect(
            x0=low, x1=high,
            fillcolor=col,
            layer="below",
            line_width=0,
            annotation_text=label,
            annotation_position="top left",
            annotation_font=dict(size=9, color=COLORS['text_muted'])
        )
        
    fig.update_layout(
        title="<b>AQI Distribution across Indian Monitoring Stations</b>",
        xaxis_title="Air Quality Index (AQI)",
        yaxis_title="Observation Frequency (Days)",
        bargap=0.05
    )
    return apply_aeris_theme(fig)

def plot_aqi_category_donut(df):
    """Donut chart showing distribution of Indian AQI categories."""
    cat_order = ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe']
    counts = df['AQI_Bucket'].value_counts()
    
    # Ensure ordered representation
    ordered_labels = [c for c in cat_order if c in counts.index]
    ordered_values = [counts[c] for c in ordered_labels]
    colors = [CAT_COLOR_MAP[c] for c in ordered_labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=ordered_labels,
        values=ordered_values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(family='Inter, sans-serif', size=11, color=COLORS['text_primary']),
        hovertemplate='<b>%{label}</b><br>Observations: %{value:,} days (%{percent})<extra></extra>'
    )])
    
    fig.update_layout(
        title="<b>Air Quality Classification Share</b>",
        annotations=[dict(
            text="<b>CPCB</b><br>Breakdown",
            x=0.5, y=0.5,
            font_size=13,
            font_family="Poppins, sans-serif",
            font_color=COLORS['forest'],
            showarrow=False
        )],
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return apply_aeris_theme(fig)

def plot_city_aqi_ranking(df):
    """Horizontal bar chart comparing average AQI across cities."""
    city_avg = df.groupby('City')['AQI'].mean().reset_index()
    city_avg = city_avg.sort_values(by='AQI', ascending=True)
    
    # Assign color based on AQI value
    def get_color(val):
        if val <= 50: return COLORS['aqi_good']
        if val <= 100: return COLORS['aqi_satisfactory']
        if val <= 200: return COLORS['aqi_moderate']
        if val <= 300: return COLORS['aqi_poor']
        if val <= 400: return COLORS['aqi_very_poor']
        return COLORS['aqi_severe']
        
    colors = [get_color(v) for v in city_avg['AQI']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=city_avg['City'],
        x=city_avg['AQI'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color=COLORS['forest'], width=1)
        ),
        text=[f"{v:.1f}" for v in city_avg['AQI']],
        textposition='outside',
        textfont=dict(family='Space Grotesk, sans-serif', size=11, color=COLORS['forest']),
        hovertemplate='<b>%{y}</b><br>Mean AQI: %{x:.1f}<extra></extra>'
    ))
    
    # Add National Mean Reference Line
    nat_mean = df['AQI'].mean()
    fig.add_vline(
        x=nat_mean,
        line_dash="dash",
        line_color=COLORS['forest'],
        line_width=1.5,
        annotation_text=f"Network Avg: {nat_mean:.1f}",
        annotation_position="bottom right",
        annotation_font=dict(size=10, color=COLORS['forest'])
    )
    
    fig.update_layout(
        title="<b>City-wise Mean AQI Ranking</b>",
        xaxis_title="Mean AQI Value",
        yaxis_title="Monitored City",
        xaxis=dict(range=[0, max(city_avg['AQI']) * 1.15])
    )
    return apply_aeris_theme(fig)

def plot_pollutant_concentration_comparison(df):
    """Comparison of mean concentrations and standard deviations across key pollutants."""
    pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'O3']
    means = [df[p].mean() for p in pollutants]
    stds = [df[p].std() for p in pollutants]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=pollutants,
        y=means,
        error_y=dict(type='data', array=stds, visible=True, color=COLORS['text_muted']),
        marker=dict(
            color=[COLORS['emerald'], '#2D9A7A', '#41AA8A', '#5CB99B', '#7EC8AF'],
            line=dict(color=COLORS['forest'], width=1)
        ),
        hovertemplate='<b>%{x}</b><br>Mean: %{y:.1f} µg/m³<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Mean Pollutant Concentrations (µg/m³)</b>",
        xaxis_title="Atmospheric Pollutant",
        yaxis_title="Concentration (µg/m³)"
    )
    return apply_aeris_theme(fig)

def plot_aqi_trend(df, city=None):
    """Temporal AQI trendline with rolling average."""
    sub_df = df[df['City'] == city].copy() if (city and city != "All Cities (National Aggregate)") else df.groupby('Date')['AQI'].mean().reset_index()
    sub_df['Date'] = pd.to_datetime(sub_df['Date'])
    sub_df = sub_df.sort_values('Date')
    sub_df['Rolling_7d'] = sub_df['AQI'].rolling(window=7, min_periods=1).mean()
    
    fig = go.Figure()
    
    # Daily points / faint line
    fig.add_trace(go.Scatter(
        x=sub_df['Date'],
        y=sub_df['AQI'],
        mode='lines',
        name='Daily AQI',
        line=dict(color='#A3C4B8', width=1),
        opacity=0.6,
        hovertemplate='%{x|%b %d, %Y}<br>Daily AQI: %{y:.1f}<extra></extra>'
    ))
    
    # 7-day smoothed trend
    fig.add_trace(go.Scatter(
        x=sub_df['Date'],
        y=sub_df['Rolling_7d'],
        mode='lines',
        name='7-Day Rolling Trend',
        line=dict(color=COLORS['forest'], width=2.5),
        hovertemplate='%{x|%b %d, %Y}<br>7-Day Trend: %{y:.1f}<extra></extra>'
    ))
    
    # Add Moderate and Poor benchmark reference lines
    fig.add_hline(y=100, line_dash="dot", line_color=COLORS['aqi_satisfactory'], annotation_text="Satisfactory Limit (100)", annotation_position="top left", annotation_font_size=9)
    fig.add_hline(y=200, line_dash="dot", line_color=COLORS['aqi_poor'], annotation_text="Unhealthy/Poor (200)", annotation_position="top left", annotation_font_size=9)
    
    target_name = city if (city and city != "All Cities (National Aggregate)") else "All Monitored Cities"
    fig.update_layout(
        title=f"<b>Temporal AQI Trajectory: {target_name}</b>",
        xaxis_title="Observation Timeline",
        yaxis_title="AQI Level",
        yaxis=dict(range=[0, max(500, sub_df['AQI'].max() + 20)])
    )
    return apply_aeris_theme(fig)

def plot_correlation_heatmap(df):
    """Green-divergent correlation matrix of all pollutants and AQI."""
    cols = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'AQI']
    corr = df[cols].corr().round(2)
    
    custom_colorscale = [
        [0.0, '#EAF2EA'],
        [0.35, '#B7E4C7'],
        [0.70, '#1F8A70'],
        [1.0, '#12372A']
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=cols,
        y=cols,
        colorscale=custom_colorscale,
        text=corr.values,
        texttemplate="%{text}",
        textfont=dict(family="Space Grotesk, sans-serif", size=12, color="#FFFFFF"),
        colorbar=dict(title="r", tickfont=dict(color=COLORS['text_secondary'])),
        hovertemplate='Feature 1: %{y}<br>Feature 2: %{x}<br>Correlation r: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Atmospheric Pollutant Correlation Matrix</b>",
        xaxis=dict(side="bottom"),
        margin=dict(l=60, r=40, t=50, b=50)
    )
    return apply_aeris_theme(fig)

def plot_scatter_relationship(df, x_col, y_col='AQI'):
    """Scatter plot showing pollutant vs AQI with trendline and category shading."""
    # Subsample 700 points for crisp interactive performance
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
    
    # Compute OLS line directly with numpy polyfit
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
            line=dict(color=COLORS['forest'], width=2.5, dash='dash')
        ))
    
    fig.update_traces(marker=dict(size=6, line=dict(width=0.5, color='#FFFFFF')), selector=dict(mode='markers'))
    fig.update_layout(
        title=f"<b>Empirical Relationship: {x_col} vs {y_col}</b>",
        xaxis_title=f"{x_col} Concentration",
        yaxis_title="Calculated AQI"
    )
    return apply_aeris_theme(fig)

def plot_model_comparison_bar(metrics_dict):
    """Bar chart comparing MAE, RMSE, and R2 across ML models."""
    models = list(metrics_dict.keys())
    maes = [metrics_dict[m]['MAE'] for m in models]
    rmses = [metrics_dict[m]['RMSE'] for m in models]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='MAE (Mean Absolute Error)',
        x=models,
        y=maes,
        marker=dict(color=COLORS['emerald'], line=dict(color=COLORS['forest'], width=1)),
        text=[f"{v:.2f}" for v in maes],
        textposition='outside',
        textfont=dict(size=11)
    ))
    
    fig.add_trace(go.Bar(
        name='RMSE (Root Mean Squared Error)',
        x=models,
        y=rmses,
        marker=dict(color='#3A6B56', line=dict(color=COLORS['forest'], width=1)),
        text=[f"{v:.2f}" for v in rmses],
        textposition='outside',
        textfont=dict(size=11)
    ))
    
    fig.update_layout(
        title="<b>Error Metric Comparison Across Algorithms (Lower is Better)</b>",
        yaxis_title="Error Margin (AQI Points)",
        barmode='group',
        xaxis_title="Machine Learning Model"
    )
    return apply_aeris_theme(fig)

def plot_actual_vs_predicted(eval_df, model_key):
    """Actual vs Predicted AQI scatter plot with 45° perfect prediction reference line."""
    pred_col = f"Pred_{model_key}"
    sample_eval = eval_df.sample(min(500, len(eval_df)), random_state=42)
    
    fig = go.Figure()
    
    # 45-degree reference line
    min_val = 0
    max_val = 500
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        name='Ideal 1:1 Identity',
        line=dict(color='#DC2626', width=2, dash='dash')
    ))
    
    # Predictions
    fig.add_trace(go.Scatter(
        x=sample_eval['Actual_AQI'],
        y=sample_eval[pred_col],
        mode='markers',
        name='Model Predictions',
        marker=dict(
            color=COLORS['emerald'],
            size=6,
            opacity=0.65,
            line=dict(color=COLORS['forest'], width=0.5)
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
    return apply_aeris_theme(fig)

def plot_residual_distribution(eval_df, model_key):
    """Histogram of prediction residuals (Actual - Predicted)."""
    res_col = f"Residual_{model_key}"
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=eval_df[res_col],
        nbinsx=40,
        marker=dict(
            color=COLORS['forest'],
            line=dict(color=COLORS['mint'], width=1)
        ),
        opacity=0.85,
        hovertemplate='Residual Error: %{x:.2f}<br>Frequency: %{y}<extra></extra>'
    ))
    
    # Zero residual indicator line
    fig.add_vline(x=0, line_dash="solid", line_color="#DC2626", line_width=2, annotation_text="Zero Error Baseline", annotation_position="top left", annotation_font_size=10)
    
    fig.update_layout(
        title="<b>Residual Error Distribution (Actual - Predicted)</b>",
        xaxis_title="Residual Error (AQI Points)",
        yaxis_title="Count of Test Instances",
        bargap=0.05
    )
    return apply_aeris_theme(fig)

def plot_feature_importance(features, importances):
    """Horizontal bar chart for Random Forest feature importances."""
    fi_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    fi_df = fi_df.sort_values(by='Importance', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=fi_df['Feature'],
        x=fi_df['Importance'],
        orientation='h',
        marker=dict(
            color=COLORS['emerald'],
            line=dict(color=COLORS['forest'], width=1)
        ),
        text=[f"{v*100:.1f}%" for v in fi_df['Importance']],
        textposition='outside',
        textfont=dict(family='Space Grotesk, sans-serif', size=11, color=COLORS['forest']),
        hovertemplate='<b>%{y}</b><br>Relative Influence: %{x:.3f} (%{text})<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Random Forest Feature Importance Weighting</b>",
        xaxis_title="Relative Feature Importance Score",
        yaxis_title="Atmospheric Parameter",
        xaxis=dict(range=[0, max(fi_df['Importance']) * 1.2])
    )
    return apply_aeris_theme(fig)
