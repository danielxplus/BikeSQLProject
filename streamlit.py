# run using the command `python -m streamlit run app.py`

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import plotly.express as px

# Connect to SQLite Database
DB_FILE = "db_file.sqlite"
TABLE_NAME = "small_busiest_hours"  # Change table name as needed

@st.cache_data
def load_data(table_name):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# Sidebar
st.sidebar.title("Dashboard Settings")
selected_table = st.sidebar.selectbox("Select Table", [
    "small_busiest_hours",
    "small_popular_stations",
    "small_avg_trip_duration",
    "small_popular_station_pairs",
    "small_most_used_bikes"
])

data = load_data(selected_table)

# Title
st.title("🚲 Bike Rentals Dashboard")
st.write("### Visualizing Data from SQLite")

# Show Dataset
st.write("### Sample Data")
st.dataframe(data)

# Fix rental_hour type
if "rental_hour" in data.columns:
    data["rental_hour"] = pd.to_numeric(data["rental_hour"], errors='coerce').fillna(0).astype(int)

# Visualization 1: Bar Chart of Rentals by Hour with User Selection
if "rental_hour" in data.columns:
    st.write("### 🚴 Busiest Rental Hours")
    hour_range = st.slider("Select Hour Range", int(data["rental_hour"].min()), int(data["rental_hour"].max()), (int(data["rental_hour"].min()), int(data["rental_hour"].max())))
    filtered_data = data[(data["rental_hour"] >= hour_range[0]) & (data["rental_hour"] <= hour_range[1])]
    
    fig, ax = plt.subplots()
    ax.bar(filtered_data["rental_hour"], filtered_data["total_rentals"], color="blue")
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

# Visualization 2: Most Popular Stations as Interactive Pie Chart
if "start_station_name" in data.columns:
    st.write("### 📍 Most Popular Stations")
    top_stations = data.nlargest(10, "trip_count")
    
    # Create an interactive pie chart
    fig = px.pie(top_stations, 
                 names="start_station_name", 
                 values="trip_count", 
                 title="Top 10 Most Popular Stations",
                 color_discrete_sequence=px.colors.qualitative.Set3, hole=0.1)  # Optional: Makes it a donut chart

    st.plotly_chart(fig, use_container_width=True)

# Visualization 3: Rental Duration Distribution (Fixed)
if "avg_minutes_duration" in data.columns:
    st.write("### ⏳ Average Trip Duration Per Day")
    fig, ax = plt.subplots()
    day_order = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    data["short_day_name"] = data["rental_day_name"].map({
        "Sunday": "Sun", "Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed", 
        "Thursday": "Thu", "Friday": "Fri", "Saturday": "Sat"
    })
    data_sorted = data.sort_values("short_day_name", key=lambda x: pd.Categorical(x, categories=day_order, ordered=True))
    ax.bar(data_sorted["short_day_name"], data_sorted["avg_minutes_duration"], color="orange", edgecolor='black')
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Average Duration (Minutes)")
    ax.set_title("Average Trip Duration Per Day")
    ax.set_ylim(0, 25)  # Set Y-axis limit from 0 to 25
    st.pyplot(fig)

# Visualization 4: Most Traveled Station Pairs with Dropdowns
if "start_station_name" in data.columns and "end_station_name" in data.columns:
    st.write("### 🔄 Search Trips Between Stations")
    
    # Drop NaN values before finding unique stations
    data = data.dropna(subset=["start_station_name", "end_station_name"])
    
    unique_stations = sorted(set(data["start_station_name"].dropna().unique()).union(set(data["end_station_name"].dropna().unique())))
    
    start_station = st.selectbox("Select Start Station", unique_stations)
    end_station = st.selectbox("Select End Station", unique_stations)
    
    trip_count = data[(data["start_station_name"] == start_station) & (data["end_station_name"] == end_station)]["trip_count"].sum()
    
    st.write(f"Total Trips from **{start_station}** to **{end_station}**: {trip_count}")


# Visualization 5: Trips Per Bike ID
if "bike_id" in data.columns:
    st.write("### 🚲 Search Trips by Bike ID")
    
    # Ensure bike_id is treated as a string for dropdown selection
    data["bike_id"] = data["bike_id"].astype(str)
    
    # Create a dropdown to select a bike ID
    selected_bike = st.selectbox("Select Bike ID", data["bike_id"].unique())
    
    # Filter data for the selected bike
    bike_trips = data[data["bike_id"] == selected_bike]["usage_count"].sum()
    
    # Display the total trips for the selected bike
    st.write(f"Total Trips for **Bike ID {selected_bike}**: {bike_trips}")

st.write("### 📊 Summary")
st.write(f"Total Records in `{selected_table}`: {len(data)}")