from fuzzywuzzy import process
import yfinance as yf
import pandas as pd
import pandas as ta  # Make sure you have this installed: pip install pandas_ta

def build_ticker_dict():
    return {
        "Tesla Inc": "TSLA",
        "Apple Inc": "AAPL",
        "Microsoft Corporation": "MSFT",
        "Amazon.com Inc": "AMZN",
        "Alphabet Inc": "GOOGL"
    }

def get_closest_ticker(company_name, ticker_dict):
    match, score = process.extractOne(company_name, ticker_dict.keys())
    if score >= 70:
        return ticker_dict[match]
    return None

def get_stock_data(ticker, period="6mo"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    # For 1d period fallback: get last available day if empty
    if hist.empty and period == "1d":
        hist = stock.history(period="5d").tail(1)
    info = stock.info
    if hist.empty or 'shortName' not in info:
        raise ValueError(f"No data found for ticker '{ticker}'")
    return hist, info

def get_live_price(ticker):
    stock = yf.Ticker(ticker)
    try:
        price = stock.fast_info['lastPrice']
    except (KeyError, AttributeError):
        info = stock.info
        price = info.get('regularMarketPrice', None)
    return price

