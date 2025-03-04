import duckdb

# Define file paths
csv_file_path = "london.csv"
db_file_path = "large_db.duckdb"

# Connect to DuckDB and create a new database file
con = duckdb.connect(db_file_path)

# Load CSV into DuckDB (ensuring it gets stored)
con.execute(f"CREATE TABLE london_rentals AS SELECT * FROM read_csv_auto('{csv_file_path}')")

# Verify table is now saved
tables = con.execute("SHOW TABLES").fetchall()
print("Tables in DuckDB:", tables)

# Close connection
con.close()