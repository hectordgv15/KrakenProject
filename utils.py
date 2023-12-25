import streamlit as st

from datetime import datetime, timedelta


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
