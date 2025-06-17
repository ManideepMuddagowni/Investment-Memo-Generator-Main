from .base import call_ai_agent

def generate_risks_opportunities(financial_summary, technical_summary, sentiment_summary):
    prompt = f"""
    Given these summaries:

    Company Info Summary:
    {financial_summary}

    Technical Analysis Summary:
    {technical_summary}

    News Sentiment Summary:
    {sentiment_summary}

    Identify key investment risks and opportunities.
    Risks:
    Opportunities:
    """
    return call_ai_agent(prompt)
