import os
import yfinance as yf
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")


def get_stock_data(ticker: str, live=True, period="6mo"):
    if live:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            info = stock.info
            if hist.empty or 'shortName' not in info:
                raise ValueError("No data found on yfinance.")
            return hist, info
        except Exception as e:
            print(f"[Warning] Could not fetch live data for '{ticker}': {e}")
            return pd.DataFrame(), {
                "shortName": ticker.upper(),
                "sector": "N/A",
                "marketCap": "N/A",
                "longBusinessSummary": "No live data available."
            }
    else:
        # LLM-only mode: Return empty DataFrame and minimal info
        return pd.DataFrame(), {
            "shortName": ticker.upper(),
            "sector": "N/A",
            "marketCap": "N/A",
            "longBusinessSummary": "No live data, LLM generated summary only."
        }

def get_from_alpha_vantage(ticker: str):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_KEY,
        "outputsize": "compact"
    }
    r = requests.get(url, params=params).json()
    ts = r.get("Time Series (Daily)", {})
    if not ts:
        raise ValueError("No data returned from Alpha Vantage.")

    df = pd.DataFrame.from_dict(ts, orient="index").sort_index()
    df = df.rename(columns={"5. adjusted close": "Close"})
    df["Close"] = df["Close"].astype(float)
    df.index = pd.to_datetime(df.index)

    metadata = {
        "shortName": ticker,
        "sector": "N/A",
        "marketCap": "N/A",
        "longBusinessSummary": "N/A"
    }
    return df.tail(120), metadata





# ----------------------------------------
# 2. Technical Indicators Agent
# ----------------------------------------

def get_stock_data(ticker, period="6mo"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    if hist.empty and period == "1d":
        hist = stock.history(period="5d").tail(1)

    # 🛠 Fix: Ensure 'Close' column exists
    if 'Close' not in hist.columns and 'Adj Close' in hist.columns:
        hist['Close'] = hist['Adj Close']
    elif 'Close' not in hist.columns:
        raise ValueError(f"'Close' column missing for {ticker}")

    info = stock.info
    if hist.empty or 'shortName' not in info:
        raise ValueError(f"No data found for ticker '{ticker}'")

    return hist, info

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_indicators(df):
    if df.empty or 'Close' not in df.columns:
        return df

    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()

    # Calculate RSI and add to df
    df['RSI'] = calculate_rsi(df['Close'], period=14)

    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df
