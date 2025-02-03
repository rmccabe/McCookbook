# 1_data_science_notebook_example.py
#
# This snippet demonstrates how a data scientist or finance engineer
# might explore data interactively in a Jupyter notebook.

# Jupyter-specific: often you'd see something like:
# %matplotlib inline
# to display plots inline in the notebook. (We'll omit that here for script form.)

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# 1) Download sample market data (e.g., Apple stock over 3 years)
ticker = yf.Ticker("AAPL")
df = ticker.history(period="3y")

# 2) Basic exploratory analysis
print("Dataframe head:")
print(df.head(), "\n")

print("Dataframe info:")
print(df.info(), "\n")

# 3) Compute daily returns
df["Daily Return"] = df["Close"].pct_change()

# 4) Plot the Close price
plt.figure(figsize=(10, 4))
plt.plot(df.index, df["Close"], label="AAPL Close Price", color="blue")
plt.title("Apple Close Price over 3 years")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.show()

# 5) Quick stats on daily returns
mean_return = df["Daily Return"].mean()
volatility = df["Daily Return"].std()
print(f"Mean daily return: {mean_return:.4%}")
print(f"Volatility (std dev) : {volatility:.4%}")

# Typical usage in a Notebook:
# - Additional cells might explore correlation with macro data,
#   plot moving averages, or run more advanced analysis.
