import pandas as pd
import numpy as np

def get_monthly_averages(df):
    """Calculate monthly averages for weather metrics."""
    monthly_avg = df.groupby('month_name')[['temperature', 'humidity', 'rainfall']].mean()
    # Reorder months chronologically
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_avg = monthly_avg.reindex(month_order)
    return monthly_avg

def get_seasonal_averages(df):
    """Calculate seasonal averages for weather metrics."""
    seasonal_avg = df.groupby('season')[['temperature', 'humidity', 'rainfall']].mean()
    # Reorder seasons chronologically
    season_order = ['Winter', 'Spring', 'Summer', 'Fall']
    seasonal_avg = seasonal_avg.reindex(season_order)
    return seasonal_avg

def get_summary_stats(df):
    """Calculate summary statistics for the dataset."""
    return df[['temperature', 'humidity', 'rainfall']].describe()

def get_extreme_days(df):
    """Find days with extreme weather conditions."""
    hottest_day = df.loc[df['temperature'].idxmax()]
    coldest_day = df.loc[df['temperature'].idxmin()]
    wettest_day = df.loc[df['rainfall'].idxmax()]
    most_humid_day = df.loc[df['humidity'].idxmax()]
    
    return {
        'hottest': hottest_day,
        'coldest': coldest_day,
        'wettest': wettest_day,
        'most_humid': most_humid_day
    }

def get_correlation_data(df):
    """Calculate correlations between weather metrics."""
    return df[['temperature', 'humidity', 'rainfall']].corr()

def get_rainy_days_count(df):
    """Count days with rainfall above threshold."""
    return (df['rainfall'] > 0.1).sum()

def get_comfort_index(df):
    """Calculate a simple comfort index based on temperature and humidity."""
    # Simple comfort index (lower is more comfortable)
    # Penalizes extreme temperatures and high humidity
    temp_comfort = np.abs(df['temperature'] - 23)  # Ideal temperature around 23°C
    humidity_discomfort = np.maximum(0, df['humidity'] - 60) / 10  # Penalty for humidity above 60%
    
    comfort_index = temp_comfort + humidity_discomfort
    
    df_comfort = df.copy()
    df_comfort['comfort_index'] = comfort_index
    
    return df_comfort
