#!/usr/bin/env python3
"""
finance_dashboard_gui.py

A tkinter GUI that:
  - Fetches stock market data (via yfinance)
  - Fetches macroeconomic indicators (Fed Funds Rate, Unemployment, Inflation, US GDP)
  - Displays both in a single window with an embedded Matplotlib chart
  - Shows a splash screen at startup

Usage:
    python finance_dashboard_gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime

import yfinance as yf
from pandas_datareader import data as pdr
import wbdata

import matplotlib
matplotlib.use("TkAgg")  # Use TkAgg for embedding in tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Function to Fetch Market Data and Update Chart ---
def update_plot():
    """
    Fetches stock data for the selected ticker and period,
    updates the embedded Matplotlib chart, and then fetches macro data.
    """
    ticker = ticker_entry.get().strip()
    period = period_var.get()

    if not ticker:
        messagebox.showwarning("Input Error", "Please enter a valid stock ticker.")
        return

    try:
        data = yf.Ticker(ticker).history(period=period)
    except Exception as e:
        messagebox.showerror("Data Fetch Error", f"Failed to download stock data:\n{e}")
        return

    if data.empty:
        messagebox.showinfo("No Data", f"No stock data found for '{ticker}' with period '{period}'.")
        return

    # Use Adjusted Close if available, otherwise use Close
    price_col = "Adj Close" if "Adj Close" in data.columns else "Close"

    # Clear previous chart and plot new data
    ax.clear()
    ax.plot(data.index, data[price_col], label=f"{ticker} ({period})", color="blue")
    ax.set_title(f"{ticker} Price Over {period}")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"{price_col} (USD)")
    ax.legend()
    ax.grid(True)
    canvas.draw()

    # After updating the chart, update macro data
    update_macro_data()


# --- Function to Fetch and Update Macro Data ---
def update_macro_data():
    """
    Fetches macroeconomic indicators from FRED and World Bank,
    then updates the corresponding labels with both value and date.
    """
    try:
        # Define a 5-year date range for FRED data
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(days=365 * 5)

        # Fetch FRED data for US Macroeconomic Indicators
        interest_rate = pdr.get_data_fred("FEDFUNDS", start=start_date, end=end_date)
        unemployment_rate = pdr.get_data_fred("UNRATE", start=start_date, end=end_date)
        inflation_rate = pdr.get_data_fred("CPIAUCSL", start=start_date, end=end_date)

        # Extract the most recent values and their dates
        interest_value = round(interest_rate.iloc[-1, 0], 2)
        interest_date = interest_rate.index[-1].strftime("%Y-%m-%d")

        unemployment_value = round(unemployment_rate.iloc[-1, 0], 2)
        unemployment_date = unemployment_rate.index[-1].strftime("%Y-%m-%d")

        inflation_value = round(
            ((inflation_rate.iloc[-1, 0] - inflation_rate.iloc[-12, 0]) / inflation_rate.iloc[-12, 0]) * 100,
            2
        )
        inflation_date = inflation_rate.index[-1].strftime("%Y-%m-%d")

        # Fetch World Bank GDP Data for the US
        indicators = {"NY.GDP.MKTP.CD": "GDP"}
        gdp_data = wbdata.get_dataframe(indicators, country="US")
        gdp_value = round(gdp_data.iloc[-1, 0] / 1e12, 2)  # Convert dollars to trillions
        # Use the year of the latest GDP data
        gdp_date = gdp_data.index[-1].year if hasattr(gdp_data.index[-1], "year") else "N/A"

        # Update UI Labels with values and their dates
        interest_label_value.config(text=f"{interest_value}% (as of {interest_date})")
        unemployment_label_value.config(text=f"{unemployment_value}% (as of {unemployment_date})")
        inflation_label_value.config(text=f"{inflation_value}% YoY (as of {inflation_date})")
        gdp_label_value.config(text=f"${gdp_value} Trillion (as of {gdp_date})")

    except Exception as e:
        messagebox.showerror("Macro Data Error", f"Failed to fetch macroeconomic data:\n{e}")


# --- Splash Screen ---
def show_splash():
    """
    Displays a splash screen while the main window is loading.
    """
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x200+300+200")  # Adjust position and size as needed
    splash_label = ttk.Label(splash, text="Loading Finance Dashboard...", font=("Arial", 16))
    splash_label.pack(expand=True)

    # After 2 seconds, destroy the splash screen and show the main window
    root.after(2000, splash.destroy)
    root.after(2000, lambda: (root.deiconify(), update_plot()))  # Deiconify and update data


# --- Create Main Application Window ---
root = tk.Tk()
root.title("Finance Dashboard")
root.geometry("1000x700")  # Set an initial larger window size
root.minsize(1000, 700)    # Enforce a minimum size

# Configure grid so that frames expand with the window
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)  # The chart row

# --- 1) INPUT FRAME (Ticker & Period Selection) ---
input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
input_frame.columnconfigure(1, weight=1)

ttk.Label(input_frame, text="Stock Ticker:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
ticker_entry = ttk.Entry(input_frame, width=15, font=("Arial", 12))
ticker_entry.insert(0, "AAPL")  # Prepopulate with "AAPL"
ticker_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

ttk.Label(input_frame, text="Time Period:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
time_periods = ["1mo", "3mo", "6mo", "1y", "5y", "ytd", "max"]
period_var = tk.StringVar(value="1mo")
dropdown = ttk.OptionMenu(input_frame, period_var, "1mo", *time_periods)
# Removed the font configuration here as OptionMenu does not support the 'font' option directly.
dropdown.config(width=10)
dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

plot_btn = ttk.Button(input_frame, text="Fetch Data", command=update_plot, style="Accent.TButton")
plot_btn.grid(row=2, column=0, columnspan=2, pady=10)

# --- 2) MATPLOTLIB CHART EMBEDDED ---
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# --- 3) MACRO DATA DISPLAY (Below the Chart) ---
macro_frame = ttk.Frame(root, relief="groove", padding=10)
macro_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
macro_frame.columnconfigure(1, weight=1)

ttk.Label(macro_frame, text="Macro Indicators", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

ttk.Label(macro_frame, text="Fed Funds Rate:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5)
interest_label_value = ttk.Label(macro_frame, text="Fetching...", font=("Arial", 12, "bold"))
interest_label_value.grid(row=1, column=1, sticky="w")

ttk.Label(macro_frame, text="Unemployment Rate:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5)
unemployment_label_value = ttk.Label(macro_frame, text="Fetching...", font=("Arial", 12, "bold"))
unemployment_label_value.grid(row=2, column=1, sticky="w")

ttk.Label(macro_frame, text="Inflation Rate (YoY):", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=5)
inflation_label_value = ttk.Label(macro_frame, text="Fetching...", font=("Arial", 12, "bold"))
inflation_label_value.grid(row=3, column=1, sticky="w")

ttk.Label(macro_frame, text="US GDP:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=5)
gdp_label_value = ttk.Label(macro_frame, text="Fetching...", font=("Arial", 12, "bold"))
gdp_label_value.grid(row=4, column=1, sticky="w")

# Initially hide the main window and show a splash screen for a fast startup
root.withdraw()  # Hide the main window
show_splash()

# Start the Tkinter event loop
root.mainloop()
