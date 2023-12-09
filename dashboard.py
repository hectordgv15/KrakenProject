# =========================================================================================================================
# Import libraries
# Data process
import pandas as pd
import numpy as np

# Krakenex library
import krakenex
from pykrakenapi import KrakenAPI

# Dates
import time
import datetime
from datetime import datetime, timedelta

# Graphics
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots

# Utils
from utils import get_information_asset, select_box_date, time_series_chart

# Streamlit
import streamlit as st

# =========================================================================================================================
# Streamlit App initial config
st.set_page_config(layout="wide")

st.title("STOCHASTIC OSCILLATOR FOR CRYPTOCURRENCIES")
st.subheader(
    "🔔 This is an interactive site where you can see the behavior of all cryptocurrencies"
)


# Special effect
with st.spinner("Wait for it..."):
    time.sleep(1)


# =========================================================================================================================
# Parameters and load data
# Data
ticker_options = (
    "BTCUSD",
    "ETHUSD",
    "USDTUSD",
    "XRPUSD",
    "USDCUSD",
    "SOLUSD",
    "ADAUASD",
    "DOGEUSD",
    "TRXUSD",
)  # Get information
interval = 1440

# graph
days_plot_dafault = 180
w_plot = 1000
h_plot = 600

# =========================================================================================================================
# Side bar
st.sidebar.image(
    "./images/Logohg.png", caption="Technological platform for financial services"
)

selected_asset = st.sidebar.selectbox("Which asset do you want to see?", ticker_options)


# Apply
# Initial data to set date range
initial_data = get_information_asset()

selected_date = select_box_date(initial_data, days_plot_dafault)


# =========================================================================================================================
# Dataframe filtered
daily_data = get_information_asset(ticker=selected_asset, interval=interval)

filtered_data = daily_data[
    daily_data["date"].between(
        pd.to_datetime(selected_date[0]), pd.to_datetime(selected_date[1])
    )
]


with st.expander("💹​ Asset information"):
    showData = st.multiselect(
        "Filter: ",
        filtered_data.columns,
        default=["date", "open", "high", "close", "volume", "pctK", "pctD", "signal"],
    )

    st.dataframe(filtered_data[showData], use_container_width=True)


# =========================================================================================================================
# Additional information in boxes
count_cat = filtered_data["signal"].value_counts()
cat_buy = count_cat["Buy"]
cat_sell = count_cat["Sell"]

avg_return = filtered_data["close"].pct_change().mean() * 100
avg_price = filtered_data["close"].mean()

value1, value2, value3, value4 = st.columns(4, gap="medium")

with value1:
    st.info("Average return", icon="🚨")
    st.metric(label="Daily", value=f"{avg_return:,.2f}%")

with value2:
    st.info("Average price", icon="🚨")
    st.metric(label="Daily", value=f"{avg_price:,.2f}")

with value3:
    st.info("Buy signals", icon="🚨")
    st.metric(label="Times", value=f"{cat_buy:,.0f}")

with value4:
    st.info("Sell signals", icon="🚨")
    st.metric(label="Times", value=f"{cat_sell:,.0f}")


# =========================================================================================================================
# Graphs

# Apply
fig_1, fig_2 = time_series_chart(filtered_data, selected_asset, w_plot, h_plot)

st.plotly_chart(fig_1)
st.plotly_chart(fig_2)
