# Import libraries
# Data process
import pandas as pd

# Utils
from utils import select_box_date
from analysis_class import Analysis

# Streamlit
import streamlit as st


# Define dashboard class
class CryptoAnalysisApp:
    def __init__(self):
        self.analysis = Analysis()
        model_config_dash = self.analysis.config["model"]

        self.interval = model_config_dash["interval"]
        self.days_plot_default = model_config_dash["days_plot_default"]
        self.w_plot = model_config_dash["w_plot"]
        self.h_plot = model_config_dash["h_plot"]

    def run(self):
        st.set_page_config(layout="wide")
        self.display_title()
        self.display_sidebar()

    def display_title(self):
        st.title("STOCHASTIC OSCILLATOR FOR CRYPTOCURRENCIES")
        st.subheader("🔔 This is an interactive site where you can see the behavior of all cryptocurrencies")

    def display_sidebar(self):
        try:
            st.sidebar.image("./images/Logov2.png", caption="Technological platform for financial services")

            ticker_options = self.analysis.get_crypto_pairs()
            selected_asset = st.sidebar.selectbox("Which asset do you want to see?", ticker_options)

            asset_data = self.analysis.get_data(pair=selected_asset, interval=self.interval)
            asset_data = self.analysis.compute_indicators(pair=selected_asset, interval=self.interval)

            selected_date = select_box_date(asset_data)
            filtered_data = asset_data[
                asset_data["date"].between(pd.to_datetime(selected_date[0]), pd.to_datetime(selected_date[1]))
            ]

            with st.expander("💹​ Asset information"):
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

            self.display_additional_info(filtered_data)
            self.display_graph(filtered_data, selected_asset)

        except:
            st.warning("You have chosen the wrong option", icon="⚠️")

    def display_additional_info(self, filtered_data):
        cat_buy = filtered_data["Overbought_Signal"].sum()
        cat_sell = filtered_data["Oversold_Signal"].sum()

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
            st.info("Overbought signals", icon="🚨")
            st.metric(label="Times", value=f"{cat_buy:,.0f}")

        with value4:
            st.info("Oversold signals", icon="🚨")
            st.metric(label="Times", value=f"{cat_sell:,.0f}")

    def display_graph(self, filtered_data, selected_asset):
        fig = self.analysis.graph_pair(filtered_data, selected_asset, self.w_plot, self.h_plot)
        st.plotly_chart(fig)


# Run app
if __name__ == "__main__":
    app = CryptoAnalysisApp()
    app.run()
