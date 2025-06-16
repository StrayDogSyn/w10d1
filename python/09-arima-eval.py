from pmdarima import auto_arima

# Automatic model selection
auto_model = auto_arima(train, 
                       start_p=0, start_q=0, 
                       max_p=5, max_q=5,
                       seasonal=True, m=52,  # weekly seasonality
                       stepwise=True,
                       suppress_warnings=True,
                       error_action='ignore')

print(f"Best model: {auto_model.order}")
if auto_model.seasonal_order:
    print(f"Seasonal order: {auto_model.seasonal_order}")

# Generate forecasts
auto_forecast = auto_model.predict(n_periods=len(test))
Comparing Multiple Approaches:
python
# Let's compare all our approaches
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def create_lag_features(data, n_lags=7):import matplotlib.pyplot as plt


# In[24]:


plt.figure(figsize=(10,8))
plt.plot(df['DATE'], df['TMAX'], label="Max Temp", color="red")
plt.plot(df['DATE'], df['TMIN'], label="Min Temp", color="green")
plt.xlabel('Date')
plt.ylabel('Temp')
plt.show()

    """Create lag features for ML models"""
    df = pd.DataFrame(data)
    for lag in range(1, n_lags + 1):
        df[f'lag_{lag}'] = df[data.name].shift(lag)
    return df.dropna()

# Prepare data for ML models
ml_data = create_lag_features(daily_temp, n_lags=7)
split_idx = int(len(ml_data) * 0.8)

X_train = ml_data.iloc[:split_idx, 1:]
y_train = ml_data.iloc[:split_idx, 0]
X_test = ml_data.iloc[split_idx:, 1:]
y_test = ml_data.iloc[split_idx:, 0]

# Train different models
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
}

ml_results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    ml_results[name] = {'predictions': predictions, 'mse': mse}

# Combine all results
all_results = {
    'ARIMA': {'mse': results[best_order]['mse']},
    'SARIMA': {'mse': sarima_mse * 7},  # Approximate daily MSE
    **{k: {'mse': v['mse']} for k, v in ml_results.items()}
}

# Visualize comparison
plt.figure(figsize=(10, 6))
models_names = list(all_results.keys())
mse_values = [all_results[m]['mse'] for m in models_names]

plt.bar(models_names, mse_values, color=['blue', 'green', 'red', 'orange'])
plt.ylabel('Mean Squared Error')
plt.title('Model Comparison for Weather Forecasting')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Print detailed comparison
print("\nModel Performance Summary:")
print("-" * 50)
for model, metrics in all_results.items():
    print(f"{model:20} MSE: {metrics['mse']:.2f}")
Residual Diagnostics:
"A good model should have residuals that are:
    1. Randomly distributed (no patterns)
    2. Normally distributed
    3. No autocorrelation"
python
# Diagnostic plots for best ARIMA model
best_model = results[best_order]['model']

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Residual plot
residuals = best_model.resid
axes[0,0].plot(residuals)
axes[0,0].set_title('Residuals')
axes[0,0].axhline(y=0, color='r', linestyle='--')

# Histogram of residuals
axes[0,1].hist(residuals, bins=30)
axes[0,1].set_title('Residual Distribution')

# Q-Q plot
from scipy import stats
stats.probplot(residuals, dist="norm", plot=axes[1,0])
axes[1,0].set_title('Q-Q Plot')

# ACF of residuals
plot_acf(residuals, ax=axes[1,1], lags=20)
axes[1,1].set_title('ACF of Residuals')

plt.tight_layout()
plt.show()

# Ljung-Box test for residual autocorrelation
from statsmodels.stats.diagnostic import acorr_ljungbox
lb_test = acorr_ljungbox(residuals, lags=[10], return_df=True)
print("\nLjung-Box Test for Residual Autocorrelation:")
print(lb_test)
print("p-value > 0.05 indicates no significant autocorrelation")
