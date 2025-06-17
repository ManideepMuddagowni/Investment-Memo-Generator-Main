import streamlit as st
import pandas as pd
import re
from ai_agents.main_agent import generate_investment_memo
from utils.ticker_lookup import get_stock_data, get_closest_ticker, build_ticker_dict
from utils.pdf_util import save_text_pdf
from memo_builder import get_stock_data, calculate_indicators

st.set_page_config(page_title="Investment Memo Generator", layout="wide")

# 🎨 Header
st.markdown(
    """
    <h1 style='text-align:center; color:#4B8BBE; background-color:#FFE873; padding:10px; border-radius:10px;'>
        📊 Investment Memo Generator
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#555; font-size:18px;'>"
    "Enter a company name or ticker on the left, and view the memo on the right."
    "</p>",
    unsafe_allow_html=True,
)

# Two-column layout
left_col, right_col = st.columns([1.2, 2])

# ---------- LEFT: INPUTS ----------
with left_col:
    ticker_dict = build_ticker_dict()
    user_input = st.text_input("🔎 Company Ticker or Name", value="TSLA")

    # Show tip
    st.markdown(
        "<p style='font-size:12px; color:#888;'>Tip: Enter full company name or symbol like TSLA, AAPL, etc.</p>",
        unsafe_allow_html=True
    )

    ticker = user_input.upper()
    if len(user_input) > 5 or not user_input.isalpha():
        fuzzy_ticker = get_closest_ticker(user_input, ticker_dict)
        if fuzzy_ticker:
            ticker = fuzzy_ticker
            st.success(f"Detected ticker for '{user_input}' → {ticker}")
        else:
            st.warning("Could not resolve company name to ticker, using input as ticker.")

    memo_type = st.radio(
        "🧠 Select Memo Type",
        ("Live Stock Data Memo (fetches live price)", "LLM Knowledge Memo"),
        horizontal=False
    )

    period = None
    if memo_type.startswith("Live"):
        period = st.selectbox(
            "📆 Select Period for Historical Data",
            options=["Most Recent Price", "1 Month", "6 Months"],
            index=2
        )

    generate_btn = st.button("🚀 Generate Investment Memo")

# ---------- RIGHT: OUTPUT ----------
with right_col:
    def render_structured_memo(memo_text):
        sections = re.split(r'\n(?=### )', memo_text)
        for section in sections:
            lines = section.strip().split('\n')
            if lines:
                header = lines[0]
                content = "\n".join(lines[1:]).strip()
                st.markdown(f"### {header[4:] if header.startswith('### ') else header}")
                st.markdown(content.replace('\n', '  \n'))

    if generate_btn:
        with st.spinner("⏳ Generating memo..."):
            try:
                if memo_type.startswith("Live"):
                    yf_period = {
                        "Most Recent Price": "1d",
                        "1 Month": "1mo",
                        "6 Months": "6mo"
                    }[period]

                    hist, info = get_stock_data(ticker, period=yf_period)
                    if hist.empty and yf_period == "1d":
                        hist, info = get_stock_data(ticker, period="5d")
                        hist = hist.tail(1)
                    hist = calculate_indicators(hist)
                else:
                    hist = pd.DataFrame()
                    info = {
                        "shortName": ticker,
                        "sector": "N/A",
                        "marketCap": "N/A",
                        "longBusinessSummary": (
                            "This memo is generated purely by the AI model's knowledge without live stock data."
                        )
                    }

                memo = generate_investment_memo(info, hist, ticker)
                st.success(f"✅ Memo generated for {info.get('shortName', ticker)}")

                with st.expander("📝 Investment Memo Preview", expanded=True):
                    render_structured_memo(memo)

                # Save PDF
                pdf_file = save_text_pdf(memo)

                # Download button
                with open(pdf_file, "rb") as pdf:
                    st.download_button(
                        label="📄 Download PDF",
                        data=pdf,
                        file_name=f"{ticker}_investment_memo.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"❌ Error generating memo: {e}")
    else:
        st.info("Fill out the form on the left and click **Generate Investment Memo**.")
