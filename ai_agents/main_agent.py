from .financial_summary_agent import generate_financial_summary
from .technical_analysis_agent import generate_technical_analysis
from .news_sentiment_agent import generate_news_sentiment
from .risk_opportunity_agent import generate_risks_opportunities

def generate_investment_memo(info, df, ticker):
    print("[Main Agent] Generating financial summary...")
    financial_summary = generate_financial_summary(info)

    print("[Main Agent] Generating technical analysis...")
    if not df.empty:
        technical_summary = generate_technical_analysis(df)
    else:
        technical_summary = "No technical analysis available."

    print("[Main Agent] Generating news sentiment...")
    sentiment_summary = generate_news_sentiment(ticker)

    print("[Main Agent] Generating risks and opportunities...")
    risks_opportunities = generate_risks_opportunities(financial_summary, technical_summary, sentiment_summary)

    # Compose final memo
    memo = f"""
    ===== Investment Memo =====

    Executive Summary:
    {financial_summary}

    Technical Analysis:
    {technical_summary}

    Market Sentiment:
    {sentiment_summary}

    Risks and Opportunities:
    {risks_opportunities}
    """
    return memo.strip()
