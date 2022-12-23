import sqlite3
import sys

# Check if a database file name was provided as a command line argument
if len(sys.argv) < 2:
    print("Usage: python print_database.py database_file")
    sys.exit()

# Open the database connection
conn = sqlite3.connect(sys.argv[1])

# Create a cursor object
cursor = conn.cursor()

# Execute a SELECT statement to retrieve all rows from all tables in the database
cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")

# Fetch all rows from the cursor
tables = cursor.fetchall()

# Iterate over the tables and print the rows for each table
for table in tables:
    print(f"Table name: {table[1]}")
    cursor.execute(f"SELECT * FROM {table[1]};")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

# Close the cursor and connection
cursor.close()
conn.close()
