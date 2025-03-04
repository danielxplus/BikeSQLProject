import duckdb

duckdb.sql("INSTALL sqlite; LOAD sqlite;")

# Connect to DuckDB
duckdb_conn = duckdb.connect("large_db.duckdb")

# Enable SQLite extension
duckdb_conn.execute("INSTALL sqlite; LOAD sqlite;")

# Connect DuckDB to SQLite
duckdb_conn.execute("ATTACH 'db_file.sqlite' AS sqlite_db (TYPE sqlite);")

# List of tables to export
tables = [
    "small_busiest_hours",
    "small_popular_stations",
    "small_avg_trip_duration",
    "small_overall_avg_duration", 
    "small_popular_station_pairs",
    "small_most_used_bikes"
]

# Loop through and export each table
for table_name in tables:
    print(f"Exporting {table_name} to SQLite...")

    # Export table from DuckDB to SQLite
    duckdb_conn.execute(f"CREATE TABLE sqlite_db.{table_name} AS SELECT * FROM {table_name};")

# Close the connection
duckdb_conn.close()

print("All tables successfully exported to SQLite")