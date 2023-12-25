import yaml
import krakenex
import numpy as np
import sys
import requests
from exception import CustomException

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import process_response


class Analysis:
    def __init__(self):
        self.get_conection()
        self.config = self.load_config()
        self.data_cache = {}

    def get_conection(self):
        # Initialize API
        self.connection = krakenex.API()

    def load_config(self, config_path="config.yml"):
        with open(config_path, "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config

    def get_data(self, pair="BTCUSD", interval=1440, **kwargs):
        """
        This function allows us to calculate the stochastic Oscillator.
        The second argument refers to the time interval for the data
        in seconds; for example, to display daily data we need
        indicates how many seconds there are in a day.
        """

        try:
            data = self.data_cache.get(pair, {}).get("raw", "NO_DATA")

            if isinstance(data, str):
                # Extract the information
                params = {
                    "pair": pair,
                    "interval": interval,
                    **kwargs,
                }
                response = self.connection.query_public("OHLC", params)

                # Response error raise
                if response["error"]:
                    raise response["error"][0]

                # Process response
                data = process_response(response)

                # Save cache data
                self.data_cache[pair] = {"raw": data}

            return data

        except Exception as e:
            raise CustomException(e, sys)

    def get_crypto_pairs(self):
        url = "https://api.kraken.com/0/public/AssetPairs"
        response = requests.get(url)

        try:
            pairs_data = response.json()
            pairs = pairs_data["result"].keys()
            return pairs

        except:
            return ["BTCUSD", "ETHUSD", "USDTUSD", "XRPUSD", "USDCUSD", "SOLUSD", "ADAUASD", "DOGEUSD", "TRXUSD"]

    def compute_indicators(self, pair="BTCUSD", interval=1440, **kwargs):
        """
        This function allows us to calculate the stochastic Oscillator.
        The second argument refers to the time interval for the data
        in seconds; for example, to display daily data we need
        indicates how many seconds there are in a day.
        """
        raw_data = self.data_cache.get(pair, {}).get("raw", "NO_DATA")

        if isinstance(raw_data, str):
            print(f"Warning. No existing raw data for {pair}")
            raw_data = self.get_data(kwargs, pair=pair, interval=interval)

        data = raw_data.copy()

        model_config = self.config["model"]

        try:
            # Compute stochastic oscillator
            data["MA"] = data["close"].rolling(window=model_config["window_size_ma"]).mean()
            data["period_high"] = data["high"].rolling(model_config["stochastic_window"]).max()
            data["period_low"] = data["low"].rolling(model_config["stochastic_window"]).min()
            data["pctK"] = ((data["close"] - data["period_low"]) / (data["period_high"] - data["period_low"])) * 100
            data["pctD"] = data["pctK"].rolling(model_config["stochastic_nmean"]).mean()
            data = data.dropna().reset_index(drop=True)

            # Define sell and buy signals
            data["signal"] = np.where(data["pctK"] > data["pctD"], "Buy", "Sell")

            self.data_cache[pair]["data"] = data

            return data

        except Exception as e:
            raise CustomException(e, sys)

    def graph_pair(self, data, pair, width, height):
        # Basic plot with MA
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.3])

        fig.add_trace(
            go.Scatter(x=data["date"], y=data["close"], mode="lines", name="Close", line=dict(color="black")),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(x=data["date"], y=data["MA"], mode="lines", name="MA", line=dict(color="green")), row=1, col=1
        )

        fig.add_trace(go.Bar(x=data["date"], y=data["volume"], name="Volume", marker_color="#FF8300"), row=2, col=1)

        fig.update_yaxes(title_text="Close price", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=1)

        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)

        fig.update_layout(
            title_text=f" ☑️​ Moving average and volume:​ {pair}",
            showlegend=True,
            height=height,
            width=width,
            xaxis=dict(
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
                )
            ),
        )

        return fig

    def graph_indicator(self, data, pair, width, height):
        # Graph of indicator
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=data["date"], y=data["pctK"], name="%K", line=dict(color="#FF8300")),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=data["date"], y=data["pctD"], name="%D", line=dict(color="green")),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=data["date"], y=data["close"], name="Close", line=dict(color="black")),
            secondary_y=True,
        )

        fig.update_layout(title_text=f"☑️​ Stochastic Oscillator: {pair}")
        fig.update_xaxes(
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
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Indicator (%K, %D)", secondary_y=False)
        fig.update_yaxes(title_text="Close price", secondary_y=True)
        fig.update_layout(width=width, height=height)

        return fig
