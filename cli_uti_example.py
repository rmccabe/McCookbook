# 2_cli_utility_example.py
#
# Example of a Python CLI tool for fetching stock data and printing
# a quick summary. This can be expanded or scheduled in a cron job.

#usage: python 2_cli_utility_example.py AAPL --period 6mo


import argparse
import yfinance as yf
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Simple CLI to fetch stock data and print a price summary."
    )
    parser.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL)")
    parser.add_argument("--period", default="1mo", help="Data period (e.g., 1mo, 3mo, 1y, etc.)")
    args = parser.parse_args()

    ticker = args.ticker
    period = args.period

    # Fetch data
    print(f"Fetching data for {ticker}, period={period}...")
    try:
        df = yf.Ticker(ticker).history(period=period)
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    if df.empty:
        print("No data returned. Check your ticker or period.")
        sys.exit(1)

    # Compute summary
    start_price = df["Close"].iloc[0]
    end_price = df["Close"].iloc[-1]
    change = end_price - start_price
    pct_change = (change / start_price) * 100

    print(f"Start Price: ${start_price:.2f}")
    print(f"End Price:   ${end_price:.2f}")
    print(f"Change:      ${change:.2f}  ({pct_change:.2f}%)")

if __name__ == "__main__":
    main()
