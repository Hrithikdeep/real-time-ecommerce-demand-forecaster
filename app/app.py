import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from fpdf import FPDF

st.set_page_config(page_title="E-commerce Demand Forecaster", layout="wide")

st.title(" E-commerce Demand Forecaster")

# === Sidebar filters ===
st.sidebar.header("Filters & Objective")

forecast_mode = st.sidebar.radio("Choose Objective", ["Recent Sales (7/14/30 Days)", "Forecasting (7/14/30 Days)"])
forecast_period = st.sidebar.selectbox("Select Forecast Period (Days)", [7, 14, 30])

# === File upload ===
file = st.file_uploader("Upload CSV File", type=["csv"])

if file:
    df = pd.read_csv(file, parse_dates=["Date"])
    df = df.sort_values("Date")

    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    # Sidebar filters
    regions = df["Region"].unique().tolist()
    categories = df["Product_Category"].unique().tolist()

    selected_regions = st.sidebar.multiselect("Filter by Region", regions, default=regions)
    selected_categories = st.sidebar.multiselect("Filter by Category", categories, default=categories)

    df_filtered = df[df["Region"].isin(selected_regions) & df["Product_Category"].isin(selected_categories)]

    if forecast_mode == "Forecasting (7/14/30 Days)":
        st.subheader(f"📈 Forecast for Next {forecast_period} Days")

        # Aggregate daily sales
        daily_sales = df_filtered.groupby("Date")["Units_Sold"].sum().reset_index()
        daily_sales.columns = ["ds", "y"]

        if len(daily_sales) < 2:
            st.error("Not enough data to forecast.")
        else:
            model = Prophet()
            model.fit(daily_sales)

            future = model.make_future_dataframe(periods=forecast_period)
            forecast = model.predict(future)

            # Plot
            fig1 = model.plot(forecast)
            st.pyplot(fig1)

            # Show forecast table
            forecast_table = forecast[["ds", "yhat"]].tail(forecast_period)
            forecast_table.columns = ["Date", "Predicted Units Sold"]
            st.dataframe(forecast_table)

    else:
        st.subheader(f"Recent Sales (Last {forecast_period} Days)")

        recent_df = df_filtered[df_filtered["Date"] >= df_filtered["Date"].max() - pd.Timedelta(days=forecast_period)]
        summary = recent_df.groupby("Date")[["Units_Sold", "Revenue"]].sum().reset_index()

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(summary["Date"], summary["Units_Sold"], label="Units Sold")
        ax.set_title("Recent Units Sold")
        ax.legend()
        st.pyplot(fig)

else:
    st.info("Please upload a CSV file to begin.")



