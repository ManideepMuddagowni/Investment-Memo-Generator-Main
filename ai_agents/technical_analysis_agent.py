from .base import call_ai_agent
from datetime import datetime
def generate_technical_analysis(df):
    if df.empty or 'Close' not in df.columns:
        return "No technical analysis available."

    latest = df.iloc[-1]
    latest_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    prompt = f"""
    Analyze these technical indicators for the stock {latest_date}:\n"
    f"Open Price: {latest['Open']:.2f}\n"
    f"Close Price: {latest['Close']:.2f}\n"
    f"MA20: {latest['MA20']:.2f}\n"
    f"MA50: {latest['MA50']:.2f}\n"
    f"RSI: {latest['RSI']:.2f}\n"
    f"MACD: {latest['MACD']:.4f}\n"
    f"Signal Line: {latest['Signal']:.4f}"

    Provide a short interpretation of the trend and momentum.
    """
    return call_ai_agent(prompt)


