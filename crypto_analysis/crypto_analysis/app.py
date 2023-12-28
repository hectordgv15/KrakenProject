# Import libraries
import pandas as pd
import streamlit as st
import sys

from crypto_analysis.utils import select_box_date
from crypto_analysis.model import CryptoAnalysisModel
from crypto_analysis.exception import DashboardException


# Application deployment class
class CryptoAnalysisApp:
    def __init__(self):
        self.analysis = CryptoAnalysisModel()
        self.config = self.analysis.config

    def run(self):
        st.set_page_config(layout="wide")
        self.display_title()
        self.display_sidebar()
        self.display_additional_info()
        self.display_graph()

    def display_title(self):
        st.title(self.config["text"]["title"])
        st.subheader("🔔 " + self.config["text"]["subtitle"])

    def display_sidebar(self):
        try:
            st.sidebar.image(self.config["logo"]["path"], caption=self.config["logo"]["caption"])

            ticker_options = self.analysis.get_crypto_pairs()
            self.selected_asset = st.sidebar.selectbox(self.config["text"]["asset_selectbox"], ticker_options)

            asset_data = self.analysis.get_data(pair=self.selected_asset)
            asset_data = self.analysis.compute_indicators(pair=self.selected_asset)

            start_date, end_date = select_box_date(asset_data)
            filtered_data = asset_data[
                asset_data["date"].between(pd.to_datetime(start_date), pd.to_datetime(end_date))
            ]

            with st.expander("💹​ " + self.config["text"]["data_expander"]):
                showData = st.multiselect(
                    "Filter: ",
                    filtered_data.columns,
                    default=[
                        "date",
                        "open",
                        "high",
                        "close",
                        "volume",
                        "pctK",
                        "pctD",
                        "Overbought_Signal",
                        "Oversold_Signal",
                    ],
                )
                st.dataframe(filtered_data[showData], use_container_width=True)

            self.filtered_data = filtered_data

        except Exception as e:
            st.warning(self.config["text"]["asset_warning"], icon="⚠️")
            raise DashboardException(e, "DATA BUILD")

    def display_additional_info(self):
        try:
            cat_buy = self.filtered_data["Overbought_Signal"].sum()
            cat_sell = self.filtered_data["Oversold_Signal"].sum()

            avg_return = self.filtered_data["close"].pct_change().mean() * 100
            avg_price = self.filtered_data["close"].mean()

            value1, value2, value3, value4 = st.columns(4, gap="medium")

            with value1:
                st.info("Average return", icon="🚨")
                st.metric(label="Daily", value=f"{avg_return:,.2f}%")

            with value2:
                st.info("Average price", icon="🚨")
                st.metric(label="Daily", value=f"{avg_price:,.2f}")

            with value3:
                st.info("Overbought signals", icon="🚨")
                st.metric(label="Times", value=f"{cat_buy:,.0f}")

            with value4:
                st.info("Oversold signals", icon="🚨")
                st.metric(label="Times", value=f"{cat_sell:,.0f}")

        except Exception as e:
            raise DashboardException(e, "INDICATORS BUILD")

    def display_graph(self):
        try:
            fig = self.analysis.graph_pair(self.filtered_data, self.selected_asset)
            st.plotly_chart(fig)
        except Exception as e:
            raise DashboardException(e, "GRAPH BUILD")
