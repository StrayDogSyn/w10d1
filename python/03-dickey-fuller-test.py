# Notice how the decomposition reveals:
#     • A slight warming trend over the years
#     • Clear seasonal patterns (summer vs winter)
#     • Random variations after removing trend and seasonality"
# Understanding Stationarity:
# "For many time series models, especially ARIMA, we need our data to be 'stationary'. This means:
#     • Constant mean over time
#     • Constant variance over time
#     • No seasonal patterns
# Why? Because it's much easier to model and predict stationary data. Let's check if our temperature data is stationary:"

from statsmodels.tsa.stattools import adfuller

def check_stationarity(timeseries, title):
    # Perform Augmented Dickey-Fuller test
    result = adfuller(timeseries.dropna())
    
    print(f'Results for {title}:')
    print(f'ADF Statistic: {result[0]:.4f}')
    print(f'p-value: {result[1]:.4f}')
    print(f'Critical Values:')
    for key, value in result[4].items():
        print(f'\t{key}: {value:.3f}')
    
    if result[1] <= 0.05:
        print("✓ Data is stationary (reject null hypothesis)")
    else:
        print("✗ Data is non-stationary (fail to reject null hypothesis)")
    
    # Visual check
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    timeseries.plot(ax=axes[0], title=f'{title} - Time Series')
    timeseries.hist(ax=axes[1], bins=50)
    axes[1].set_title(f'{title} - Distribution')
    plt.tight_layout()
    plt.show()

# Check original data
check_stationarity(daily_temp, 'Original Temperature')

# Check after removing trend and seasonality
stationary_temp = decomposition.resid.dropna()
check_stationarity(stationary_temp, 'Residuals (Stationary)')
"As expected, raw temperature data is non-stationary due to seasonality. But the residuals after decomposition are stationary!"
Making Data Stationary Through Differencing:
"When decomposition isn't appropriate, we can use differencing:"
python
# First-order differencing (remove trend)
diff_1 = daily_temp.diff().dropna()
check_stationarity(diff_1, 'First Difference')

# Seasonal differencing (remove seasonality)
diff_seasonal = daily_temp.diff(365).dropna()
check_stationarity(diff_seasonal, 'Seasonal Difference')

# Both trend and seasonal differencing
diff_both = daily_temp.diff().diff(365).dropna()
check_stationarity(diff_both, 'Trend + Seasonal Difference')
