import pandas as pd
import numpy as np
from arch import arch_model

# Load and clean the data
df = pd.read_csv("spy.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Define date range and filter, using .copy() to avoid warning
end_date = "2025-06-05"
start_date = "2020-04-15"
df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)].copy()

# Clean numeric columns
df_filtered["Change %"] = df_filtered["Change %"].str.replace("%", "").astype(float)
df_filtered["Price"] = df_filtered["Price"].astype(float)
df_filtered["High"] = df_filtered["High"].astype(float)
df_filtered["Low"] = df_filtered["Low"].astype(float)
df_filtered["Open"] = df_filtered["Open"].astype(float)
df_filtered = df_filtered.drop(columns=["Vol."])

# Sort by date ascending for GARCH
df_filtered = df_filtered.sort_values("Date").reset_index(drop=True)

# Recalculate returns using log differences
df_filtered["log_return"] = np.log(df_filtered["Price"]).diff()

# Drop NA from diff
returns = df_filtered["log_return"].dropna() * 100  # scale to %

#Fit GARCH(1,1)
model = arch_model(returns, mean='zero', vol='EGARCH', p=1, q=1, rescale=True)
res = model.fit(disp="off")

# Forecast 1-day ahead volatility
forecast = res.forecast(horizon=1)
next_vol = np.sqrt(forecast.variance.iloc[-1, 0])  # Daily volatility in % scale

print(f"Next day forecasted volatility: {next_vol:.4f}%")
print(res.summary())
