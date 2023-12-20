import krakenex
from pykrakenapi import KrakenAPI

import numpy as np
import pandas as pd

import streamlit as st

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots

# # Model
# stochastic_window = 14  # Compute indicator
# stochastic_nmean = 3  # Compute indicator

# window_size_ma = 26  # Compute MA

# # Initialize API
# api = krakenex.API()
# connection = KrakenAPI(api)


# # Function to extract the information
# def get_information_asset(ticker="BTCUSD", interval=1440):
#     """
#     This function allows us to calculate the stochastic Oscillator.
#     The second argument refers to the time interval for the data
#     in seconds; for example, to display daily data we need
#     indicates how many seconds there are in a day.

#     """

#     try:
#         # Extract the information
#         data = connection.get_ohlc_data(ticker, interval=interval, ascending=True)[0]
#         data = data.iloc[:, [1, 2, 3, 4, 6]].apply(pd.to_numeric, errors="coerce").reset_index()
#         data = data.rename(columns={"dtime": "date"})

#         # Compute stochastic oscillator
#         data["MA26"] = data["close"].rolling(window=window_size_ma).mean()
#         data["period_high"] = data["high"].rolling(stochastic_window).max()
#         data["period_low"] = data["low"].rolling(stochastic_window).min()
#         data["pctK"] = (data["close"] - data["period_low"]) * 100 / (data["period_high"] - data["period_low"])
#         data["pctD"] = data["pctK"].rolling(stochastic_nmean).mean()
#         data = data.dropna().reset_index(drop=True)

#         # Define sell and buy signals
#         data["signal"] = np.where(data["pctK"] > data["pctD"], "Buy", "Sell")

#         return data

#     except:
#         print("There is a problem with the function or its parameters")


# Select date and asset
def select_box_date(asset_data, days_plot):
    """
    this function generates the box to select a specific range of dates.

    """

    start_date = st.sidebar.date_input(
        "Start date",
        (datetime.today() - timedelta(days=days_plot)),
        min_value=asset_data["date"].min(),
        max_value=asset_data["date"].max(),
    )

    try:
        end_date = st.sidebar.date_input(
            "End date",
            datetime.today(),
            min_value=asset_data["date"].min(),
            max_value=asset_data["date"].max(),
        )

    # Sometimes the user make a query when the data is not available because the API have not shown the data yet.
    except:
        end_date = st.sidebar.date_input(
            "End date",
            datetime.today() - timedelta(days=1),
            min_value=asset_data["date"].min(),
            max_value=asset_data["date"].max(),
        )

    return (start_date, end_date)


# def time_series_chart(data, asset, width, height):
#     # Basic plot
#     fig_1 = px.line(
#         data,
#         x="date",
#         y=["close", "MA26"],
#         title=f" ☑️​​ {asset}",
#         color_discrete_map={"close": "black", "MA26": "green"},
#     )

#     fig_1.update_xaxes(
#         rangeslider_visible=True,
#         rangeselector=dict(
#             buttons=list(
#                 [
#                     dict(count=1, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(count=1, label="YTD", step="year", stepmode="todate"),
#                     dict(count=1, label="1y", step="year", stepmode="backward"),
#                     dict(step="all"),
#                 ]
#             )
#         ),
#     )

#     fig_1.update_yaxes(title_text="Close price")
#     fig_1.update_xaxes(title_text="Date")
#     fig_1.update_layout(width=width, height=height)

#     # Graph of indicator
#     fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
#     fig_2.add_trace(
#         go.Scatter(x=data["date"], y=data["pctK"], name="%K", line=dict(color="#FF8300")),
#         secondary_y=False,
#     )
#     fig_2.add_trace(
#         go.Scatter(x=data["date"], y=data["pctD"], name="%D", line=dict(color="green")),
#         secondary_y=False,
#     )
#     fig_2.add_trace(
#         go.Scatter(x=data["date"], y=data["close"], name="Close", line=dict(color="black")),
#         secondary_y=True,
#     )
#     fig_2.update_layout(title_text=f"☑️​ ​Stochastic Oscillator: {asset}")
#     fig_2.update_xaxes(
#         rangeslider_visible=True,
#         rangeselector=dict(
#             buttons=list(
#                 [
#                     dict(count=1, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(count=1, label="YTD", step="year", stepmode="todate"),
#                     dict(count=1, label="1y", step="year", stepmode="backward"),
#                     dict(step="all"),
#                 ]
#             )
#         ),
#     )
#     fig_2.update_xaxes(title_text="Date")
#     fig_2.update_yaxes(title_text="Indicator (%K, %D)", secondary_y=False)
#     fig_2.update_yaxes(title_text="Close price", secondary_y=True)
#     fig_2.update_layout(width=width, height=height)

#     return fig_1, fig_2
