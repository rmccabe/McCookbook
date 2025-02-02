#!/usr/bin/env python3
"""
interactive_ticker_gui.py

A minimal tkinter GUI to fetch stock data (via yfinance) for a user-specified ticker
and time period. Displays one Matplotlib chart at a time.

Usage:
    python interactive_ticker_gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt

def fetch_and_plot(ticker: str, period: str):
    """
    Downloads historical data for 'ticker' over the given 'period'
    and plots the Adjusted Close (or Close if 'Adj Close' unavailable).
    """
    if not ticker.strip():
        messagebox.showwarning("Input Error", "Please enter a valid ticker symbol.")
        return

    try:
        data = yf.Ticker(ticker).history(period=period)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download data: {e}")
        return

    if data.empty:
        messagebox.showinfo("No Data", f"No data returned for ticker '{ticker}' with period '{period}'.")
        return

    # Use 'Adj Close' if available, else 'Close'
    price_col = "Adj Close" if "Adj Close" in data.columns else "Close"

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(data.index, data[price_col], label=f"{ticker} ({period})", color="blue")
    plt.title(f"{ticker} Price Over {period}")
    plt.xlabel("Date")
    plt.ylabel(f"{price_col} (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()  # Blocks until user closes the chart window

def on_plot_click():
    """
    Callback for the "Plot Data" button.
    Reads the ticker and period from the GUI, then calls fetch_and_plot.
    """
    ticker = ticker_entry.get()
    period = period_var.get()
    fetch_and_plot(ticker, period)

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Stock Data Plotter (yfinance)")

    # Basic window layout
    # ------------------------------------------------------
    # Ticker Label + Entry
    ticker_label = ttk.Label(root, text="Stock Ticker:")
    ticker_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    global ticker_entry
    ticker_entry = ttk.Entry(root, width=15)
    ticker_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Period Label + Dropdown
    period_label = ttk.Label(root, text="Time Period:")
    period_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    # Common yfinance periods
    time_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "ytd", "max"]

    global period_var
    period_var = tk.StringVar(value=time_periods[2])  # default "1mo"

    period_dropdown = ttk.OptionMenu(root, period_var, time_periods[2], *time_periods)
    period_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Plot Button
    plot_button = ttk.Button(root, text="Plot Data", command=on_plot_click)
    plot_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Adjust spacing
    root.columnconfigure(1, weight=1)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
