import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#i gotta use this to run st
#C:\Users\loloa\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\streamlit.exe
# Connect to the database

conn = sqlite3.connect('DENG/fitbit_database.db')
cursor = conn.cursor()


query = "SELECT * FROM daily_activity"
df = pd.read_sql_query(query, conn)

conn.close()

times=df["ActivityDate"].unique()
times=times.tolist()
times.sort()


df['TotalActiveMinutes'] = df['LightlyActiveMinutes'] + df['VeryActiveMinutes'] + df['FairlyActiveMinutes']

unique_ids = df['Id'].unique()
selected_id = st.sidebar.selectbox('See data by Id', unique_ids)
selected_time=st.sidebar.selectbox('See data by Day',times)
# Filtering data based on selected Id
filtered_df = df[df['Id'] == selected_id]


if st.sidebar.button('General Statistics'):
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

