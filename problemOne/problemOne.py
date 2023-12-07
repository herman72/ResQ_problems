# Import necessary packages
import sqlite3
import pandas as pd

# Establish a connection to the SQLite database
conn = sqlite3.connect('../mock_resq.db')

# Define SQL queries to fetch data from the tables
query_orders = "SELECT * FROM orders"
query_providers = "SELECT * FROM providers"
query_users = "SELECT * FROM users"

# Execute the queries and store the results in pandas DataFrames
orders = pd.read_sql_query(query_orders, conn)
providers = pd.read_sql_query(query_providers, conn)
users = pd.read_sql_query(query_users, conn)

# Merge orders and users DataFrames on user ID
orders_regDate = pd.merge(orders, users[['id', 'registeredDate']], left_on='userId', right_on='id')
orders_regDate = orders_regDate.drop('id_y', axis=1)
orders_regDate = orders_regDate.rename(columns={'id_x': 'id'})

# Convert registeredDate to datetime and extract the year
orders_regDate["registeredDate"] = pd.to_datetime(orders_regDate["registeredDate"]).dt.year

# Merge orders_regDate and providers DataFrames on provider ID
orders_regDate_offer = pd.merge(orders_regDate, providers[['id', 'defaultOfferType']], left_on='providerId', right_on='id')
orders_regDate_offer = orders_regDate_offer.drop('id_y', axis=1)
orders_regDate_offer = orders_regDate_offer.rename(columns={'id_x': 'id'})

# Convert createdAt to datetime and extract the year and month
orders_regDate_offer['createdAt'] = pd.to_datetime(orders_regDate_offer['createdAt'])
orders_regDate_offer['year_month'] = orders_regDate_offer['createdAt'].dt.to_period('M')

# Convert year_month to string
orders_regDate_offer['year_month'] = orders_regDate_offer['year_month'].astype(str)

# Establish a new connection to the SQLite database
conn = sqlite3.connect('orders_regDate_offer.db')

# Write the DataFrame to the database
orders_regDate_offer.to_sql('orders_regDate_offer', conn, if_exists='replace')

# Close the connection
conn.close()
