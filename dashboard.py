
# Import libraries
# Data process
import pandas as pd

# Utils
from utils import select_box_date
from analysis_class import Analysis

# Streamlit
import streamlit as st


if __name__=='__main__':
    # Streamlit App initial config
    st.set_page_config(layout="wide")

    st.title("STOCHASTIC OSCILLATOR FOR CRYPTOCURRENCIES")
    st.subheader("🔔 This is an interactive site where you can see the behavior of all cryptocurrencies")



    # Parameters and load data
    # Data
    # Apply
    analysis = Analysis()

    ticker_options = analysis.get_crypto_pairs()

    interval = 1440

    # graph
    days_plot_dafault = 365
    w_plot = 1000
    h_plot = 600


    # Side bar
    st.sidebar.image("./images/Logov2.png", caption="Technological platform for financial services")

    selected_asset = st.sidebar.selectbox("Which asset do you want to see?", ticker_options)
    

    # Dataframe filtered
    asset_data = analysis.get_data(pair=selected_asset, interval=interval)
    asset_data = analysis.compute_indicators(pair=selected_asset, interval=interval)

    selected_date = select_box_date(asset_data, days_plot_dafault)

    filtered_data = asset_data[
        asset_data["date"].between(pd.to_datetime(selected_date[0]), pd.to_datetime(selected_date[1]))
    ]


    with st.expander("💹​ Asset information"):
        showData = st.multiselect(
            "Filter: ",
            filtered_data.columns,
            default=["date", "open", "high", "close", "volume", "pctK", "pctD", "Overbought_Signal", "Oversold_Signal"],
        )

        st.dataframe(filtered_data[showData], use_container_width=True)



    # Additional information in boxes
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



    # Graphs
    fig = analysis.graph_pair(filtered_data, selected_asset, w_plot, h_plot)

    st.plotly_chart(fig)
    
