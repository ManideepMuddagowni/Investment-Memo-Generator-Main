from .base import call_ai_agent

def generate_financial_summary(info):
    live_data_available = info.get("longBusinessSummary") != "No live data, LLM generated summary only." and \
                          "AI model's knowledge" not in info.get("longBusinessSummary", "")

    if live_data_available:
        prompt = f"""
            You are an investment analyst. Based on the following company data, generate a structured investment memo with the following sections:

            1. Executive Summary  
            2. Company Overview  
            3. Industry Context  
            4. Technical Analysis (based on assumed market trends)  
            5. Market Sentiment (based on general perception and recent performance)  
            6. Risks and Opportunities  
            7. Investment Outlook  

            Company Name: {info.get('shortName', 'N/A')}  
            Sector: {info.get('sector', 'N/A')}  
            Market Cap: {info.get('marketCap', 'N/A')}  
            Country: {info.get('country', 'N/A')}  
            Business Summary: {info.get('longBusinessSummary', 'N/A')}  

            Keep the tone formal and factual. Use bullet points where appropriate. If technical or sentiment data is unavailable, use a general assumption based on the company's sector and market position.
            """

    else:
        prompt = f"""
        You are an expert financial analyst. Summarize the company {info.get('shortName', 'N/A')} based purely on your knowledge.
        No live stock price, market, or recent news data is available.
        Provide an investment memo summary based on general company background and industry context.
        Keep it concise and factual.
        """

    return call_ai_agent(prompt)

