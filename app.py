import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.title("📈 Real-Time Stock Market Dashboard")

# User input
stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")

API_KEY = "demo"  # Replace with your Alpha Vantage API key

def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()

    if "Time Series (5min)" not in data:
        return None

    df = pd.DataFrame.from_dict(data["Time Series (5min)"], orient='index')
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })

    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

data = get_stock_data(stock_symbol)

if data is not None:
    st.subheader(f"Stock Data for {stock_symbol}")
    st.write(data.tail())

    fig = px.line(data, x=data.index, y="Close", title="Stock Price")
    st.plotly_chart(fig)

    st.metric("Latest Price", data["Close"].iloc[-1])
else:
    st.error("Failed to fetch data. Check symbol or API key.")
