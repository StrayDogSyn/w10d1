## 🔍 Model Coefficients & Summary

```
Covariance Type: opg
```

* The standard errors and confidence intervals were calculated using the **outer product of gradients (OPG)** method.
* This is one way to estimate uncertainty in your model parameters; it’s often used when the model likelihood is non-linear.

---

### 📈 Coefficient Table

| Term   | Estimate | Std. Error | z-Score | p-value | 95% CI            |
| ------ | -------- | ---------- | ------- | ------- | ----------------- |
| ar.L1  | 0.5182   | 0.025      | 20.64   | 0.000   | [0.469, 0.567]   |
| ma.L1  | -0.8919  | 0.014      | -63.76  | 0.000   | [-0.919, -0.864] |
| sigma² | 48.86    | 1.35       | 36.24   | 0.000   | [y46.22, 51.50]   |

#### ✳️ Interpretation:

* **ar.L1 = 0.5182**: This means the current value of the series is positively correlated with the previous value ($y_{t-1}$). The AR(1) term is statistically significant (p < 0.001).
* **ma.L1 = -0.8919**: This MA(1) term tells us the current value is influenced by the *error* from the previous time step — strong negative correlation. Again, highly significant.
* **sigma² = 48.86**: Estimated variance of the residuals (white noise). This is not standardized; it reflects scale of your data.

---

## ✅ Model Diagnostics

| Test                       | Value | p-value | Interpretation                                                  |
| -------------------------- | ----- | ------- | --------------------------------------------------------------- |
| **Ljung–Box (L1)**         | 7.21  | 0.01    | Reject null: residuals may still have autocorrelation.          |
| **Jarque–Bera**            | 66.09 | 0.00    | Reject normality: residuals are not normally distributed.       |
| **Skew**                   | -0.07 | —       | Near 0: slight left skew, not concerning.                       |
| **Kurtosis**               | 3.89  | —       | Above 3: distribution is slightly heavier-tailed than a normal. |
| **Heteroskedasticity (H)** | 1.00  | 0.98    | Fail to reject null: no evidence of heteroskedasticity (good).  |

---

## 🎯 Overall Model Assessment

* ✅ The **AR and MA terms are statistically significant**, and model seems well-fit in terms of structure.
* ❌ However, **residuals fail the Ljung–Box test** → still some autocorrelation left over. You may need to increase AR or MA order.
* ❌ **Residuals are not normally distributed** (based on JB test and kurtosis), which could affect confidence intervals.
* ✅ No sign of **heteroskedasticity**, which is good for modeling stability.

## 📌 Recommendations

* Check **ACF and PACF plots** of residuals to see where autocorrelation remains.
* Consider:

  * Increasing model order (e.g., AR(2) or MA(2))
  * Applying a **Box-Cox transformation** or **log scale** if the data is skewed
* Use `plot_diagnostics()` from `statsmodels` to visualize residual patterns
