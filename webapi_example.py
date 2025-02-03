# 3_web_api_example.py
#
# Minimal FastAPI example that returns the latest stock price for a ticker.
'''
Run the API:
bash

uvicorn 3_web_api_example:app --reload


Go to http://127.0.0.1:8000/stock/AAPL in your browser or via curl to see JSON output like:
json

{
  "ticker": "AAPL",
  "last_close": 153.12
}

Pros:
Standard pattern for internal or external services in finance.
Integrates well with front-end dashboards or other systems.
'''

from fastapi import FastAPI, HTTPException
import yfinance as yf

app = FastAPI(
    title="Stock Price API",
    description="A simple FastAPI service to fetch the latest stock price from Yahoo Finance",
    version="1.0.0",
)

@app.get("/stock/{ticker}")
def get_stock_price(ticker: str):
    """
    Returns the current/last close price of the specified stock ticker.
    """
    try:
        data = yf.Ticker(ticker).history(period="1d")
        if data.empty:
            raise HTTPException(status_code=404, detail="No data found for that ticker.")

        last_close = data["Close"].iloc[-1]
        return {"ticker": ticker, "last_close": round(last_close, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
