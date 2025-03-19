import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

#i (lolo) gotta use this to run st
#C:\Users\loloa\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\streamlit.exe run DENG/dashboard.py
# Connect to the database

#only imported daily_activity from the database. if you import more tables make sure to add so they are filtered by date or id in the below code
#i indicated below where it is that you can add the charts and stats for each part of the dashboard

conn = sqlite3.connect('DENG/fitbit_database.db')
cursor = conn.cursor()


query = "SELECT * FROM daily_activity"
df = pd.read_sql_query(query, conn)

conn.close()




df['TotalActiveMinutes'] = df['LightlyActiveMinutes'] + df['VeryActiveMinutes'] + df['FairlyActiveMinutes']
gen=st.sidebar.button("General Stats")

unique_ids = df['Id'].unique()
unique_ids = unique_ids.astype(object)
unique_ids = np.insert(unique_ids, 0, "Select Id")
selected_id = st.sidebar.selectbox('See data by Id', unique_ids)
df["ActivityDate"]=pd.to_datetime(df['ActivityDate'])
times=df["ActivityDate"].unique()
times=times.tolist()
times.sort()

min_date = pd.to_datetime(times[0]).to_pydatetime()
max_date = pd.to_datetime(times[-1]).to_pydatetime()
start_date, end_date = st.sidebar.slider("Select Date Range", min_value=min_date, max_value=max_date, value=(min_date, max_date), format="YYYY-MM-DD")
time_df = df[(df['ActivityDate'] >= start_date) & (df['ActivityDate'] < end_date + pd.Timedelta(days=1))]
date_range_button = st.sidebar.button("Click to see data filtered by the chosen date range")

# Filtering data based on selected Id
filtered_df = df[df['Id'] == selected_id]

if gen: #theres a bug here where a long deleted table still appears. if you rerun in streamlit it disappears.

    st.write("Non id-specific data will appear here.")
    col1,col2=st.columns(2)
    with col1:
        avg_lightly_active = df['LightlyActiveMinutes'].mean()
        avg_fairly_active = df['FairlyActiveMinutes'].mean()
        avg_very_active = df['VeryActiveMinutes'].mean()
        fig1, ax1 = plt.subplots()
        activity_types = ['Lightly Active', 'Fairly Active', 'Very Active']
        average_minutes = [avg_lightly_active, avg_fairly_active, avg_very_active]
        ax1.bar(activity_types, average_minutes, color=['green', 'orange', 'blue'])
        ax1.set_xlabel('Activity Type')
        ax1.set_ylabel('Average Minutes')
        ax1.set_title('Average Time Spent in Different Activity Types')
        st.pyplot(fig1)
            
    with col2:
        from fitbit import classified_df
        # Assuming classified_df is a DataFrame with a column "class" containing user types
        user_counts = classified_df['Class'].value_counts()

        fig, ax = plt.subplots()
        user_counts = user_counts.reindex(['Light user', 'Moderate user', 'Heavy user'])
        
        ax.bar(user_counts.index, user_counts.values, color=['red', 'yellow', 'blue'])
        
        ax.set_xlabel('User Type')
        ax.set_ylabel('Count')
        ax.set_title('Number of Users by Type')

        st.pyplot(fig)
######HERE in the if add the code for general statistics

elif selected_id != 'Select Id' and not gen and not date_range_button:
    

    # Plot TotalActiveMinutes vs Calories for all dates for the selected Id
    fig, ax = plt.subplots()
    for date, group in filtered_df.groupby('ActivityDate'):
        ax.scatter(group['TotalActiveMinutes'], group['Calories'], label=date)
    # Add a trend line
    if not filtered_df.empty:
        z = np.polyfit(filtered_df['TotalActiveMinutes'], filtered_df['Calories'], 1)
        p = np.poly1d(z)
        ax.plot(filtered_df['TotalActiveMinutes'], p(filtered_df['TotalActiveMinutes']), "r--", label='Trend Line')
    ax.set_xlabel('Total Active Minutes')
    ax.set_ylabel('Calories')
    ax.set_title(f'Total Active Minutes vs Calories for Id {selected_id}')
    ax.legend(title='Activity Date', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)
######HERE in the if add the code for ID specific data, using filtered_df
elif date_range_button:
    selected_id="Select Id"
    st.write(f"Data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
######HERE in the if add the code for data to be filtered by dates, using time_df