import streamlit as st
import requests
import time

st.set_page_config(page_title="AI Trading Assistant", layout="wide")

TICKERS = ["AAPL", "GOOG", "NVDA", "AVGO"]

API_KEY = st.secrets["general"]["ALPACA_API_KEY"]
BASE_URL = "https://data.alpaca.markets/v2/stocks"

def fetch_price(ticker):
    url = f"{BASE_URL}/{ticker}/bars?timeframe=1Min&limit=1"
    headers = {"APCA-API-KEY-ID": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        bars = response.json().get("bars", [])
        if bars:
            return bars[-1]["c"]  # Closing price
    return None

st.title("📈 AI Trading Assistant")
st.markdown("This assistant monitors selected tickers and refreshes prices every few seconds using Alpaca API.")

placeholder = st.empty()

def render_prices():
    with placeholder.container():
        for ticker in TICKERS:
            price = fetch_price(ticker)
            if price:
                st.success(f"{ticker}: ${price:.2f}")
            else:
                st.error(f"Price for {ticker} not available.")

while True:
    render_prices()
    time.sleep(10)
