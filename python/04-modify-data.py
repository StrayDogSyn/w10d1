# Check original data
check_stationarity(daily_temp, 'Original Temperature')

# Check after removing trend and seasonality
stationary_temp = decomposition.resid.dropna()
# check_stationarity(stationary_temp, 'Residuals (Stationary)')
# "As expected, raw temperature data is non-stationary due to seasonality. But the residuals after decomposition are stationary!"
# Making Data Stationary Through Differencing:
# "When decomposition isn't appropriate, we can use differencing:"

# First-order differencing (remove trend)
diff_1 = daily_temp.diff().dropna()
check_stationarity(diff_1, 'First Difference')

# Seasonal differencing (remove seasonality)
diff_seasonal = daily_temp.diff(365).dropna()
check_stationarity(diff_seasonal, 'Seasonal Difference')

# Both trend and seasonal differencing
diff_both = daily_temp.diff().diff(365).dropna()
check_stationarity(diff_both, 'Trend + Seasonal Difference')
