# Weather Data Dashboard

## Overview

This Weather Data Dashboard is an interactive web application that visualizes and analyzes synthetic weather data for a full year. Built with Streamlit and Python, it offers comprehensive insights into weather patterns, seasonal trends, and climate data correlations.

## Features

- **Interactive Data Filtering**
  - Filter by date range
  - Filter by season (Winter, Spring, Summer, Fall)
  
- **Key Weather Metrics**
  - Temperature, humidity, and rainfall trends
  - Automatic comparison to overall averages
  - Rainy days counter
  
- **Extreme Weather Analysis**
  - Highlights of extreme temperature, humidity, and rainfall events
  - Date tracking for significant weather occurrences
  
- **Visualization Tabs**
  - **Time Series**: Track weather patterns over time
  - **Monthly Trends**: Analyze monthly averages with bar charts
  - **Seasonal Analysis**: Compare seasons with radar charts
  - **Correlations**: Explore relationships between weather metrics
  - **Comfort Index**: Visualize weather comfort levels throughout the year
  
- **Data Explorer**
  - View and filter raw data
  - Download filtered data as CSV
  - Summary statistics with expandable details

## Project Structure

```
weather_dashboard_project/
├── app.py             # Main Streamlit application file
├── data_generator.py  # Generate synthetic weather data
├── data_processor.py  # Process and analyze data
└── README.md          # Project documentation
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bit-saurabh/weather-dashboard.git
   cd weather-dashboard
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   
    install individually:
   ```bash
   pip install streamlit pandas numpy matplotlib seaborn plotly
   ```

## Usage

1. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL shown in your terminal (typically http://localhost:8501)

3. Use the sidebar controls to filter data and explore different visualizations through the tabs

## Data Generation

The dashboard uses synthetic weather data generated to simulate realistic weather patterns:

- **Temperature**: Follows seasonal patterns with random variations
- **Humidity**: Varies with temperature and seasons
- **Rainfall**: More frequent in spring and fall with realistic distribution

This allows for testing and demonstration without requiring external data sources.

## Customization

### Using Your Own Data

To use your own weather data instead of the synthetic data:

1. Prepare a CSV file with columns for date, temperature, humidity, and rainfall
2. Modify the `app.py` file to load your data instead of generating it:

```python
# Replace the data generation code with:
@st.cache_data
def load_data():
    df = pd.read_csv("your_weather_data.csv")
    df['date'] = pd.to_datetime(df['date'])
    
    # Add any necessary columns like month_name and season
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name()
    
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
    
    df['season'] = df['month'].apply(get_season)
    
    return df

# Use this instead of generate_weather_data()
weather_data = load_data()
```

### Adding New Visualizations

To add a new visualization tab:

1. Add a new tab name to the tabs list:
```python
tabs = st.tabs(["Time Series", "Monthly Trends", "Seasonal Analysis", "Correlations", "Comfort Index", "Your New Tab"])
```

2. Add your visualization code in a new `with tabs[5]:` block after the existing tabs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Data visualization powered by [Plotly](https://plotly.com/) and [Matplotlib](https://matplotlib.org/)
- Data processing with [Pandas](https://pandas.pydata.org/)