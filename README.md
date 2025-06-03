# 🛒 Real-Time E-commerce Demand Forecaster

A powerful, interactive forecasting dashboard built with **Streamlit**, designed to help e-commerce businesses make informed inventory and marketing decisions using historical sales data and live Google Trends.

---

## 🚀 Features

- 📊 **Recent Sales Analysis**: Visualize unit sales trends for the past 7/14/30 days.
- 📈 **Demand Forecasting**: Predict future demand using Facebook’s Prophet model.
- 🌎 **Filter by Region & Product Category**: Zoom into specific segments.
- 🔎 **Google Trends Integration**: Understand public interest for specific product keywords.
- 📅 **Downloadable Reports**: Export forecast results as CSV and PDF.
- ⚠️ **Stock Refill Alerts**: Get warnings when predicted demand exceeds stock threshold.

---

## 📁 Project Structure

```
real_time_ecommerce_demand_forecaster/
│
├── app/                     # Streamlit app source code
│   └── app.py               # Main Streamlit application
│
├── data/                    # Folder to store sample or uploaded datasets
│
├── notebooks/               # Jupyter notebooks for data exploration (optional)
│
├── outputs/                 # Forecast outputs (CSV, PDF reports)
│
├── .gitignore               # Files/folders to ignore in git
├── requirements.txt         # Project dependencies
├── README.md                # Project description and usage guide
```

---

## 💽 Demo

> _Coming soon_ – live deployment on **Streamlit Cloud** / **Hugging Face Spaces**

---

## 📦 Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/Hrithikdeep/real-time-ecommerce-demand-forecaster.git
cd real-time-ecommerce-demand-forecaster
```

### 2. Install Dependencies

Create a virtual environment (optional but recommended), then:

```bash
pip install -r requirements.txt
```

### 3. Launch the App

```bash
streamlit run app/app.py
```

---

## 📊 How It Works

### 🔹 Upload Data

Upload a `.csv` file containing historical sales with the following columns:

- `Date`: Date of transaction (YYYY-MM-DD)
- `Region`: Region or city of sale
- `Product_Category`: Category of product
- `Units_Sold`: Number of units sold

### 🔹 Choose Objective

- **Recent Sales**: See how units sold changed over time
- **Forecasting**: Predict demand for the next 7, 14, or 30 days

### 🔹 Google Trends

Enter any **product keyword** to see how interest has changed recently. Useful for spotting seasonality and trends.

### 🔹 Export & Alerts

- **Download Forecast**: Get results as CSV or PDF
- **Set Stock Threshold**: Get alerts when demand exceeds a threshold

---

## 📷 Screenshots

> (Add screenshots of your app UI here)

---

## 🔍 Tech Stack

- [Streamlit](https://streamlit.io/) – UI and interactivity
- [Prophet](https://facebook.github.io/prophet/) – Time series forecasting
- [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) – Visualization
- [Pytrends](https://pypi.org/project/pytrends/) – Google Trends API
- [FPDF](https://pyfpdf.github.io/fpdf2/) – PDF report generation

---

## 🧐 Use Cases

- Inventory planning & restocking
- Marketing campaign planning
- Sales trend analysis
- Keyword trend tracking

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Made with ❤️ by [Hrithik](https://github.com/Hrithikdeep)

---

## 🌐 Contributions

PRs and suggestions are welcome! Feel free to fork this repo, enhance features, and open a pull request.
 
