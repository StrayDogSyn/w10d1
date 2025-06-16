import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

# (1) Stationary AR(1): φ=0.7
np.random.seed(42)
n = 200
y_stat = np.zeros(n)
for t in range(1, n):
    y_stat[t] = 0.7 * y_stat[t-1] + np.random.normal()

# (2) Unit‑root: φ=1 (random walk)
y_rw = np.cumsum(np.random.normal(size=n))

def test_series(y, title):
    print(title)
    result = adfuller(y, regression='c', maxlag=0)
    print(f"ADF stat = {result[0]:.3f}, p‑value = {result[1]:.3f}")
    for key, val in result[4].items():
        print(f"  {key}: {val:.3f}")
    print()

test_series(y_stat, "Stationary AR(1)")
test_series(y_rw,  "Random Walk")
 
