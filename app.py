import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(page_title="OLA Ride Insights Dashboard", layout="wide")

st.title("🚕 OLA Ride Insights Dashboard")

# Load dataset
df = pd.read_csv("dataset/cleaned_ola_dataset.csv")

# Dataset preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

st.divider()

# ---------------- KPI METRICS ----------------

total_rides = df.shape[0]
total_revenue = df["Booking_Value"].sum()
avg_rating = df["Customer_Rating"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Rides", total_rides)
col2.metric("Total Revenue", round(total_revenue))
col3.metric("Avg Customer Rating", round(avg_rating,2))

st.divider()

# ---------------- FILTER ----------------

st.sidebar.header("Filters")

vehicle_filter = st.sidebar.multiselect(
    "Select Vehicle Type",
    options=df["Vehicle_Type"].unique(),
    default=df["Vehicle_Type"].unique()
)

filtered_df = df[df["Vehicle_Type"].isin(vehicle_filter)]

# ---------------- RIDE TREND ----------------

st.subheader("Ride Volume Over Time")

ride_trend = filtered_df.groupby("Date")["Booking_ID"].count().reset_index()

fig1 = px.line(
    ride_trend,
    x="Date",
    y="Booking_ID",
    title="Daily Ride Volume"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- VEHICLE TYPE RIDES ----------------

st.subheader("Ride Count by Vehicle Type")

vehicle_counts = filtered_df["Vehicle_Type"].value_counts().reset_index()
vehicle_counts.columns = ["Vehicle_Type","Rides"]

fig2 = px.bar(
    vehicle_counts,
    x="Vehicle_Type",
    y="Rides",
    color="Vehicle_Type"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- BOOKING STATUS ----------------

st.subheader("Booking Status Breakdown")

status_counts = filtered_df["Booking_Status"].value_counts().reset_index()
status_counts.columns = ["Status","Count"]

fig3 = px.pie(
    status_counts,
    names="Status",
    values="Count"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- PAYMENT METHOD ----------------

st.subheader("Revenue by Payment Method")

payment_revenue = filtered_df.groupby("Payment_Method")["Booking_Value"].sum().reset_index()

fig4 = px.bar(
    payment_revenue,
    x="Payment_Method",
    y="Booking_Value",
    color="Payment_Method"
)

st.plotly_chart(fig4, use_container_width=True)