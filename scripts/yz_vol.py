import pandas as pd
import numpy as np
df = pd.read_csv("spy.csv")
df["Date"] = pd.to_datetime(df["Date"])
end_date = "2025-06-05"
start_date = "2025-04-21"
df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
df_filtered["Change %"] = df_filtered["Change %"].str.replace("%","").astype(float).copy()
df_filtered["Price"] = df_filtered["Price"].astype(float).copy()
df_filtered["High"] = df_filtered["High"].astype(float).copy()
df_filtered["Low"] = df_filtered["Low"].astype(float).copy()
df_filtered["Open"] = df_filtered["Open"].astype(float).copy()
realized_vol = np.std(df_filtered["Change %"],ddof=1)
df_filtered = df_filtered.drop(columns=["Vol."])
df_filtered = df_filtered.sort_values("Date").reset_index(drop=True)

# --- Yang-Zhang Volatility Estimator
# Convert prices to log values
df_filtered["log_open"] = np.log(df_filtered["Open"])
df_filtered["log_close"] = np.log(df_filtered["Price"])
df_filtered["log_high"] = np.log(df_filtered["High"])
df_filtered["log_low"] = np.log(df_filtered["Low"])

# Lagged close for overnight return
df_filtered["log_prev_close"] = df_filtered["log_close"].shift(1)

# Compute components
df_filtered["overnight"] = df_filtered["log_open"] - df_filtered["log_prev_close"]
df_filtered["open_to_close"] = df_filtered["log_close"] - df_filtered["log_open"]
df_filtered["rs"] = (
    (df_filtered["log_high"] - df_filtered["log_open"]) * (df_filtered["log_high"] - df_filtered["log_close"]) +
    (df_filtered["log_low"] - df_filtered["log_open"]) * (df_filtered["log_low"] - df_filtered["log_close"])
)


# Drop first row (NaN from lag)
df_yz = df_filtered.dropna().copy()

df_yz = df_yz.replace([np.inf, -np.inf], np.nan).dropna(subset=["overnight", "open_to_close", "rs"])

n_original= len(df_filtered)
# Compute variances
sigma_o = np.var(df_yz["overnight"], ddof=0)
sigma_c = np.var(df_yz["open_to_close"], ddof=0)
sigma_rs = df_yz["rs"].mean()

# Compute weighting factor k
k = 0.34 / (1.34 + (n_original + 1)/(n_original - 1))


# Yang-Zhang variance
yz_var = sigma_o + k * sigma_c + (1 - k) * sigma_rs
yang_zhang_vol = np.sqrt(yz_var) * 100  # scale to % for comparison

# --- Output both
print(f"σ_o (overnight variance): {sigma_o:.6f}")
print(f"σ_c (open-to-close variance): {sigma_c:.6f}")
print(f"σ_rs (RS term mean): {sigma_rs:.6f}")
print(f"Weight k: {k:.6f}")
print("Realized Close-to-Close Volatility: {:.4f}%".format(realized_vol))
print("Yang-Zhang Volatility: {:.4f}%".format(yang_zhang_vol))
