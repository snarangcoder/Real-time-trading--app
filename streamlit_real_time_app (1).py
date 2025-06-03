
import streamlit as st
import requests
import time

st.set_page_config(page_title="Live Trading Assistant", layout="wide")

TICKERS = ["AAPL", "GOOG", "NVDA", "AVGO"]

# Fetch API key safely from Streamlit secrets
API_KEY = st.secrets["general"]["ALPACA_API_KEY"]

BASE_URL = "https://data.alpaca.markets/v2/stocks"

def fetch_price(ticker):
    url = f"{BASE_URL}/{ticker}/quotes/latest"
    headers = {"APCA-API-KEY-ID": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("quote", {}).get("ap", None)
    return None

st.title("📈 AI Trading Assistant")
st.markdown("This assistant shows real-time price updates using Alpaca API.")

for ticker in TICKERS:
    price = fetch_price(ticker)
    if price:
        st.metric(label=f"{ticker} Price", value=f"${price:.2f}")
    else:
        st.warning(f"Price for {ticker} not available.")
