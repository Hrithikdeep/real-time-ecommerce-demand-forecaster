import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from io import BytesIO
from fpdf import FPDF


# Page setup
st.set_page_config(page_title="E-commerce Demand Forecaster", layout="wide")

st.title(" Real-Time E-commerce Demand Forecaster")
st.markdown("Upload your dataset, apply filters, and choose an objective to get started.")

# File upload
file = st.file_uploader(" Upload your sales CSV", type=["csv"])

# Sidebar filters and settings
st.sidebar.header(" Filters & Objective")
analysis_type = st.sidebar.radio(" Choose Objective", [" Recent Sales (7/14/30 Days)", " Forecasting (7/14/30 Days)"])
forecast_period = st.sidebar.selectbox(" Select Forecast Period (Days)", [7, 14, 30])

if file:
    df = pd.read_csv(file)

    # Preprocess
    try:
        df['Date'] = pd.to_datetime(df['Date'])
    except:
        st.error(" Date column parsing failed. Ensure 'Date' column is in YYYY-MM-DD format.")
        st.stop()

    # Data preview
    st.subheader(" Preview of Uploaded Data")
    st.dataframe(df.head())

    # Sidebar Filters
    st.sidebar.subheader(" Data Filters")
    all_regions = df['Region'].dropna().unique().tolist()
    all_categories = df['Product_Category'].dropna().unique().tolist()

    selected_regions = st.sidebar.multiselect(" Filter by Region", all_regions, default=all_regions)
    selected_categories = st.sidebar.multiselect(" Filter by Category", all_categories, default=all_categories)

    # Apply filters
    filtered_df = df[(df['Region'].isin(selected_regions)) & (df['Product_Category'].isin(selected_categories))]

    if filtered_df.empty:
        st.warning(" No data available for selected filters.")
        st.stop()

    # View 1: Recent Trends
    if analysis_type == "Recent Sales (7/14/30 Days)":
        st.subheader(f" Units Sold in the Last {forecast_period} Days")
        latest = filtered_df['Date'].max()
        start = latest - pd.Timedelta(days=forecast_period)
        recent = filtered_df[filtered_df['Date'] >= start]

        daily = recent.groupby('Date')['Units_Sold'].sum().reset_index()

        fig, ax = plt.subplots()
        sns.lineplot(data=daily, x='Date', y='Units_Sold', ax=ax, marker="o")
        ax.set_title(f" Units Sold (Filtered by Region & Category) - Last {forecast_period} Days")
        ax.set_ylabel("Units Sold")
        ax.set_xlabel("Date")
        st.pyplot(fig)

        st.markdown(" **Explanation:** This line graph shows the trend in units sold over the selected period. Peaks indicate days of high demand which could relate to promotions, weekends, or seasonal events.**")

    # View 2: Forecasting
    else:
        st.subheader(f" Forecast for Next {forecast_period} Days")

        grouped = filtered_df.groupby('Date')['Units_Sold'].sum().reset_index()
        grouped.columns = ['ds', 'y']

        if len(grouped) < 2:
            st.error(" Not enough data for forecasting.")
        else:
            m = Prophet()
            m.fit(grouped)

            future = m.make_future_dataframe(periods=forecast_period)
            forecast = m.predict(future)

            st.write("Forecast Plot:")
            fig1 = m.plot(forecast)
            st.pyplot(fig1)

            st.markdown("**Explanation:** The graph shows predicted sales with confidence intervals. This helps plan inventory, campaigns, and logistics. Look for rising trends (increased demand) or drops (less interest).**")

            forecast_result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_period)
            st.write("Forecast Table:")
            st.dataframe(forecast_result)

            # Stock Refill Alert
            stock_threshold = st.number_input(" Set Stock Refill Threshold", value=500, min_value=0)
            alerts = forecast_result[forecast_result['yhat'] > stock_threshold]

            if not alerts.empty:
                st.warning(" **Stock Refill Alert:** These dates may exceed your stock threshold!")
                st.dataframe(alerts[['ds', 'yhat']])
            else:
                st.success(" No stock refill alerts for the selected forecast period.")

            # CSV Download
            csv = forecast_result.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=" Download Forecast CSV",
                data=csv,
                file_name='forecast_result.csv',
                mime='text/csv'
            )

            # PDF Report
            from fpdf import FPDF

def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="📦 E-commerce Demand Forecast Report", ln=1, align='C')

    for index, row in df.iterrows():
        line = f"{row['ds'].date()} - Predicted: {row['yhat']:.2f}"
        pdf.cell(200, 10, txt=line, ln=1)

    # Export PDF as bytes
    pdf_bytes = pdf.output(dest='S').encode('latin-1')  # Safe encoding
    return pdf_bytes



