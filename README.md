# SPY-volatility-estimator
This is a project for predicting SPY future volatility and estimating historical volatility using 2 different methods.


## EGARCH

The first method is using EGARCH to forecast the next day volatility.You can set start and end dates for the historical data , but keep in mind that for garch models atleast a 1000 data points are recommended(in this case meaning atleast a 1000 days of historical data).We are using EGARCH instead of GARCH because it more accurately captures the key characteristics of volatility — asymmetry and leverage effects.

<img width="629" alt="Screenshot 2025-06-21 at 16 20 44" src="https://github.com/user-attachments/assets/ee443f31-f6c7-4677-aada-11b31b9fa2b3" />


In financial markets, negative shocks (e.g., price drops) often increase volatility more than positive shocks of the same magnitude. This behavior is known as the leverage effect.
Standard GARCH assumes that volatility responds symmetrically to past shocks, meaning it treats positive and negative returns the same when updating volatility.
EGARCH, on the other hand, models the log of the variance, which allows for asymmetric response to shocks (via the alpha term) and better fits data for assets like equities or ETFs.

When you exeecute the script it will print out the next day forecasted volatiltiy along with a summary for the model:
<img width="631" alt="Screenshot 2025-06-20 at 16 35 29" src="https://github.com/user-attachments/assets/d3d9ae4c-a4fe-403f-8199-7ed7dbba1025" />


Mean=0

We assume no deterministic trend (mean=0).
While it uis well known that the S&P 500 has an upward price trend, volatility models like EGARCH operate on returns, not prices.
Returns are usually stationary (they fluctuate around a relatively stable mean), while prices are non-stationary. For simplicity and to focus purely on modeling volatility, we will assume the mean of returns is zero — that is, there's no consistent predictable return on a daily basis.

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

This is an advanced and robust method for estimating historical volatility. It combines overnight volatility(close to next day open), open to close volatility and the Rogers-Satchell estimator(intraday high and low prices). This makes it more comprehensive and less biased than close-to-close(realized) volatility, Garman-Klaas and Rogers-Satchell estimators individually.

You can set the range for which you want to calculate the volatility by changing the start_date and end_date variables. 

<img width="330" alt="Screenshot 2025-06-21 at 12 20 54" src="https://github.com/user-attachments/assets/a52e3e7e-eb17-4b05-a740-8547a947beb1" />

When you run the script it will print out the YZ vol. for the given date range along with some of the parameters for the calculation.
I also inlcuded a calculation for the close-to-close(realized vol.) for comparison.

Here you can see how the YZ vol. is different from the realized because of overnight gaps and intraday highs and lows:

<img width="356" alt="Screenshot 2025-06-21 at 12 24 13" src="https://github.com/user-attachments/assets/80dd1f60-eb65-4c2a-b10d-d58a90bb54a3" />


## Loading the data

The load_data.py script is responsible for updating the dataset (spy.csv) with the latest daily price data for the S&P 500 ETF (SPY) using the yfinance API.You don't need to change anything here .You can run it when you want to add new daily data to the spy.csv file.



