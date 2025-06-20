import yfinance as yf
import pandas as pd
from datetime import datetime

# Load existing data
df_existing = pd.read_csv("spy.csv")
df_existing["Date"] = pd.to_datetime(df_existing["Date"])

# Get last date in your CSV
last_date = df_existing["Date"].max().date()

# Fetch new data from the next day to today
today = datetime.today().date()
if last_date >= today:
    print("Data already up to date.")
    exit()
else:
    df_new = yf.download("SPY", start=last_date + pd.Timedelta(days=1), end=today + pd.Timedelta(days=1), interval="1d",auto_adjust=False)
    df_new.reset_index(inplace=True)
    if df_new["Date"].max().date() == last_date:
        print("Data already up to date.")
        exit()
    # Clean to match schema
    df_new = df_new[["Date", "Close", "Open", "High", "Low", "Volume"]]
    # Flatten MultiIndex columns
    if isinstance(df_new.columns, pd.MultiIndex):
        df_new.columns = df_new.columns.get_level_values(0)
    # Remove column index name
    df_new.columns.name = None

    # Reset index if needed (just to be sure)
    df_new = df_new.reset_index(drop=True)
    df_new = df_new.sort_values("Date").reset_index(drop=True)
    df_new["Change %"] = df_new["Close"].pct_change() * 100
    df_new["Change %"] = df_new["Change %"].round(2).astype(str) + "%"
    df_new["Change %"].iloc[0] = "0.00%"
    df_new = df_new.rename(columns={
        "Date": "Date",
        "Open": "Open",
        "High": "High",
        "Low": "Low",
        "Close": "Price",
        "Volume": "Vol."

    })
    df_new["Date"] = df_new["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df_new["Price"] = df_new["Price"].round(2)
    df_new["Open"] = df_new["Open"].round(2)
    df_new["High"] = df_new["High"].round(2)
    df_new["Low"] = df_new["Low"].round(2)
    df_new.sort_values(by="Date",ascending=False,inplace=True)
    df_updated = pd.concat([df_new, df_existing],ignore_index=True)
    df_updated = df_updated[["Date", "Price", "Open", "High", "Low", "Vol.", "Change %"]]
    print(df_updated.head())
    print(df_updated.columns)
    df_updated.to_csv("spy.csv", index=False)
    print(f"Appended {len(df_new)} new rows to spy.csv")
