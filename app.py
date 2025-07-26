import streamlit as st
import pandas as pd
import requests
import datetime

st.set_page_config(layout="wide")
st.title("AI Analis Crypto - TROVANA")

coins = ['bitcoin', 'ethereum', 'dogecoin', 'solana', 'cardano']
selected = st.selectbox("Pilih Koin", coins)

days = st.selectbox("Timeframe", ['1', '7', '30'])
vs = 'usd'

url = f"https://api.coingecko.com/api/v3/coins/{selected}/market_chart?vs_currency={vs}&days={days}"
data = requests.get(url).json()

prices = pd.DataFrame(data['prices'], columns=["timestamp", "price"])
prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit='ms')
prices.set_index("timestamp", inplace=True)

sma_fast = prices["price"].rolling(5).mean()
sma_slow = prices["price"].rolling(20).mean()

st.line_chart(prices["price"], height=300)
st.line_chart(pd.DataFrame({"SMA 5": sma_fast, "SMA 20": sma_slow}), height=300)

latest = prices["price"].iloc[-1]
sma5 = sma_fast.iloc[-1]
sma20 = sma_slow.iloc[-1]

signal = ""
if sma5 > sma20:
    signal = "📈 LONG (Bullish)"
elif sma5 < sma20:
    signal = "📉 SHORT (Bearish)"
else:
    signal = "⏸️ Wait / Sideways"

st.markdown(f"### 💡 Sinyal AI: {signal}")
st.markdown(f"- Harga sekarang: **${latest:.2f}**")
