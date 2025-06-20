# SPY-volatility-estimator
This is a project for estimating SPY future volatility using 2 different methods.


## EGARCH

The first method is using EGARCH.You can set start and end dates for the historical data , but keep in mind that for garch models atleast a 1000 data points are recommended(in this case meaning atleast a 1000 days of historical data).We are using EGARCH instead of GARCH because it more accurately captures the key characteristics of volatility — asymmetry and leverage effects.

In financial markets, negative shocks (e.g., price drops) often increase volatility more than positive shocks of the same magnitude. This behavior is known as the leverage effect.
Standard GARCH assumes that volatility responds symmetrically to past shocks, meaning it treats positive and negative returns the same when updating volatility.
EGARCH, on the other hand, models the log of the variance, which:
Guarantees positivity of variance without parameter constraints,
Allows for asymmetric response to shocks (via the alpha term),
Better fits empirical data for assets like equities or ETFs.

When you exeecute the script it will print out the next day forecasted volatiltiy along with a summary for the model:
<img width="631" alt="Screenshot 2025-06-20 at 16 35 29" src="https://github.com/user-attachments/assets/d3d9ae4c-a4fe-403f-8199-7ed7dbba1025" />
Mean=0
We assume no deterministic trend (mean=0)

Distribution: Normal
Assumes residuals follow a normal distribution. (Can be changed to t-distribution for fat tails.)

Dep. Variable	
The series being modeled — here, the log returns of SPY.

Log-Likelihood
Higher values imply a better model fit.

AIC & BIC	Information criteria — lower is better. Used for model comparison.

No. Observations
Number of data points used (1297 daily returns).

omega (ω)	Constant term in the variance equation. Sets the long-run average variance.
alpha[1] (α)	Measures the reaction to new shocks in volatility. Higher = more reactive.
beta[1] (β)	Persistence of past volatility. Closer to 1 = longer memory.


R^2 = 0.000
This is not important for volatility models. GARCH-type models focus on predicting variance (not the mean), so R^2 isn't meaningful.

The model tells us that SPY volatility has a low but stable base level (omega),reacts quickly to shocks in the market (alpha),and stays elevated for a long time after a shock (beta).
This is exactly the kind of behavior we see in financial time series like SPY: volatility spikes suddenly and fades gradually.


## YANG-ZHANG Volatility estimator
