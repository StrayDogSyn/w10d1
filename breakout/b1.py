"""
Weather Data Analysis Script
----------------------------

This script provides a reusable function to analyze a weather variable for:
1. Seasonal decomposition
2. Stationarity testing
3. Differencing to achieve stationarity

Required CSV: weather_history.csv with columns:
- date
- temperature

Author: Evan Misshula
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# Load and prepare weather data
weather_data = pd.read_csv('weather_history.csv', parse_dates=['date'])
weather_data.set_index('date', inplace=True)

# Ensure daily frequency with resampling
weather_data = weather_data.resample('D').mean()

def check_stationarity(timeseries, title):
    """Perform ADF test and plot time series + histogram."""
    result = adfuller(timeseries.dropna())
    adf_statistic = result[0]
    p_value = result[1]
    
    print(f'Results for {title}:')
    print(f'ADF Statistic: {adf_statistic:.4f}')
    print(f'p-value: {p_value:.4f}')
    print('Critical Values:')
    
    # Handle critical values safely
    if len(result) > 4 and hasattr(result[4], 'items'):
        critical_values = result[4]
        for key, value in critical_values.items():
            print(f'  {key}: {value:.3f}')
    else:
        print('  Critical values not available in expected format')
    
    if p_value <= 0.05:
        print("✓ Data is stationary (reject null hypothesis)")
    else:
        print("✗ Data is non-stationary (fail to reject null hypothesis)")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    timeseries.plot(ax=axes[0], title=f'{title} - Time Series')
    timeseries.hist(ax=axes[1], bins=50)
    axes[1].set_title(f'{title} - Distribution')
    plt.tight_layout()
    plt.show()

def analyze_weather_variable(data, variable_name, period=365):
    """Decompose and test a weather variable for stationarity."""
    series = data[variable_name].dropna()

    # 1. Seasonal decomposition
    decomposition = seasonal_decompose(series, model='additive', period=period)
    fig, axes = plt.subplots(4, 1, figsize=(12, 10))
    series.plot(ax=axes[0], title='Original Data')
    decomposition.trend.plot(ax=axes[1], title='Trend')
    decomposition.seasonal.plot(ax=axes[2], title='Seasonality')
    decomposition.resid.plot(ax=axes[3], title='Residuals')
    plt.tight_layout()
    plt.show()

    # 2. Stationarity testing
    check_stationarity(series, 'Original Series')
    check_stationarity(decomposition.resid.dropna(), 'Residuals')

    # 3. Differencing
    diff_1 = series.diff().dropna()
    check_stationarity(diff_1, 'First Difference')

    diff_seasonal = series.diff(period).dropna()
    check_stationarity(diff_seasonal, 'Seasonal Difference')

    diff_both = series.diff().diff(period).dropna()
    check_stationarity(diff_both, 'First + Seasonal Difference')

# Run the analysis for temperature
analyze_weather_variable(weather_data, 'temperature')
