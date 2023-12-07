# Import necessary packages
import sqlite3
import pandas as pd

# Establish a connection to the SQLite database
conn = sqlite3.connect('../mock_resq.db')

# Create a cursor object
cursor = conn.cursor()

# SQL query to create a view named 'presentation_table'
createViewQuery = """
CREATE VIEW presentation_table AS
SELECT orders.*, strftime('%Y-%m', createdAt) AS month, strftime('%Y', users.registeredDate) AS registeredYear, providers.defaultOfferType 
FROM orders 
INNER JOIN users ON orders.userId = users.id 
INNER JOIN providers ON orders.providerId = providers.id; 
"""

# Execute the SQL query
cursor.executescript(createViewQuery)

# Fetch all the results
results = cursor.fetchall()

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

# Re-establish the connection to the SQLite database
conn = sqlite3.connect('../mock_resq.db')

# Create a cursor object
cursor = conn.cursor()

# SQL query to select all records from 'presentation_table'
query_presentation_table = "SELECT * FROM presentation_table"

# Execute the SQL query and store the result in a pandas DataFrame
presentation_table = pd.read_sql_query(query_presentation_table, conn)

# Display the first 5 records of the DataFrame
presentation_table.head()
