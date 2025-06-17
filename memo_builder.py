from analysis import get_stock_data, calculate_indicators
from ai_agents.main_agent import generate_investment_memo

def build_memo(ticker):
    df, info = get_stock_data(ticker)
    df = calculate_indicators(df)
    memo = generate_investment_memo(info, df, ticker)
    return memo
