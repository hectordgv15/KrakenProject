# Import libraries
# Data process
import pandas as pd
import sys

# Utils
from utils import select_box_date
from analysis_class import Analysis
from exception import DashboardException

# Streamlit
import streamlit as st


# Define dashboard class
class CryptoAnalysisApp:
    def __init__(self):
        self.analysis = Analysis()
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
            raise DashboardException(e, sys)

    def display_additional_info(self):
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

    def display_graph(self):
        fig = self.analysis.graph_pair(
            self.filtered_data, self.selected_asset, self.config["visual"]["w_plot"], self.config["visual"]["h_plot"]
        )
        st.plotly_chart(fig)


# Run app
if __name__ == "__main__":
    app = CryptoAnalysisApp()
    app.run()
