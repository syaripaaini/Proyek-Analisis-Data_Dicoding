import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style="dark")

# Load datasets
main_data = pd.read_csv("main_data.csv")  # Pastikan jalur file sesuai

# Pastikan kolom 'order_date' adalah datetime
main_data["order_date"] = pd.to_datetime(main_data["order_date"])

# Tentukan rentang tanggal berdasarkan data
min_date = main_data["order_date"].min()
max_date = main_data["order_date"].max()

# Sidebar Configuration
with st.sidebar:
    # Title and Logo
    st.title("Syaripatul Aini Dashboard")
    st.image("gcl.png")  # Jalur gambar disesuaikan

    # Date Input
    start_date, end_date = st.date_input(
        label="Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

# Filtered data berdasarkan rentang tanggal
filtered_data = main_data[
    (main_data["order_date"] >= pd.Timestamp(start_date)) & 
    (main_data["order_date"] <= pd.Timestamp(end_date))
]

# Helper function untuk menghitung metrik harian
def create_daily_metrics(df):
    daily_df = df.resample("D", on="order_date").agg(
        {"order_id": "nunique"}
    ).reset_index()
    daily_df.rename(columns={"order_id": "order_count"}, inplace=True)
    return daily_df

# Data Analysis
daily_metrics = create_daily_metrics(filtered_data)

# Visualizations
st.title("E-Commerce Dashboard")
st.subheader("Daily Order Metrics")

# Display Metrics
col1, col2 = st.columns(2)
col1.metric("Total Orders", value=int(daily_metrics["order_count"].sum()))
col2.metric(
    "Total Revenue",
    value=format_currency(daily_metrics["order_count"].sum(), "USD", locale="en_US")
)

# Daily Orders Plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    daily_metrics["order_date"],
    daily_metrics["order_count"],
    marker="o",
    color="#42A5F5",
    label="Orders",
)
ax.set_title("Daily Orders", fontsize=16)
ax.set_xlabel("Date")
ax.set_ylabel("Number of Orders")
ax.legend()
st.pyplot(fig)

# Footer
st.caption("Copyright © Syaripatul Aini 2024")
