# Streamlit App Entry Point
import streamlit as st

st.title('🛒 Real-Time E-commerce Demand Forecaster')

st.write('This is a placeholder for your Streamlit app.')

# app.py

import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objs as go

st.set_page_config(page_title="E-commerce Demand Forecaster", layout="wide")

st.title("📈 Real-Time E-commerce Demand Forecaster")

@st.cache_data
def load_data():
    df = pd.read_csv('data/ecommerce_sales_data.csv', parse_dates=['Date'])
    return df

df = load_data()

# Sidebar controls
st.sidebar.header("Select Forecast Parameters")

categories = df['Product_Category'].unique()
regions = df['Region'].unique()

selected_category = st.sidebar.selectbox("Product Category", categories)
selected_region = st.sidebar.selectbox("Region", regions)
forecast_days = st.sidebar.radio("Forecast Days", [7, 15, 30])


# Filter data
filtered_df = df[(df['Product_Category'] == selected_category) & (df['Region'] == selected_region)]
filtered_df = filtered_df.groupby('Date')['Units_Sold'].sum().reset_index()
filtered_df.rename(columns={'Date': 'ds', 'Units_Sold': 'y'}, inplace=True)

if len(filtered_df) < 2:
    st.error("Not enough data to forecast. Try another category or region.")
else:
    # Train model
    model = Prophet()
    model.fit(filtered_df)

    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)

    # Plot
    st.subheader("📊 Forecast Plot")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['ds'], y=filtered_df['y'], name='Historical'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast', line=dict(dash='dash')))
    st.plotly_chart(fig, use_container_width=True)

    # Download
    forecast_out = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_days)
    forecast_out.rename(columns={
        'ds': 'Date',
        'yhat': 'Forecast',
        'yhat_lower': 'Lower Bound',
        'yhat_upper': 'Upper Bound'
    }, inplace=True)

    st.subheader("📥 Download Forecast")
    st.dataframe(forecast_out)
    csv = forecast_out.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="forecast.csv", mime="text/csv")

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '../data/ecommerce_sales_data.csv')
df = pd.read_csv(DATA_PATH)

