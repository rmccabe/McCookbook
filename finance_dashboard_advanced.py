#!/usr/bin/env python3
"""
advanced_finance_dashboard.py

A multi-tab financial dashboard that:
  - Tab 1 (Dashboard):
      • Fetches and plots stock data (with 50- and 200-day moving averages).
      • Displays stock performance (start/end prices + absolute/percentage change).
      • Displays macroeconomic indicators as a range from the stock's start date
        (or a custom Macro Date) to the current date, including:
          - Fed Funds Rate
          - Unemployment Rate
          - YoY Inflation (CPI)
          - US Treasury yields for 1-, 5-, 10-, 30-year
          - Nonfarm Payrolls
          - Housing Starts
          - US GDP (latest available)
  - Tab 2 (Ticker Info):
      • Pulls company details from Yahoo Finance (country, currency, sector, industry, website, etc.).
  - Provides a splash screen, single "Fetch Data" button, status messages for loading, and
    an auto-refresh option with a configurable interval.

Requires:
    pip install yfinance pandas-datareader wbdata matplotlib pandas
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
import wbdata
import matplotlib

matplotlib.use("TkAgg")  # Use TkAgg for embedding in tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------------------------------------------------------------------------
# Helper: Update status bar with a message, then force UI to update
# ------------------------------------------------------------------------------------
def set_status(message):
    status_bar.config(text=message)
    root.update_idletasks()  # Force refresh of the interface

# ------------------------------------------------------------------------------------
# Helper Functions for FRED
# ------------------------------------------------------------------------------------
def get_fred_value(series_id, target_date, window=30):
    """
    Fetches a FRED series for a window around target_date,
    returns the last value on or before target_date and its date.
    """
    start = target_date - datetime.timedelta(days=window)
    end = target_date + datetime.timedelta(days=window)
    data = pdr.get_data_fred(series_id, start=start, end=end)
    if data.empty:
        return None, None
    subset = data.loc[:target_date]
    if subset.empty:
        return None, None
    value = subset.iloc[-1, 0]
    date_str = subset.index[-1].strftime("%Y-%m-%d")
    return round(value, 2), date_str

def get_fred_range(series_id, start_date, end_date, window=30):
    """
    Returns a tuple:
      (val_start, date_start, val_end, date_end)
    for the given FRED series, representing the value at start_date
    and the value at end_date (with a window).
    """
    v_start, d_start = get_fred_value(series_id, start_date, window)
    v_end, d_end = get_fred_value(series_id, end_date, window)
    return v_start, d_start, v_end, d_end

def get_inflation_value(target_date):
    """
    Computes YoY inflation from the CPIAUCSL series (CPI),
    returning (inflation_percent, date_str).
    """
    start = target_date - datetime.timedelta(days=400)
    end = target_date + datetime.timedelta(days=30)
    data = pdr.get_data_fred("CPIAUCSL", start=start, end=end)
    if data.empty:
        return None, None
    current_subset = data.loc[:target_date]
    if current_subset.empty:
        return None, None
    current_value = current_subset.iloc[-1, 0]
    current_date = current_subset.index[-1]
    prev_date = target_date - datetime.timedelta(days=365)
    prev_subset = data.loc[:prev_date]
    if prev_subset.empty:
        return None, None
    previous_value = prev_subset.iloc[-1, 0]
    inflation = ((current_value - previous_value) / previous_value) * 100
    return round(inflation, 2), current_date.strftime("%Y-%m-%d")

def get_inflation_range(start_date, end_date):
    """
    Returns (infl_start, date_start, infl_end, date_end),
    representing inflation at start_date and end_date.
    """
    s_val, s_dt = get_inflation_value(start_date)
    e_val, e_dt = get_inflation_value(end_date)
    return s_val, s_dt, e_val, e_dt

def get_gdp_value(target_date):
    """
    Fetches US GDP data from the World Bank, returning (gdp_in_trillions, year).
    gdp_in_trillions is the data on or before target_date.
    """
    indicators = {"NY.GDP.MKTP.CD": "GDP"}
    gdp_data = wbdata.get_dataframe(indicators, country="US")
    if gdp_data.empty:
        return None, None
    try:
        gdp_data.index = pd.to_datetime(gdp_data.index, format="%Y")
    except Exception:
        return None, None
    subset = gdp_data[gdp_data.index <= target_date]
    if subset.empty:
        return None, None
    value = subset.iloc[-1, 0] / 1e12
    year = subset.index[-1].year
    return round(value, 2), year

# ------------------------------------------------------------------------------------
# Stock Data Functions
# ------------------------------------------------------------------------------------
def update_all_data():
    """
    Single entry-point to refresh:
      1) Stock data & chart
      2) Macro data (range from stock start date or custom Macro Date to current date)
      3) Ticker info
    """
    update_stock_data()  # This also calls update_macro_data() and update_ticker_info()

def update_stock_data():
    """Fetches stock data, updates chart & performance, sets Macro Date if empty, calls macro & ticker updates."""
    ticker = ticker_entry.get().strip()
    period = period_var.get()

    if not ticker:
        messagebox.showwarning("Input Error", "Please enter a valid stock ticker.")
        return

    set_status(f"Loading stock data for {ticker} (Period: {period})...")
    root.update_idletasks()

    try:
        data = yf.Ticker(ticker).history(period=period)
    except Exception as e:
        set_status("Error loading stock data.")
        messagebox.showerror("Data Fetch Error", f"Failed to download stock data:\n{e}")
        return

    if data.empty:
        set_status("No data found.")
        messagebox.showinfo("No Data", f"No stock data found for '{ticker}' with period '{period}'.")
        return

    price_col = "Adj Close" if "Adj Close" in data.columns else "Close"

    # Calculate moving averages
    data["MA50"] = data[price_col].rolling(window=50).mean()
    data["MA200"] = data[price_col].rolling(window=200).mean()

    # Update chart
    ax_stock.clear()
    ax_stock.plot(data.index, data[price_col], label=price_col, color="blue")
    ax_stock.plot(data.index, data["MA50"], label="50-Day MA", color="orange")
    ax_stock.plot(data.index, data["MA200"], label="200-Day MA", color="green")
    ax_stock.set_title(f"{ticker} Price Over {period}")
    ax_stock.set_xlabel("Date")
    ax_stock.set_ylabel("Price (USD)")
    ax_stock.legend()
    ax_stock.grid(True)
    canvas_stock.draw()

    # Stock performance info
    start_price = data[price_col].iloc[0]
    end_price = data[price_col].iloc[-1]
    price_change = end_price - start_price
    pct_change = (price_change / start_price) * 100

    stock_start_label_value.config(text=f"${start_price:.2f}")
    stock_end_label_value.config(text=f"${end_price:.2f}")
    stock_change_label_value.config(text=f"${price_change:.2f} ({pct_change:.2f}%)")
    last_update_label.config(text=f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Update Macro Date if none is provided
    stock_start_date_str = data.index[0].strftime("%Y-%m-%d")
    if not macro_date_entry.get().strip():
        macro_date_entry.delete(0, tk.END)
        macro_date_entry.insert(0, stock_start_date_str)

    # Now fetch macro data
    update_macro_data()

    # Also update ticker info
    update_ticker_info()

    set_status("Fetch complete.")

def update_macro_data():
    """
    Fetches macro data (range: Macro Date -> Today) for:
      - Fed Funds Rate
      - Unemployment
      - Treasury Yields (1,5,10,30)
      - Nonfarm Payrolls (PAYEMS)
      - Housing Starts (HOUST)
      - YoY Inflation
      - US GDP (most recent)
    """
    macro_date_str = macro_date_entry.get().strip()
    if not macro_date_str:
        return  # Skip if still empty

    # Show status
    set_status("Loading macro data from FRED & World Bank...")
    root.update_idletasks()

    try:
        start_date = datetime.datetime.strptime(macro_date_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Date Error", "Macro Date must be YYYY-MM-DD.")
        set_status("Macro date error.")
        return

    end_date = datetime.datetime.today()

    try:
        # Fed Funds Rate
        fed_s, fed_sd, fed_e, fed_ed = get_fred_range("FEDFUNDS", start_date, end_date, window=30)
        # Unemployment
        unemp_s, unemp_sd, unemp_e, unemp_ed = get_fred_range("UNRATE", start_date, end_date, window=30)
        # Inflation (YoY)
        infl_s, infl_sd = get_inflation_value(start_date)
        infl_e, infl_ed = get_inflation_value(end_date)

        # US Treasury Yields
        bond1_s, bond1_sd, bond1_e, bond1_ed = get_fred_range("DGS1", start_date, end_date, window=30)
        bond5_s, bond5_sd, bond5_e, bond5_ed = get_fred_range("DGS5", start_date, end_date, window=30)
        bond10_s, bond10_sd, bond10_e, bond10_ed = get_fred_range("DGS10", start_date, end_date, window=30)
        bond30_s, bond30_sd, bond30_e, bond30_ed = get_fred_range("DGS30", start_date, end_date, window=30)

        # Nonfarm Payrolls (in thousands)
        nf_s, nf_sd, nf_e, nf_ed = get_fred_range("PAYEMS", start_date, end_date, window=30)
        # Housing Starts (in thousands)
        hs_s, hs_sd, hs_e, hs_ed = get_fred_range("HOUST", start_date, end_date, window=30)

        # US GDP (just current)
        gdp_val, gdp_year = get_gdp_value(end_date)

        # Format to show range
        if fed_s is not None:
            interest_label_value.config(text=f"{fed_s}% (as of {fed_sd}) → {fed_e}% (as of {fed_ed})")
        else:
            interest_label_value.config(text="N/A")

        if unemp_s is not None:
            unemployment_label_value.config(text=f"{unemp_s}% (as of {unemp_sd}) → {unemp_e}% (as of {unemp_ed})")
        else:
            unemployment_label_value.config(text="N/A")

        if infl_s is not None:
            inflation_label_value.config(text=f"{infl_s}% (as of {infl_sd}) → {infl_e}% (as of {infl_ed})")
        else:
            inflation_label_value.config(text="N/A")

        # Bond Yields
        bond1_label_value.config(text=(f"{bond1_s}% (as of {bond1_sd}) → {bond1_e}% (as of {bond1_ed})")
                                   if bond1_s is not None else "N/A")
        bond5_label_value.config(text=(f"{bond5_s}% (as of {bond5_sd}) → {bond5_e}% (as of {bond5_ed})")
                                  if bond5_s is not None else "N/A")
        bond10_label_value.config(text=(f"{bond10_s}% (as of {bond10_sd}) → {bond10_e}% (as of {bond10_ed})")
                                   if bond10_s is not None else "N/A")
        bond30_label_value.config(text=(f"{bond30_s}% (as of {bond30_sd}) → {bond30_e}% (as of {bond30_ed})")
                                   if bond30_s is not None else "N/A")

        # Nonfarm
        if nf_s is not None:
            nonfarm_label_value.config(text=f"{nf_s}k (as of {nf_sd}) → {nf_e}k (as of {nf_ed})")
        else:
            nonfarm_label_value.config(text="N/A")

        # Housing
        if hs_s is not None:
            housing_label_value.config(text=f"{hs_s}k (as of {hs_sd}) → {hs_e}k (as of {hs_ed})")
        else:
            housing_label_value.config(text="N/A")

        # GDP
        if gdp_val is not None:
            gdp_label_value.config(text=f"${gdp_val} Trillion (year {gdp_year})")
        else:
            gdp_label_value.config(text="N/A")

    except Exception as e:
        set_status("Macro data error.")
        messagebox.showerror("Macro Data Error", f"Failed to fetch macroeconomic data:\n{e}")
        return

    set_status("Fetch complete.")

def update_ticker_info():
    """Fetches ticker info from yfinance and updates the Ticker Info tab."""
    ticker = ticker_entry.get().strip()
    if not ticker:
        return
    set_status(f"Loading Ticker Info for {ticker}...")
    root.update_idletasks()

    try:
        info = yf.Ticker(ticker).info
    except Exception as e:
        set_status("Error loading ticker info.")
        messagebox.showerror("Data Fetch Error", f"Failed to fetch ticker info:\n{e}")
        return

    name = info.get("longName") or info.get("shortName") or "N/A"
    country = info.get("country", "N/A")
    currency = info.get("currency", "N/A")
    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    website = info.get("website", "N/A")

    ticker_name_value.config(text=name)
    ticker_country_value.config(text=country)
    ticker_currency_value.config(text=currency)
    ticker_sector_value.config(text=sector)
    ticker_industry_value.config(text=industry)
    ticker_website_value.config(text=website)

# ------------------------------------------------------------------------------------
# Splash Screen
# ------------------------------------------------------------------------------------
def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x200+500+400")
    splash_label = ttk.Label(splash, text="Loading Finance Dashboard...", font=("Arial", 16))
    splash_label.pack(expand=True)
    root.after(2000, splash.destroy)
    root.after(2000, lambda: (root.deiconify(), update_all_data()))

# ------------------------------------------------------------------------------------
# Main Application
# ------------------------------------------------------------------------------------
root = tk.Tk()
root.title("Advanced Finance Dashboard")
root.geometry("1400x1000")
root.minsize(1400, 1000)

# Menu Bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Notebook with two tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# --- Tab 1: Dashboard ---
tab_dashboard = ttk.Frame(notebook)
notebook.add(tab_dashboard, text="Dashboard")

# Input Frame
dashboard_input_frame = ttk.Frame(tab_dashboard, padding=10)
dashboard_input_frame.pack(fill="x")
dashboard_input_frame.columnconfigure(1, weight=1)

# Row 0
ttk.Label(dashboard_input_frame, text="Stock Ticker:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
ticker_entry = ttk.Entry(dashboard_input_frame, width=15, font=("Arial", 12))
ticker_entry.insert(0, "AAPL")
ticker_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
ticker_entry.bind("<Return>", lambda event: update_all_data())

ttk.Label(dashboard_input_frame, text="Time Period:", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5, sticky="e")
time_periods = ["1mo", "3mo", "6mo", "1y", "5y", "ytd", "max"]
period_var = tk.StringVar(value="1mo")
dropdown = ttk.OptionMenu(dashboard_input_frame, period_var, "1mo", *time_periods)
dropdown.config(width=10)
dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="w")

ttk.Label(dashboard_input_frame, text="Macro Date (YYYY-MM-DD):", font=("Arial", 12)).grid(row=0, column=4, padx=5, pady=5, sticky="e")
macro_date_entry = ttk.Entry(dashboard_input_frame, width=12, font=("Arial", 12))
macro_date_entry.grid(row=0, column=5, padx=5, pady=5, sticky="w")

auto_refresh_var = tk.BooleanVar(value=False)
auto_refresh_check = ttk.Checkbutton(dashboard_input_frame, text="Auto Refresh", variable=auto_refresh_var)
auto_refresh_check.grid(row=0, column=6, padx=5, pady=5, sticky="w")

ttk.Label(dashboard_input_frame, text="Interval (ms):", font=("Arial", 12)).grid(row=0, column=7, padx=5, pady=5, sticky="e")
refresh_interval = tk.IntVar(value=60000)
refresh_entry = ttk.Entry(dashboard_input_frame, width=8, textvariable=refresh_interval, font=("Arial", 12))
refresh_entry.grid(row=0, column=8, padx=5, pady=5, sticky="w")

fetch_btn = ttk.Button(dashboard_input_frame, text="Fetch Data", command=update_all_data)
fetch_btn.grid(row=0, column=9, padx=10, pady=5)

# Chart Frame
chart_frame = ttk.Frame(tab_dashboard, padding=10)
chart_frame.pack(fill="both", expand=True)
fig_stock, ax_stock = plt.subplots(figsize=(10, 6), dpi=100)
canvas_stock = FigureCanvasTkAgg(fig_stock, master=chart_frame)
canvas_stock.get_tk_widget().pack(fill="both", expand=True)

# Stock Performance Info
stock_info_frame = ttk.Frame(tab_dashboard, relief="groove", padding=10)
stock_info_frame.pack(fill="x", padx=10, pady=10)
ttk.Label(stock_info_frame, text="Stock Performance", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
ttk.Label(stock_info_frame, text="Start Price:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5)
stock_start_label_value = ttk.Label(stock_info_frame, text="N/A", font=("Arial", 12, "bold"))
stock_start_label_value.grid(row=1, column=1, sticky="w", padx=5)
ttk.Label(stock_info_frame, text="End Price:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5)
stock_end_label_value = ttk.Label(stock_info_frame, text="N/A", font=("Arial", 12, "bold"))
stock_end_label_value.grid(row=2, column=1, sticky="w", padx=5)
ttk.Label(stock_info_frame, text="Change:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=5)
stock_change_label_value = ttk.Label(stock_info_frame, text="N/A", font=("Arial", 12, "bold"))
stock_change_label_value.grid(row=3, column=1, sticky="w", padx=5)
last_update_label = ttk.Label(stock_info_frame, text="Last Updated: N/A", font=("Arial", 10))
last_update_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=5)

# Macro Data Info
macro_info_frame = ttk.Frame(tab_dashboard, relief="groove", padding=10)
macro_info_frame.pack(fill="x", padx=10, pady=10)

ttk.Label(macro_info_frame, text="Macro Indicators (Range: Start→Now)", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=5)

# Fed Funds, Unemployment
ttk.Label(macro_info_frame, text="Fed Funds Rate:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5)
interest_label_value = ttk.Label(macro_info_frame, text="N/A", font=("Arial", 12, "bold"))
interest_label_value.grid(row=1, column=1, sticky="w")

ttk.Label(macro_info_frame, text="Unemployment Rate:", font=("Arial", 12)).grid(row=1, column=2, sticky="w", padx=5)
unemployment_label_value = ttk.Label(macro_info_frame, text="N/A", font=("Arial", 12, "bold"))
unemployment_label_value.grid(row=1, column=3, sticky="w")

# Inflation, 1yr Yield
ttk.Label(macro_info_frame, text="YoY Inflation:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5)
inflation_label_value = ttk.Label(macro_info_frame, text="N/A", font=("Arial", 12, "bold"))
inflation_label_value.grid(row=2, column=1, sticky="w")

ttk.Label(macro_info_frame, text="1-Year Yield:", font=("Arial", 12)).grid(row=2, column=2, sticky="w", padx=5)
bond1_label_value = ttk.Label(macro_info_frame, text="N/A", font=("Arial", 12, "bold"))
bond1_label_value.grid(row=2, column=3, sticky="w")

# 5yr, 10yr
ttk.Label(macro_info_frame, text="5-Year Yield:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=5)
bond5_label_value = ttk.Label(macro_info_frame, text="N/A", font=("Arial", 12, "bold"))
bond5_label_value.grid(row=3, column=1, sticky="w")

ttk.Label(macro_info_frame, text="10-Year Yield:", font=("Arial", 12)).grid(row=3, column=2, sticky="w", padx=5)
bond10_label_value = ttk.Label(macro_info_frame, text="N/A", font=("Arial", 12, "bold"))
bond10_label_value.grid(row=3, column=3, sticky="w")

# 30yr, GDP
ttk.Label(macro_info_frame, text="30-Year Yield:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=5)
bond30_label_value = ttk.Label(macro_info_frame, text="N/A", font=("Arial", 12, "bold"))
bond30_label_value.grid(row=4, column=1, sticky="w")

ttk.Label(macro_info_frame, text="US GDP:", font=("Arial", 12)).grid(row=4, column=2, sticky="w", padx=5)
gdp_label_value = ttk.Label(macro_info_frame, text="N/A", font=("Arial", 12, "bold"))
gdp_label_value.grid(row=4, column=3, sticky="w")

# Nonfarm Payrolls, Housing Starts
ttk.Label(macro_info_frame, text="Nonfarm Payrolls:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=5)
nonfarm_label_value = ttk.Label(macro_info_frame, text="N/A", font=("Arial", 12, "bold"))
nonfarm_label_value.grid(row=5, column=1, sticky="w")

ttk.Label(macro_info_frame, text="Housing Starts:", font=("Arial", 12)).grid(row=5, column=2, sticky="w", padx=5)
housing_label_value = ttk.Label(macro_info_frame, text="N/A", font=("Arial", 12, "bold"))
housing_label_value.grid(row=5, column=3, sticky="w")

# --- Tab 2: Ticker Info
tab_ticker = ttk.Frame(notebook)
notebook.add(tab_ticker, text="Ticker Info")

ticker_info_frame = ttk.Frame(tab_ticker, padding=10)
ticker_info_frame.pack(fill="both", expand=True)
ticker_info_frame.columnconfigure(1, weight=1)

ttk.Label(ticker_info_frame, text="Ticker Information", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
ttk.Label(ticker_info_frame, text="Company Name:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
ticker_name_value = ttk.Label(ticker_info_frame, text="N/A", font=("Arial", 12, "bold"))
ticker_name_value.grid(row=1, column=1, sticky="w", padx=5, pady=5)

ttk.Label(ticker_info_frame, text="Country:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
ticker_country_value = ttk.Label(ticker_info_frame, text="N/A", font=("Arial", 12, "bold"))
ticker_country_value.grid(row=2, column=1, sticky="w", padx=5, pady=5)

ttk.Label(ticker_info_frame, text="Currency:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
ticker_currency_value = ttk.Label(ticker_info_frame, text="N/A", font=("Arial", 12, "bold"))
ticker_currency_value.grid(row=3, column=1, sticky="w", padx=5, pady=5)

ttk.Label(ticker_info_frame, text="Sector:", font=("Arial", 12)).grid(row=4, column=0, sticky="e", padx=5, pady=5)
ticker_sector_value = ttk.Label(ticker_info_frame, text="N/A", font=("Arial", 12, "bold"))
ticker_sector_value.grid(row=4, column=1, sticky="w", padx=5, pady=5)

ttk.Label(ticker_info_frame, text="Industry:", font=("Arial", 12)).grid(row=5, column=0, sticky="e", padx=5, pady=5)
ticker_industry_value = ttk.Label(ticker_info_frame, text="N/A", font=("Arial", 12, "bold"))
ticker_industry_value.grid(row=5, column=1, sticky="w", padx=5, pady=5)

ttk.Label(ticker_info_frame, text="Website:", font=("Arial", 12)).grid(row=6, column=0, sticky="e", padx=5, pady=5)
ticker_website_value = ttk.Label(ticker_info_frame, text="N/A", font=("Arial", 12, "bold"), foreground="blue", cursor="hand2")
ticker_website_value.grid(row=6, column=1, sticky="w", padx=5, pady=5)

def open_website(event):
    import webbrowser
    site = ticker_website_value.cget("text")
    if site and site != "N/A":
        webbrowser.open(site)

ticker_website_value.bind("<Button-1>", open_website)

# ------------------------------------------------------------------------------------
# Status Bar (bottom)
# ------------------------------------------------------------------------------------
status_bar = ttk.Label(root, text="Welcome to the Advanced Finance Dashboard", relief="sunken", anchor="w", font=("Arial", 10))
status_bar.pack(side="bottom", fill="x")

# ------------------------------------------------------------------------------------
# Auto-Refresh
# ------------------------------------------------------------------------------------
def auto_refresh():
    if auto_refresh_var.get():
        update_all_data()
    root.after(refresh_interval.get(), auto_refresh)

root.after(refresh_interval.get(), auto_refresh)

# ------------------------------------------------------------------------------------
# Splash Screen and Main Loop
# ------------------------------------------------------------------------------------
root.withdraw()
def splash_screen():
    show_splash()

splash_screen()

root.mainloop()
