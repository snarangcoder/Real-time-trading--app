import streamlit as st
import req	uests
import time

st.set_page_config(page_title="AI Trading Assistant", layout="wide")

# Core watchlist of tickers
TICKERS = ["AAPL", "GOOG", "NVDA", "AVGO"]

# Safely load API key
API_KEY = st.secrets["general"]["ALPACA_API_KEY"]
BASE_URL = "https://data.alpaca.markets/v2/stocks"

# Fetch real-time price using a free endpoint
def fetch_price(ticker):
    url = f"{BASE_URL}/{ticker}/bars?timeframe=1Min&limit=1"
    headers = {"APCA-API-KEY-ID": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        bars = response.json().get("bars", [])
        if bars:
            return bars[-1]["c"]  # Close price
    return None

st.title("📈 AI Trading Assistant")
st.markdown("This assistant monitors selected tickers and refreshes prices every few seconds using Alpaca API.")

# Display prices with auto-refresh
placeholder = st.empty()

def render_prices():
    with placeholder.container():
        for ticker in TICKERS:
            price = fetch_price(ticker)
            if price:
                st.success(f"{ticker} → ${price}")
            else:
                st.warning(f"Price for {ticker} not available.")

render_prices()

# Auto-refresh loop every 10 seconds
st_autorefresh = st.experimental_data_editor({"Refresh in seconds": 10})
time.sleep(st_autorefresh["Refresh in seconds"])
st.rerun()
