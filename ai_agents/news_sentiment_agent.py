from .base import call_ai_agent

def generate_news_sentiment(ticker):
    prompt = f"""
    Imagine you have recent news headlines about {ticker}. Summarize the overall sentiment (positive, neutral, negative) and key points.
    """
    return call_ai_agent(prompt)
