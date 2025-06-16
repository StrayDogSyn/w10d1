# Demonstrating AR component
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# AR example: Create synthetic AR(1) data
np.random.seed(42)
ar_data = [10]
for i in range(100):
    ar_data.append(0.7 * ar_data[-1] + np.random.normal(0, 1))

axes[0,0].plot(ar_data)
axes[0,0].set_title('AR(1) Process: y_t = 0.7 * y_{t-1} + error')

# MA example: Create synthetic MA(1) data  
ma_data = []
errors = np.random.normal(0, 1, 101)
for i in range(100):
    if i == 0:
        ma_data.append(10 + errors[i])
    else:
        ma_data.append(10 + errors[i] + 0.5 * errors[i-1])

axes[0,1].plot(ma_data)
axes[0,1].set_title('MA(1) Process: y_t = 10 + error_t + 0.5 * error_{t-1}')

# ACF and PACF for model identification
plot_acf(daily_temp.dropna(), ax=axes[1,0], lags=40)
axes[1,0].set_title('ACF of Temperature Data')

plot_pacf(daily_temp.dropna(), ax=axes[1,1], lags=40)
axes[1,1].set_title('PACF of Temperature Data')

plt.tight_layout()
plt.show()
