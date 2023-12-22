import yaml
import krakenex
from pykrakenapi import KrakenAPI

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots

from exception import CustomException
import sys


class Analysis:
    def __init__(self):
        self.get_conection()
        self.config = self.load_config()
        self.data_cache = {}

    def get_conection(self):
        # Initialize API
        api = krakenex.API()
        self.connection = KrakenAPI(api)

    def load_config(self, config_path="config.yml"):
        with open(config_path, "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config

    def get_data(self, asset="BTC-USD", interval=1440):
        """
        This function allows us to calculate the stochastic Oscillator.
        The second argument refers to the time interval for the data
        in seconds; for example, to display daily data we need
        indicates how many seconds there are in a day.
        """

        try:
            data = self.data_cache.get(asset, {}).get("raw", "NO DATA")

            if data == "NO DATA":
                # Extract the information
                data = self.connection.get_ohlc_data(asset, interval=interval, ascending=True)[0]
                data = data.iloc[:, [1, 2, 3, 4, 6]].apply(pd.to_numeric, errors="coerce").reset_index()
                data = data.rename(columns={"dtime": "date"})
                self.data_cache[asset] = {"raw": data}

            return data
            
        except Exception as e:
            raise CustomException(e, sys)


    def compute_indicators(self, asset="BTCUSD", interval=1440):
        """
        This function allows us to calculate the stochastic Oscillator.
        The second argument refers to the time interval for the data
        in seconds; for example, to display daily data we need
        indicates how many seconds there are in a day.
        """
        raw_data = self.data_cache.get(asset, {}).get("raw", "NO DATA")

        # if raw_data == "NO DATA":
        #     print(f"Warning. No existing raw data for {asset}")
        #     raw_data = self.get_data(asset=asset, interval=interval)

        data = raw_data.copy()

        model_config = self.config["model"]

        try:
            # Compute stochastic oscillator
            data["MA26"] = data["close"].rolling(window=model_config["window_size_ma"]).mean()
            data["period_high"] = data["high"].rolling(model_config["stochastic_window"]).max()
            data["period_low"] = data["low"].rolling(model_config["stochastic_window"]).min()
            data["pctK"] = ((data["close"] - data["period_low"]) / (data["period_high"] - data["period_low"])) * 100
            data["pctD"] = data["pctK"].rolling(model_config["stochastic_nmean"]).mean()
            data = data.dropna().reset_index(drop=True)

            # Define sell and buy signals
            data["signal"] = np.where(data["pctK"] > data["pctD"], "Buy", "Sell")

            self.data_cache[asset]["data"] = data

            return data
        
        except Exception as e:
            raise CustomException(e, sys)


    def graph_asset(self, data, asset, width, height):
        # Basic plot
        fig_1 = px.line(
            data,
            x="date",
            y=["close", "MA26"],
            title=f" ☑️​​ {asset}",
            color_discrete_map={"close": "black", "MA26": "green"},
        )

        fig_1.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
        )

        fig_1.update_yaxes(title_text="Close price")
        fig_1.update_xaxes(title_text="Date")
        fig_1.update_layout(width=width, height=height)
        
        

        return fig_1

    def graph_indicator(self, data, asset, width, height):
        # Graph of indicator
        fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig_2.add_trace(
            go.Scatter(x=data["date"], y=data["pctK"], name="%K", line=dict(color="#FF8300")),
            secondary_y=False,
        )
        fig_2.add_trace(
            go.Scatter(x=data["date"], y=data["pctD"], name="%D", line=dict(color="green")),
            secondary_y=False,
        )
        fig_2.add_trace(
            go.Scatter(x=data["date"], y=data["close"], name="Close", line=dict(color="black")),
            secondary_y=True,
        )
        fig_2.update_layout(title_text=f"☑️​ Stochastic Oscillator: {asset}")
        fig_2.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
        )
        fig_2.update_xaxes(title_text="Date")
        fig_2.update_yaxes(title_text="Indicator (%K, %D)", secondary_y=False)
        fig_2.update_yaxes(title_text="Close price", secondary_y=True)
        fig_2.update_layout(width=width, height=height)

        return fig_2
