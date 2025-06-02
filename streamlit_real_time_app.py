
import streamlit as st
import requests
import time

st.set_page_config(page_title="Live Trading Assistant", layout="wide")

TICKERS = ["AAPL", "GOOG", "NVDA", "AVGO"]
API_KEY = st.secrets["ALPACA_API_KEY"]
BASE_URL = "https://data.alpaca.markets/v2/stocks"

def fetch_price(ticker):
    url = f"{BASE_URL}/{ticker}/quotes/latest"
    headers = {"APCA-API-KEY-ID": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("quote", {}).get("ap", None)
    return None

if "prices" not in st.session_state:
    st.session_state.prices = {}

st.title("📈 Real-Time Trading Assistant")

placeholder = st.empty()
while True:
    with placeholder.container():
        st.markdown("### 🔁 Live Price Updates (refreshes every 5 sec)")
        for ticker in TICKERS:
            new_price = fetch_price(ticker)
            old_price = st.session_state.prices.get(ticker)

            if new_price:
                change = ""
                if old_price:
                    if new_price > old_price:
                        change = "🟢"
                    elif new_price < old_price:
                        change = "🔴"
                    else:
                        change = "➖"

                st.markdown(f"**{ticker}: ${new_price:.2f} {change}**", unsafe_allow_html=True)
                st.session_state.prices[ticker] = new_price
            else:
                st.markdown(f"**{ticker}: Unable to fetch price**")
    time.sleep(5)
