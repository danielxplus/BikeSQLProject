import duckdb
import os

# Connect to DuckDB
con = duckdb.connect("large_db.duckdb")

# Count Total Rows
total_rows = con.execute("SELECT COUNT(*) FROM london_rentals").fetchall()
print("Total Rows:", total_rows)


##########
# Queries:
##########

# Save results in duckdb as smaller tables:
con.execute("CREATE OR REPLACE TABLE total_rows AS SELECT COUNT(*) AS total_rows FROM london_rentals")

# Find Busiest Rental Hours
con.execute("""
    CREATE OR REPLACE TABLE small_busiest_hours AS
    SELECT 
        strftime('%H', STRPTIME(start_rental_date_time, '%d/%m/%Y %H:%M')) AS rental_hour, 
        COUNT(*) AS total_rentals,
        SUM(COUNT(*)) OVER() AS overall_rental_count
    FROM london_rentals
    GROUP BY rental_hour
    ORDER BY total_rentals DESC
""")
busiest_hours = con.execute("SELECT * FROM small_busiest_hours").fetchdf()
print("Busiest Rental Hours:\n", busiest_hours)
print("===============")

# Find Most Popular Start Stations
con.execute("""
    CREATE OR REPLACE TABLE small_popular_stations AS
    SELECT 
        start_station_name, 
        COUNT(*) AS trip_count,
        RANK() OVER (ORDER BY COUNT(*) DESC) AS station_rank
    FROM london_rentals
    GROUP BY start_station_name
    ORDER BY trip_count DESC
""")
popular_stations = con.execute("SELECT * FROM small_popular_stations").fetchdf()
print("Most Popular Start Stations with Rank:\n", popular_stations)
print("===============")

# Find average trip duration per day
con.execute("""
    CREATE OR REPLACE TABLE small_avg_trip_duration AS
    SELECT 
        CASE 
            WHEN strftime('%w', STRPTIME(start_rental_date_time, '%d/%m/%Y %H:%M')) = '0' THEN 'Sunday'
            WHEN strftime('%w', STRPTIME(start_rental_date_time, '%d/%m/%Y %H:%M')) = '1' THEN 'Monday'
            WHEN strftime('%w', STRPTIME(start_rental_date_time, '%d/%m/%Y %H:%M')) = '2' THEN 'Tuesday'
            WHEN strftime('%w', STRPTIME(start_rental_date_time, '%d/%m/%Y %H:%M')) = '3' THEN 'Wednesday'
            WHEN strftime('%w', STRPTIME(start_rental_date_time, '%d/%m/%Y %H:%M')) = '4' THEN 'Thursday'
            WHEN strftime('%w', STRPTIME(start_rental_date_time, '%d/%m/%Y %H:%M')) = '5' THEN 'Friday'
            WHEN strftime('%w', STRPTIME(start_rental_date_time, '%d/%m/%Y %H:%M')) = '6' THEN 'Saturday'
        END AS rental_day_name,
        AVG(duration / 60.0) AS avg_minutes_duration
    FROM london_rentals
    GROUP BY rental_day_name
    ORDER BY avg_minutes_duration DESC
""")

avg_trip_duration_result = con.execute("SELECT * FROM small_avg_trip_duration").fetchdf()
print("Average Trip Duration Per Day:\n", avg_trip_duration_result)

# Print overall average separately
con.execute("""
    CREATE OR REPLACE TABLE small_overall_avg_duration AS
    SELECT
    AVG(duration / 60.0) AS overall_avg_duration
    FROM london_rentals""").fetchall()[0][0]

overall_avg = con.execute("SELECT * FROM small_overall_avg_duration").fetchdf()
overall_avg_value = overall_avg.iloc[0,0]
print("Overall average trip duration (minutes):", overall_avg_value)
print("===============")

# Find Most Traveled Station Pairs
con.execute("""
    CREATE OR REPLACE TABLE small_popular_station_pairs AS                      
    SELECT start_station_name, end_station_name, COUNT(*) AS trip_count
    FROM london_rentals
    WHERE start_station_name IS NOT NULL AND end_station_name IS NOT NULL
    GROUP BY start_station_name, end_station_name
    ORDER BY trip_count DESC
""")
popular_station_pairs = con.execute("SELECT * FROM small_popular_station_pairs").fetchdf()
print("Most Traveled Station Pairs:\n", popular_station_pairs)
print("===============")

# Find Most Used Bikes
con.execute("""
    CREATE OR REPLACE TABLE small_most_used_bikes AS
        SELECT 
        bike_id, 
        COUNT(*) AS usage_count
    FROM london_rentals
    GROUP BY bike_id
    ORDER BY usage_count DESC
""")
most_used_bikes = con.execute("SELECT * FROM small_most_used_bikes").fetchdf()
print("Most Used Bikes (With Total Rental Breakdown):\n", most_used_bikes)


#################
# Sample queries:
#################

# Busiest Rental Hours (Only Peak Hours 7 AM - 9 PM)
sample_busiest_hours = con.execute("""
    SELECT * FROM small_busiest_hours
    WHERE rental_hour BETWEEN '07' AND '21'
    ORDER BY total_rentals DESC
""").fetchdf()
print("\nsample from 'small_busiest_hours' (Peak Hours):\n", sample_busiest_hours)

# Most Popular Start Stations (Stations with 5000+ Rentals)
sample_popular_stations = con.execute("""
    SELECT * FROM small_popular_stations
    WHERE trip_count > 5000
    ORDER BY trip_count DESC
""").fetchdf()
print("\nsample from 'small_popular_stations' (Stations with 5000+ Rentals):\n", sample_popular_stations)

# Average Trip Duration Per Day (Only Weekends)
sample_avg_trip_duration = con.execute("""
    SELECT * FROM small_avg_trip_duration
    WHERE rental_day_name IN ('Saturday', 'Sunday')
    ORDER BY avg_minutes_duration DESC
""").fetchdf()
print("\nsample from 'small_avg_trip_duration' (Weekends Only):\n", sample_avg_trip_duration)

# Overall Average Trip Duration (Formatted)
overall_avg_df = con.execute("SELECT * FROM small_overall_avg_duration").fetchdf()
overall_avg_value = overall_avg_df.iloc[0, 0]  # Extract numeric value
print(f"\nOverall average trip duration: {overall_avg_value:.2f} minutes")

# Most Traveled Station Pairs (Only Trips Over 5000)
sample_popular_station_pairs = con.execute("""
    SELECT * FROM small_popular_station_pairs
    WHERE trip_count > 500
    ORDER BY trip_count DESC
""").fetchdf()
print("\nsample from 'small_popular_station_pairs' (Trips Over 500):\n", sample_popular_station_pairs)

# Most Used Bikes (Bikes Used More Than 1000 Times)
sample_most_used_bikes = con.execute("""
    SELECT * FROM small_most_used_bikes
    WHERE usage_count > 100
    ORDER BY usage_count DESC
""").fetchdf()
print("\nsample from 'small_most_used_bikes' (Used More Than 100 Times):\n", sample_most_used_bikes)