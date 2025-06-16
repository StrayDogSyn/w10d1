# Building ARIMA Models:
# python
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# Split data for time series (no shuffle!)
train_size = int(len(daily_temp) * 0.8)
train, test = daily_temp[:train_size], daily_temp[train_size:]

# Method 1: Manual ARIMA with specific orders
def fit_arima_model(train_data, order):
    model = ARIMA(train_data, order=order)
    model_fit = model.fit()
    return model_fit

# Try different ARIMA orders
orders_to_try = [(1,1,1), (2,1,1), (1,1,2), (2,1,2)]
results = {}

for order in orders_to_try:
    try:
        print(f"\nFitting ARIMA{order}...")
        model_fit = fit_arima_model(train, order)
        
        # Make predictions
        predictions = model_fit.forecast(steps=len(test))
        
        # Calculate metrics
        mse = mean_squared_error(test, predictions)
        mae = mean_absolute_error(test, predictions)
        aic = model_fit.aic
        
        results[order] = {
            'model': model_fit,
            'predictions': predictions,
            'mse': mse,
            'mae': mae,
            'aic': aic
        }
        
        print(f"AIC: {aic:.2f}, MSE: {mse:.2f}, MAE: {mae:.2f}")
        
    except Exception as e:
        print(f"Failed to fit ARIMA{order}: {e}")
 
# Find best model by AIC
best_order = min(results.keys(), key=lambda x: results[x]['aic'])
print(f"\nBest model by AIC: ARIMA{best_order}")
# SARIMA for Seasonal Data:
# "For weather data with strong seasonality, we use SARIMA (Seasonal ARIMA):"
# python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# SARIMA adds seasonal components: SARIMA(p,d,q)(P,D,Q)s
# where s is the seasonal period (365 for daily data with yearly seasonality)

def fit_sarima_model(train_data, order, seasonal_order):
    model = SARIMAX(train_data, 
                    order=order, 
                    seasonal_order=seasonal_order,
                    enforce_stationarity=False,
                    enforce_invertibility=False)
    return model.fit(disp=False)

# Example: SARIMA(1,1,1)(1,1,1)365
# This is computationally intensive, so we'll use a simpler seasonal period
weekly_temp = daily_temp.resample('W').mean()
train_weekly = weekly_temp[:int(len(weekly_temp)*0.8)]
test_weekly = weekly_temp[int(len(weekly_temp)*0.8):]

# Fit SARIMA with weekly seasonality (52 weeks)
sarima_model = fit_sarima_model(train_weekly, 
                                order=(1,1,1), 
                                seasonal_order=(1,1,1,52))

# Forecast
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Fit SARIMA model with timeout protection
def fit_sarima():
    model = SARIMAX(train_weekly,
                    order=(1, 1, 1),
                    seasonal_order=(1, 1, 1, 52),
                    enforce_stationarity=False,
                    enforce_invertibility=False)
    return model.fit(disp=False)

# Start the timer
start = time.time()
results = None

with ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(fit_sarima)
    try:
        results = future.result(timeout=180)
        end = time.time()
        print(f"✅ Converged in {end - start:.2f} seconds")
    except TimeoutError:
        print("❌ Model fitting timed out after 180 seconds.")

# Proceed only if model converged
if results is not None:
    # Forecast
    sarima_forecast = results.forecast(steps=len(test_weekly))

    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(train_weekly.index, train_weekly, label='Training Data')
    plt.plot(test_weekly.index, test_weekly, label='Actual')
    plt.plot(test_weekly.index, sarima_forecast, label='SARIMA Forecast', color='red')
    plt.legend()
    plt.title('SARIMA Weather Forecast')
    plt.ylabel('Temperature')
    plt.show()

    # Calculate performance
    sarima_mse = mean_squared_error(test_weekly, sarima_forecast)
    print(f"SARIMA MSE: {sarima_mse:.2f}")
else:
    print("⚠️ Skipping forecast and evaluation due to failed convergence.")


# Calculate performance
sarima_mse = mean_squared_error(test_weekly, sarima_forecast)
print(f"SARIMA MSE: {sarima_mse:.2f}")
