import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt

# Load weather data
weather_data = pd.read_csv('weather_history.csv', parse_dates=['date'])
weather_data.set_index('date', inplace=True)

# Ensure we have daily frequency
daily_temp = weather_data['temperature'].resample('D').mean()

# Perform seasonal decomposition
decomposition = seasonal_decompose(daily_temp, model='additive', period=365)

# Plot the decomposition
fig, axes = plt.subplots(4, 1, figsize=(12, 10))
daily_temp.plot(ax=axes[0], title='Original Temperature Data')
decomposition.trend.plot(ax=axes[1], title='Trend Component')
decomposition.seasonal.plot(ax=axes[2], title='Seasonal Component')
decomposition.resid.plot(ax=axes[3], title='Residual Component')
plt.tight_layout()
plt.show()
