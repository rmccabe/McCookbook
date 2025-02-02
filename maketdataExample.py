#!/usr/bin/env python3
"""
market_data_plot.py

Fetches historical market data for a given stock ticker from Yahoo Finance
(via yfinance) and displays it on separate subplots for preset time periods.

Usage:
    python market_data_plot.py

Dependencies:
    pip install yfinance matplotlib
"""

import yfinance as yf
import matplotlib.pyplot as plt

def plot_stock_data_for_periods(ticker: str, periods=None):
    """
    Downloads market data for the specified 'ticker' from Yahoo Finance,
    then plots the 'Adj Close' price for each preset time period on separate subplots.

    :param ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'GOOG')
    :param periods: List of time periods accepted by yfinance's 'history' method
                    (e.g., ['1mo', '3mo', '6mo', '1y']). Defaults to a common set.
    """
    if periods is None:
        # Common preset periods: 1m, 3m, 6m, 1y, 5y, ytd, etc.
        periods = ["1mo", "3mo", "6mo", "1y"]

    # We'll create one subplot per period
    fig, axes = plt.subplots(len(periods), 1, figsize=(10, 5 * len(periods)), sharex=False)
    fig.suptitle(f"{ticker} Stock Price - Various Time Periods", fontsize=16)

    for i, period in enumerate(periods):
        # Download data for this period
        # 'history(period=...)' automatically ends at the current date
        print(f"Downloading data for ticker={ticker}, period={period}...")
        data = yf.Ticker(ticker).history(period=period)

        # Plot on the respective subplot
        ax = axes[i] if len(periods) > 1 else axes  # axes is an array if multiple, single if 1
        if "Adj Close" in data.columns:
          ax.plot(data.index, data["Adj Close"], label="Adj Close")
        else:
            ax.plot(data.index, data["Close"], label="Close")

        #ax.plot(data.index, data["Adj Close"], label=f"{ticker} ({period})", color="blue")
        ax.set_title(f"Time Period: {period}")
        ax.set_ylabel("Adj Close Price (USD)")
        ax.legend()
        ax.grid(True)

    # Adjust spacing
    plt.tight_layout()
    # Move the main title a bit to avoid overlap
    fig.subplots_adjust(top=0.92)
    plt.show()


def main():
    # Example usage
    # Modify TICKER and PERIODS to your preference
    TICKER = "AAPL"  # Apple, for demonstration
    PERIODS = ["1mo", "3mo", "6mo", "1y", "5y"]  # Example periods

    plot_stock_data_for_periods(TICKER, PERIODS)


if __name__ == "__main__":
    main()
