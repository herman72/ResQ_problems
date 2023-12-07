# ResQ_problems
I've addressed the [ResQ Co](https://www.resq-club.com/) Task's Data Analytics Engineering position [questions](https://github.com/resqclub/data-assignment) within this repository.


# Project Setup Instructions

This document provides instructions on how to setup and run this project.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python.

## Installing Dependencies

To install the necessary dependencies for this project, execute the following command:

```bash
pip install -r requirements.txt
```

## Setting Up Metabase
Metabase is used for creating dashboards in this project. You can set it up by visiting either of the following links and following the setup instructions provided in their documentation:

[Jar file](https://www.metabase.com/docs/latest/installation-and-operation/running-the-metabase-jar-file)

[Docker](https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker)

## Full project report

[You can view the full project report at the link below.](https://github.com/herman72/ResQ_problems/blob/main/Project%20Report.pdf)

## File Descriptions

This section provides a detailed description of the files in this project.

### Problem one

#### Python and Jupyter Notebook Files

1. **problemOne.py/problemOne.ipynb**: 
    - Purpose: This file is used to create a table using the pandas library and save it as a database file.
    - Language: Python
    - Libraries Used: pandas
    - *Get results just by run python problemTwo.py*
      

2. **problemOneSql.py/problemOneSql.ipynb**: 
    - Purpose: This file is used to create a view in the database. It establishes a connection between Python and SQLite and executes the query.
    - Language: Python
    - Libraries Used: sqlite3
    - *Get results just by run python problemTwo.py*
      

#### Text Files

1. **viewQuery.txt**: 
    - Purpose: This text file contains the query that is used in Metabase to create the view.


### Problem Two

#### Python and Jupyter Notebook Files

1. **problemTwo.py.py/problemTwo.py.ipynb**: 
    - Purpose: This file is used to create plots and reports.
    - Language: Python
    - Libraries Used: pandas
    - *Get report just by run python problemTwo.py*
      

#### Text Files

1. **avgDailyVsAvgHolidayQuery.txt**: 
    - Purpose: This text file contains the query that is used in Metabase to create a dashboard for comparing average daily sales and holidays.
      
2. **avgDailyVsholidaySeriesQuery.txt**: 
    - Purpose: This text file contains the query that is used in Metabase to create a dashboard for comparing average daily sales and series sales in holidays.
  
3. **npurchasingQuery.txt**: 
    - Purpose: This text file contains the query that is used in Metabase to create a dashboard for comparing the number of purchasing users on normal days and holidays.

4. **sellingProvidersQuery.txt**: 
    - Purpose: This text file contains the query that is used in Metabase to create a dashboard for comparing the number of providers on normal days and holidays.

      
## Automation Instructions

This section provides instructions on how to automate the execution of your Python script and refresh your Metabase dashboard.

### Automating Python Script Execution

To run your Python script periodically, you can use a cron job. Follow these steps:

1. Open your terminal.
2. Type `crontab -e` to edit the cron table.
3. Add the following line to schedule your script to run at midnight (00:00) every day:

```bash
0 0 * * * /usr/bin/python3 /path/to/your/script.py
```
Replace /path/to/your/script.py with the actual path to your Python script.

### Automating Dashboard Refresh in Metabase

To refresh your dashboard in Metabase, you can use the Auto-refresh feature. Follow the instructions provided in the Metabase documentation to set it up.

<img width="1509" alt="Screenshot 2023-12-07 at 4 25 42 at night" src="https://github.com/herman72/ResQ_problems/assets/36226207/7a5ce71a-647f-476e-8e82-14b8a71b9a46">



