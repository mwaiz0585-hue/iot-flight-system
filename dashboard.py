import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import time

st.set_page_config(
    page_title="Perak Flight Monitoring Dashboard",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Perak Flight Monitoring Dashboard")
st.markdown("""
This IoT-based system continuously collects aircraft telemetry data over Perak, Malaysia using the OpenSky Network API.  
The system stores timestamped records in a local database and visualises flight patterns, altitude trends, and aircraft distribution.
""")

# Connect to database
conn = sqlite3.connect("database.db")
df = pd.read_sql_query("SELECT * FROM flights", conn)
conn.close()

if df.empty:
    st.warning("No data found yet. Please let collector.py run for a while.")
else:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    # Metrics
    total_records = len(df)
    unique_aircraft = df["icao24"].nunique()
    highest_altitude = df["altitude"].max()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", total_records)
    col2.metric("Unique Aircraft", unique_aircraft)
    col3.metric("Highest Altitude", f"{highest_altitude:.2f} m" if pd.notnull(highest_altitude) else "N/A")

    st.divider()

    # Flight data table
    st.subheader("📋 Recorded Flight Data")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # Top aircraft
    st.subheader("🛫 Most Frequently Observed Aircraft")
    if "callsign" in df.columns:
        top_aircraft = df["callsign"].fillna("Unknown").value_counts().head(5).reset_index()
        top_aircraft.columns = ["Callsign", "Observations"]
        st.dataframe(top_aircraft, use_container_width=True)

    st.divider()

    # Flights per hour
    df["hour"] = df["timestamp"].dt.hour
    hourly_counts = df.groupby("hour").size().reset_index(name="Number of Flights")

    st.subheader("📊 Flights per Hour")
    fig1 = px.bar(
        hourly_counts,
        x="hour",
        y="Number of Flights",
        title="Flights Detected by Hour"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Average altitude by hour
    altitude_trend = df.groupby("hour")["altitude"].mean().reset_index()

    st.subheader("📈 Average Altitude by Hour")
    fig2 = px.line(
        altitude_trend,
        x="hour",
        y="altitude",
        title="Average Altitude by Hour",
        markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Data growth over time
    st.subheader("📈 Data Collection Growth")
    df["date"] = df["timestamp"].dt.date
    daily_counts = df.groupby("date").size().reset_index(name="Records")

    fig3 = px.line(
        daily_counts,
        x="date",
        y="Records",
        markers=True,
        title="Data Collection Over Time"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # Map
    st.subheader("🗺️ Aircraft Position Map")
    map_data = df[["latitude", "longitude"]].dropna()

    if not map_data.empty:
        st.map(map_data)
    else:
        st.info("No valid latitude/longitude data available yet.")

    st.divider()

    # Collection summary
    st.subheader("⏱️ Collection Summary")
    earliest_time = df["timestamp"].min()
    latest_time = df["timestamp"].max()

    st.write(f"**Collection Start:** {earliest_time}")
    st.write(f"**Latest Record:** {latest_time}")
    st.write("Data is continuously collected and stored for historical flight analysis over Perak.")

st.markdown("---")
st.caption("Developed by Mohammad Waizzuddin TFB2093 IoT Project | Universiti Teknologi PETRONAS")

# Auto refresh every 30 seconds
st.caption("🔄 Auto-refresh every 30 seconds")
time.sleep(30)
st.rerun()