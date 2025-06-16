
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA

# Load time series
df = pd.read_csv('weather_history.csv', parse_dates=['date'])
df.set_index('date', inplace=True)
series = df['temperature'].dropna()

# Differencing (d=1)
diff_series = series.diff().dropna()

# ACF and PACF plots
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(diff_series, lags=30, ax=ax[0])
plot_pacf(diff_series, lags=30, ax=ax[1])
plt.tight_layout()
plt.show()

# Fit ARIMA(1,1,1) model as an example
model = ARIMA(series, order=(1, 1, 1))
result = model.fit()
print(result.summary())

