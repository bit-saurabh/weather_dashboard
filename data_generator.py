import pandas as pd
import numpy as np
from datetime import datetime

def generate_weather_data():
    """Generate synthetic weather data for a year."""
    # Create date range for a year
    date_range = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    # Base temperature patterns with seasonal variations
    base_temp = 20 + 15 * np.sin((np.arange(len(date_range)) / 365) * 2 * np.pi)
    
    # Add some random variations
    temperatures = base_temp + np.random.normal(0, 3, len(date_range))
    
    # Humidity levels (higher in summer, lower in winter, with variation)
    humidity = 60 + 20 * np.sin((np.arange(len(date_range)) / 365) * 2 * np.pi) + np.random.normal(0, 10, len(date_range))
    humidity = np.clip(humidity, 20, 100)  # Clip to realistic range
    
    # Rainfall - more frequent in certain seasons
    rainfall = np.zeros(len(date_range))
    # Rainy season in spring and fall
    spring_fall_mask = ((date_range.month >= 3) & (date_range.month <= 5)) | ((date_range.month >= 9) & (date_range.month <= 11))
    
    # Base probability of rain
    rain_prob = np.random.rand(len(date_range))
    rainfall[spring_fall_mask & (rain_prob > 0.6)] = np.random.exponential(5, size=np.sum(spring_fall_mask & (rain_prob > 0.6)))
    rainfall[~spring_fall_mask & (rain_prob > 0.8)] = np.random.exponential(2, size=np.sum(~spring_fall_mask & (rain_prob > 0.8)))
    
    # Create DataFrame
    weather_df = pd.DataFrame({
        'date': date_range,
        'temperature': temperatures,
        'humidity': humidity,
        'rainfall': rainfall
    })
    
    # Add month and season columns for analysis
    weather_df['month'] = weather_df['date'].dt.month
    weather_df['month_name'] = weather_df['date'].dt.month_name()
    
    # Define seasons
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
    
    weather_df['season'] = weather_df['month'].apply(get_season)
    
    return weather_df
