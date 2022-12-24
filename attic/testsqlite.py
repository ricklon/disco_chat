import sqlite3

# Connect to the database
conn = sqlite3.connect("mydatabase.db")

# Create a cursor
cursor = conn.cursor()

# Create a table
cursor.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")

# Commit the changes
conn.commit()

# Close the connection
conn.close()
