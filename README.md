# SPY-volatility-estimator
This is a project for estimating SPY future volatility using 2 different methods.


## EGARCH

The first method is using EGARCH.You can set start and end dates for the historical data , but keep in mind that for garch models atleast a 1000 data points are recommended(in this case meaning atleast a 1000 days of historical data).We are using EGARCH instead of GARCH because it more accurately captures the key characteristics of financial return volatility — especially asymmetry and leverage effects.

In financial markets, negative shocks (e.g., price drops) often increase volatility more than positive shocks of the same magnitude. This behavior is known as the leverage effect.
Standard GARCH assumes that volatility responds symmetrically to past shocks, meaning it treats positive and negative returns the same when updating volatility.
EGARCH, on the other hand, models the log of the variance, which:
Guarantees positivity of variance without parameter constraints,
Allows for asymmetric response to shocks (via the alpha term),
Better fits empirical data for assets like equities or ETFs.

When you exeecute the script it will print out the next day forecasted volatiltiy along with a summary for the model:
<img width="631" alt="Screenshot 2025-06-20 at 16 35 29" src="https://github.com/user-attachments/assets/d3d9ae4c-a4fe-403f-8199-7ed7dbba1025" />
