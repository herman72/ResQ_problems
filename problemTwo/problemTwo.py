# Import packages

import sqlite3
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# connect to database 
conn = sqlite3.connect('../mock_resq.db')
cursor = conn.cursor()

# Execute SQL query to fetch unique years from the createdAt column
cursor.execute("SELECT DISTINCT strftime('%Y', CreatedAt) AS Year FROM orders")

# Fetch the results
unique_years = cursor.fetchall()



def get_holidays(year):
    """
    Retrieves holiday dates for a given year using date.nager.at API.

    Args:
        year (str): A year as a string (e.g., '2022').

    Returns:
        list: A list of holiday dates for the given year.
    """
    try:
        response = requests.get(f'https://date.nager.at/api/v3/publicholidays/{year}/fi')
        response.raise_for_status()  # Raise an error for non-200 status codes
        holidays_data = response.json()
        return [holiday['date'] for holiday in holidays_data]
    except requests.RequestException as e:
        print(f"Error fetching holidays for {year}: {e}")
        return []


def create_holiday_date(unique_years):
    """
    Creates a DataFrame containing holiday dates for each year in the input list.

    Args:
        unique_years (list): A list of unique years for which to get holiday dates.

    Returns:
        DataFrame: A DataFrame containing all holiday dates for the given years.
    """
    all_holiday_dates = pd.DataFrame()

    for year in unique_years:
        holiday_dates = get_holidays(str(year[0]))
        year_holiday_dates = pd.DataFrame({'holyDate': holiday_dates})
        all_holiday_dates = pd.concat([all_holiday_dates, year_holiday_dates], ignore_index=True)

    all_holiday_dates['holyDate'] = pd.to_datetime(all_holiday_dates['holyDate'])
    all_holiday_dates.to_csv("all_holiday_dates.csv", index=False)
    return all_holiday_dates

# Create DataFrame with holiday dates for all years
all_holiday_dates = create_holiday_date(unique_years)
all_holiday_dates['holyDate'] = pd.to_datetime(all_holiday_dates['holyDate'])

# Fetch orders data from the database
query_orders = "SELECT * FROM orders"
orders = pd.read_sql_query(query_orders, conn)

# Convert 'createdAt' column to datetime format
orders['createdAt'] = pd.to_datetime(orders['createdAt'])

# Extracting date from 'createdAt' column and converting it to datetime format
orders['date'] = pd.to_datetime(orders['createdAt'].dt.date)

# Check if the order date is a holiday or not based on 'is_holiday' column and 'all_holiday_dates'
# Assign 1 if it's a holiday, else 0
orders['is_holiday'] = orders['date'].apply(lambda x: 1 if x in all_holiday_dates.values else 0)

# Convert 'sales' column to Nullable Integer type (Int64)
orders['sales'] = orders['sales'].astype('Int64')

# Calculate mean sales on holidays and regular days

holiday_sales = orders[orders['is_holiday'] == 1]['sales'].mean()
non_holiday_sales = orders[orders['is_holiday'] == 0]['sales'].mean()
mean_holidays_sales_each = pd.DataFrame(orders[orders['is_holiday'] == 1].groupby('date')['sales'].mean())

holiday_dates = mean_holidays_sales_each.index
holiday_sales_series = mean_holidays_sales_each['sales']

holiday_providers = orders[orders['is_holiday'] == 1]['providerId'].nunique()
non_holiday_providers = orders[orders['is_holiday'] == 0]['providerId'].nunique()

holiday_users = orders[orders['is_holiday'] == 1]['userId'].nunique()
non_holiday_users = orders[orders['is_holiday'] == 0]['userId'].nunique()

report = {
    "Average Sales on Public Holidays": holiday_sales,
    "Average Sales on Regular Days": non_holiday_sales,
    "Selling Providers on Public Holidays": holiday_providers,
    "Selling Providers on Regular Days": non_holiday_providers,
    "Purchasing Users on Public Holidays": holiday_users,
    "Purchasing Users on Regular Days": non_holiday_users
}

# Report analysis results
print("Analysis Results:")
for key, value in report.items():
    print(f"{key}: {value}")



with PdfPages('analysis_plots.pdf') as pdf:
    
    # Plot 1: Mean Sales on Holidays vs. Regular Days
    plt.figure(figsize=(10, 6))
    plt.plot(holiday_dates, holiday_sales_series, marker='o', linestyle='-', color='blue', label='Mean Sales on Holidays')
    # Plotting a line for the mean sales on regular days
    plt.axhline(y=non_holiday_sales, color='red', linestyle='--', label='Mean Sales on Regular Days')

    # Labeling the plot
    plt.title('Mean Sales on Holidays vs. Mean Sales on Regular Days')
    plt.xlabel('Date')
    plt.ylabel('Mean Sales')
    plt.legend()
    plt.xticks(rotation=45)  # Rotating x-axis labels for better readability

    plt.tight_layout()
    pdf.savefig()  # Save this plot to PDF

    # Plot 2: Comparison of Selling Providers on Holidays vs. Regular Days
    plt.figure(figsize=(8, 6))
    providers_data = [holiday_providers, non_holiday_providers]
    labels = ['Sales on Holidays', 'Sales on Regular Days']

    plt.bar(labels, providers_data, color=['orange', 'purple'])
    plt.title('Comparison of Selling Providers on Holidays vs. Regular Days')
    plt.ylabel('Number of Providers')

    pdf.savefig()  # Save this plot to PDF

    # Plot 3: Comparison of Purchasing Users on Holidays vs. Regular Days
    users_data = [holiday_users, non_holiday_users]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, users_data, color=['red', 'yellow'])
    plt.title('Comparison of Purchasing Users on Holidays vs. Regular Days')
    plt.ylabel('Number of Users')
    pdf.savefig()  # Save this plot to PDF

# Print or display a message once the PDF is generated
print("Plots saved in analysis_plots.pdf")

