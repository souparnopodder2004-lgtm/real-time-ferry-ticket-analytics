import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Real-Time Ferry Analytics",
    page_icon="⛴️",
    layout="wide"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/ferry_featured.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

df = load_data()

# ---------------------------------
# SIDEBAR
# ---------------------------------
st.sidebar.title("Dashboard Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Timestamp"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Timestamp"].max().date()
)

filtered_df = df[
    (df["Timestamp"].dt.date >= start_date) &
    (df["Timestamp"].dt.date <= end_date)
].copy()

# ---------------------------------
# HEADER
# ---------------------------------
st.title("⛴️ Real-Time Ferry Ticket Sales & Redemption Analytics")

st.markdown("""
### Toronto Island Park

This dashboard provides insights into:

- Ticket Sales
- Ticket Redemption
- Passenger Movement
- Peak Demand Hours
- Seasonal Trends
- Operational KPIs
""")

st.divider()

# ---------------------------------
# KPI CALCULATIONS
# ---------------------------------
total_sales = int(filtered_df["Sales Count"].sum())
total_redemption = int(filtered_df["Redemption Count"].sum())
net_passenger = total_sales - total_redemption

avg_sales = filtered_df["Sales Count"].mean()
avg_redemption = filtered_df["Redemption Count"].mean()

peak_hour = (
    filtered_df.groupby("Hour")["Sales Count"]
    .sum()
    .idxmax()
)

off_peak_hour = (
    filtered_df.groupby("Hour")["Sales Count"]
    .sum()
    .idxmin()
)

# ---------------------------------
# KPI CARDS
# ---------------------------------
c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("🎟️ Tickets Sold", f"{total_sales:,}")
c2.metric("✅ Redeemed", f"{total_redemption:,}")
c3.metric("🚶 Net Movement", f"{net_passenger:,}")
c4.metric("📈 Avg Sales", f"{avg_sales:.2f}")
c5.metric("📉 Avg Redemption", f"{avg_redemption:.2f}")
c6.metric("🔥 Peak Hour", f"{peak_hour}:00")

st.divider()

# ---------------------------------
# SALES TREND
# ---------------------------------
st.subheader("📈 Ticket Sales Trend")

fig = px.line(
    filtered_df,
    x="Timestamp",
    y="Sales Count",
    title="Ticket Sales Over Time"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# REDEMPTION TREND
# ---------------------------------
st.subheader("📉 Ticket Redemption Trend")

fig = px.line(
    filtered_df,
    x="Timestamp",
    y="Redemption Count",
    title="Ticket Redemption Over Time",
    color_discrete_sequence=["green"]
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# NET PASSENGER MOVEMENT
# ---------------------------------
filtered_df["Net Passenger Movement"] = (
    filtered_df["Sales Count"] -
    filtered_df["Redemption Count"]
)

st.subheader("🚢 Net Passenger Movement")

fig = px.line(
    filtered_df,
    x="Timestamp",
    y="Net Passenger Movement",
    title="Passenger Movement"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# HOURLY SALES
# ---------------------------------
hourly = (
    filtered_df.groupby("Hour")["Sales Count"]
    .mean()
    .reset_index()
)

st.subheader("🕒 Average Hourly Sales")

fig = px.bar(
    hourly,
    x="Hour",
    y="Sales Count",
    title="Average Sales by Hour",
    color="Sales Count"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# MONTHLY SALES
# ---------------------------------
monthly = (
    filtered_df.groupby("Month Name")["Sales Count"]
    .sum()
    .reset_index()
)

st.subheader("📅 Monthly Ticket Sales")

fig = px.bar(
    monthly,
    x="Month Name",
    y="Sales Count",
    color="Sales Count"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# MONTHLY REDEMPTION
# ---------------------------------
monthly_red = (
    filtered_df.groupby("Month Name")["Redemption Count"]
    .sum()
    .reset_index()
)

st.subheader("📅 Monthly Ticket Redemption")

fig = px.bar(
    monthly_red,
    x="Month Name",
    y="Redemption Count",
    color="Redemption Count"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# WEEKEND VS WEEKDAY
# ---------------------------------
week = (
    filtered_df.groupby("Weekend")["Sales Count"]
    .mean()
    .reset_index()
)

st.subheader("🏖️ Weekend vs Weekday")

fig = px.bar(
    week,
    x="Weekend",
    y="Sales Count",
    color="Sales Count"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# SEASONAL ANALYSIS
# ---------------------------------
season = (
    filtered_df.groupby("Season")["Sales Count"]
    .sum()
    .reset_index()
)

st.subheader("🌤️ Seasonal Demand")

fig = px.pie(
    season,
    values="Sales Count",
    names="Season"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# ROLLING AVERAGE
# ---------------------------------
filtered_df["Rolling Sales"] = (
    filtered_df["Sales Count"]
    .rolling(4)
    .mean()
)

st.subheader("📊 1-Hour Rolling Average")

fig = px.line(
    filtered_df,
    x="Timestamp",
    y="Rolling Sales"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# PEAK HOURS TABLE
# ---------------------------------
st.subheader("🔥 Top 10 Peak Demand Hours")

peak = (
    filtered_df.groupby("Hour")["Sales Count"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(peak)

# ---------------------------------
# DATA PREVIEW
# ---------------------------------
st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df.head(20))

# ---------------------------------
# DOWNLOAD BUTTON
# ---------------------------------
st.download_button(
    label="⬇ Download Filtered Dataset",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_ferry_data.csv",
    mime="text/csv"
)

# ---------------------------------
# FOOTER
# ---------------------------------
st.markdown("---")

st.markdown(
    """
**Developed by:** Souparno Podder

**Project:** Real-Time Ferry Ticket Sales & Redemption Analytics

**Tools Used:** Python • Pandas • Plotly • Streamlit
"""
)