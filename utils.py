import streamlit as st
import pandas as pd

from datetime import datetime, timedelta


def process_response(response):
    # Create pandas DataFrame
    asset = list(response["result"].keys())[0]
    data = pd.DataFrame(response["result"][asset])

    if data.empty:
        raise "Warning: Empty response"

    # Data columns
    data.columns = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "vwap",
        "volume",
        "count",
    ]

    # Processing columns
    ohlc_columns = ["open", "high", "low", "close", "volume"]
    data["date"] = pd.to_datetime(data["date"], unit="s")
    data[ohlc_columns] = data[ohlc_columns].apply(pd.to_numeric, errors="coerce")
    data = data[["date"] + ohlc_columns].copy()

    return data


# Select date and asset
def select_box_date(asset_data, days_plot):
    """
    This function generates the box to select a specific range of dates.
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
