import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_generator import generate_weather_data
from data_processor import (
    get_monthly_averages, 
    get_seasonal_averages,
    get_summary_stats,
    get_extreme_days,
    get_correlation_data,
    get_rainy_days_count,
    get_comfort_index
)

# Page config
st.set_page_config(
    page_title="Weather Data Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom CSS
st.markdown("""
<style>
    .dashboard-title {
        font-size: 42px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-container {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .chart-container {
        background-color: white;
        border-radius: 5px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        color: #7f8c8d;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="dashboard-title">🌤️ Weather Data Dashboard</div>', unsafe_allow_html=True)
st.markdown("Interactive analysis of synthetic weather data for a full year.")

# Initialize session state for data persistence
if 'weather_data' not in st.session_state:
    with st.spinner("Generating weather data..."):
        st.session_state.weather_data = generate_weather_data()
        st.session_state.monthly_avg = get_monthly_averages(st.session_state.weather_data)
        st.session_state.seasonal_avg = get_seasonal_averages(st.session_state.weather_data)
        st.session_state.extreme_days = get_extreme_days(st.session_state.weather_data)
        st.session_state.weather_data_comfort = get_comfort_index(st.session_state.weather_data)

# Get data from session state
weather_data = st.session_state.weather_data
monthly_avg = st.session_state.monthly_avg
seasonal_avg = st.session_state.seasonal_avg
extreme_days = st.session_state.extreme_days
weather_data_comfort = st.session_state.weather_data_comfort

# Sidebar
st.sidebar.header("Dashboard Controls")

# Date range selector
st.sidebar.subheader("Date Range")
date_range = st.sidebar.date_input(
    "Select date range",
    [pd.to_datetime("2024-01-01"), pd.to_datetime("2024-12-31")],
    min_value=pd.to_datetime("2024-01-01"),
    max_value=pd.to_datetime("2024-12-31")
)

# Season filter
st.sidebar.subheader("Filter by Season")
season_filter = st.sidebar.selectbox(
    "Select Season",
    ["All Seasons", "Winter", "Spring", "Summer", "Fall"]
)

# Apply filters
filtered_data = weather_data.copy()
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_data = filtered_data[(filtered_data['date'] >= pd.to_datetime(start_date)) & 
                                 (filtered_data['date'] <= pd.to_datetime(end_date))]

if season_filter != "All Seasons":
    filtered_data = filtered_data[filtered_data['season'] == season_filter]

# Metrics for filtered data
filtered_extreme_days = get_extreme_days(filtered_data)
rainy_days = get_rainy_days_count(filtered_data)
avg_temp = filtered_data['temperature'].mean()
avg_humidity = filtered_data['humidity'].mean()
avg_rainfall = filtered_data['rainfall'].mean()

# Display metrics in columns
st.markdown('<div class="section-header">Key Weather Metrics</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric(
        label="Average Temperature",
        value=f"{avg_temp:.1f} °C",
        delta=f"{avg_temp - weather_data['temperature'].mean():.1f} °C",
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric(
        label="Average Humidity",
        value=f"{avg_humidity:.1f}%",
        delta=f"{avg_humidity - weather_data['humidity'].mean():.1f}%",
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric(
        label="Average Rainfall",
        value=f"{avg_rainfall:.2f} mm",
        delta=f"{avg_rainfall - weather_data['rainfall'].mean():.2f} mm",
        delta_color="inverse"  # Higher rainfall shown as negative
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric(
        label="Rainy Days",
        value=f"{rainy_days}",
        delta=f"{rainy_days - get_rainy_days_count(weather_data)}",
        delta_color="inverse"  # More rainy days shown as negative
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Extreme weather metrics
st.markdown('<div class="section-header">Extreme Weather Events</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric(
        label="Highest Temperature",
        value=f"{filtered_extreme_days['hottest']['temperature']:.1f} °C",
    )
    st.caption(f"Date: {filtered_extreme_days['hottest']['date'].strftime('%b %d, %Y')}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric(
        label="Lowest Temperature",
        value=f"{filtered_extreme_days['coldest']['temperature']:.1f} °C",
    )
    st.caption(f"Date: {filtered_extreme_days['coldest']['date'].strftime('%b %d, %Y')}")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric(
        label="Highest Humidity",
        value=f"{filtered_extreme_days['most_humid']['humidity']:.1f}%",
    )
    st.caption(f"Date: {filtered_extreme_days['most_humid']['date'].strftime('%b %d, %Y')}")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric(
        label="Highest Rainfall",
        value=f"{filtered_extreme_days['wettest']['rainfall']:.1f} mm",
    )
    st.caption(f"Date: {filtered_extreme_days['wettest']['date'].strftime('%b %d, %Y')}")
    st.markdown('</div>', unsafe_allow_html=True)

# Tabs for different visualizations
st.markdown('<div class="section-header">Weather Analysis</div>', unsafe_allow_html=True)

tabs = st.tabs(["Time Series", "Monthly Trends", "Seasonal Analysis", "Correlations", "Comfort Index"])

with tabs[0]:  # Time Series tab
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    metric_option = st.selectbox(
        "Select Weather Metric",
        ["Temperature (°C)", "Humidity (%)", "Rainfall (mm)"],
        key="time_series_metric"
    )
    
    metric_mapping = {
        "Temperature (°C)": "temperature",
        "Humidity (%)": "humidity",
        "Rainfall (mm)": "rainfall"
    }
    
    selected_metric = metric_mapping[metric_option]
    
    # Create time series chart
    fig = px.line(
        filtered_data, 
        x='date', 
        y=selected_metric,
        title=f'{selected_metric.capitalize()} Over Time',
        color_discrete_sequence=['#1f77b4']
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=metric_option,
        height=500,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]:  # Monthly Trends tab
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Calculate monthly averages for the filtered data
    filtered_monthly_avg = get_monthly_averages(filtered_data)
    
    metric_option = st.selectbox(
        "Select Weather Metric",
        ["Temperature (°C)", "Humidity (%)", "Rainfall (mm)"],
        key="monthly_metric"
    )
    
    selected_metric = metric_mapping[metric_option]
    
    # Create monthly bar chart
    fig = px.bar(
        filtered_monthly_avg.reset_index(), 
        x='month_name', 
        y=selected_metric,
        title=f'Monthly Average {selected_metric.capitalize()}',
        color_discrete_sequence=['#2ca02c']
    )
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title=metric_option,
        height=500,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis={'categoryorder': 'array', 'categoryarray': filtered_monthly_avg.index.tolist()}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display monthly data in table
    with st.expander("View Monthly Data Table"):
        st.dataframe(filtered_monthly_avg.round(2), use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]:  # Seasonal Analysis tab
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Calculate seasonal averages for the filtered data
    filtered_seasonal_avg = get_seasonal_averages(filtered_data)
    
    # Create radar chart for seasonal comparison
    fig = go.Figure()
    
    # Add each metric as a trace
    fig.add_trace(go.Scatterpolar(
        r=filtered_seasonal_avg['temperature'].tolist() + [filtered_seasonal_avg['temperature'].iloc[0]],
        theta=['Winter', 'Spring', 'Summer', 'Fall', 'Winter'],
        fill='toself',
        name='Temperature (°C)',
        line_color='#ff7f0e'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=filtered_seasonal_avg['humidity'].tolist() + [filtered_seasonal_avg['humidity'].iloc[0]],
        theta=['Winter', 'Spring', 'Summer', 'Fall', 'Winter'],
        fill='toself',
        name='Humidity (%)',
        line_color='#1f77b4'
    ))
    
    # Scale rainfall to be visible on same chart
    rainfall_scaled = filtered_seasonal_avg['rainfall'] * 5
    fig.add_trace(go.Scatterpolar(
        r=rainfall_scaled.tolist() + [rainfall_scaled.iloc[0]],
        theta=['Winter', 'Spring', 'Summer', 'Fall', 'Winter'],
        fill='toself',
        name='Rainfall × 5 (mm)',
        line_color='#2ca02c'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(filtered_seasonal_avg['humidity'].max(), 
                              filtered_seasonal_avg['temperature'].max(), 
                              rainfall_scaled.max()) * 1.1]
            )
        ),
        title="Seasonal Weather Patterns",
        height=500,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display seasonal data in table
    with st.expander("View Seasonal Data Table"):
        st.dataframe(filtered_seasonal_avg.round(2), use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]:  # Correlations tab
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Create correlation heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    corr_matrix = get_correlation_data(filtered_data)
    
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    sns.heatmap(
        corr_matrix, 
        mask=mask, 
        cmap=cmap, 
        vmax=1, 
        vmin=-1, 
        center=0,
        square=True, 
        linewidths=.5, 
        cbar_kws={"shrink": .8},
        annot=True,
        fmt=".2f"
    )
    
    plt.title('Weather Metric Correlations')
    st.pyplot(fig)
    
    # Create scatter plots
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature vs Humidity scatter
        fig = px.scatter(
            filtered_data, 
            x="temperature", 
            y="humidity",
            color="season",
            title="Temperature vs. Humidity",
            labels={"temperature": "Temperature (°C)", "humidity": "Humidity (%)"},
            color_discrete_map={
                "Winter": "#1f77b4",
                "Spring": "#2ca02c",
                "Summer": "#ff7f0e",
                "Fall": "#d62728"
            }
        )
        
        fig.update_traces(marker=dict(size=8, opacity=0.6))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Humidity vs Rainfall scatter
        fig = px.scatter(
            filtered_data, 
            x="humidity", 
            y="rainfall",
            color="season",
            title="Humidity vs. Rainfall",
            labels={"humidity": "Humidity (%)", "rainfall": "Rainfall (mm)"},
            color_discrete_map={
                "Winter": "#1f77b4",
                "Spring": "#2ca02c",
                "Summer": "#ff7f0e",
                "Fall": "#d62728"
            }
        )
        
        fig.update_traces(marker=dict(size=8, opacity=0.6))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[4]:  # Comfort Index tab
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    st.write("""
    ### Weather Comfort Index
    
    This is a simple comfort index based on temperature and humidity. 
    Lower values indicate more comfortable weather conditions.
    
    - **Temperature Comfort**: Penalizes temperatures that deviate from 23°C (ideal temperature)
    - **Humidity Discomfort**: Penalizes humidity levels above the comfortable range (above 60%)
    """)
    
    # Filter the comfort data
    filtered_comfort = weather_data_comfort.copy()
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_comfort = filtered_comfort[(filtered_comfort['date'] >= pd.to_datetime(start_date)) & 
                                          (filtered_comfort['date'] <= pd.to_datetime(end_date))]

    if season_filter != "All Seasons":
        filtered_comfort = filtered_comfort[filtered_comfort['season'] == season_filter]
    
    # Create comfort index chart
    fig = px.line(
        filtered_comfort, 
        x='date', 
        y='comfort_index',
        title='Weather Comfort Index Over Time (Lower is Better)',
        color_discrete_sequence=['#9467bd']
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Comfort Index",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Comfort by season
    comfort_by_season = filtered_comfort.groupby('season')['comfort_index'].mean().reindex(["Winter", "Spring", "Summer", "Fall"])
    
    fig = px.bar(
        comfort_by_season.reset_index(), 
        x='season', 
        y='comfort_index',
        title='Average Comfort Index by Season (Lower is Better)',
        color_discrete_sequence=['#9467bd']
    )
    
    fig.update_layout(
        xaxis_title="Season",
        yaxis_title="Comfort Index",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Data Explorer Section
st.markdown('<div class="section-header">Data Explorer</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

with st.expander("View and Filter Raw Data"):
    # Number of rows to display
    num_rows = st.slider("Number of rows to display", 5, 100, 10)
    
    # Column selector
    all_columns = weather_data.columns.tolist()
    selected_columns = st.multiselect(
        "Select columns to display",
        all_columns,
        default=['date', 'temperature', 'humidity', 'rainfall', 'season']
    )
    
    if not selected_columns:
        selected_columns = ['date', 'temperature', 'humidity', 'rainfall', 'season']
    
    # Display the filtered data
    st.dataframe(filtered_data[selected_columns].head(num_rows), use_container_width=True)
    
    # Download button
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="weather_data_filtered.csv",
        mime="text/csv",
    )

st.markdown('</div>', unsafe_allow_html=True)

# Summary Statistics
st.markdown('<div class="section-header">Summary Statistics</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

with st.expander("View Summary Statistics"):
    summary_stats = get_summary_stats(filtered_data)
    st.dataframe(summary_stats, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Weather Data Dashboard Mini Project | Created with Streamlit, Pandas, and Plotly</div>', unsafe_allow_html=True)