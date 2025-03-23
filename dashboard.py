import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Connect to the database
conn = sqlite3.connect('fitbit_database.db')
cursor = conn.cursor()
query = "SELECT * FROM daily_activity"
df = pd.read_sql_query(query, conn)

st.title("Fitbit Dashboard")

df['TotalActiveMinutes'] = df['LightlyActiveMinutes'] + df['VeryActiveMinutes'] + df['FairlyActiveMinutes']

gen = st.sidebar.button("General Stats")

unique_ids = df['Id'].unique()
unique_ids = unique_ids.astype(object)
unique_ids = np.insert(unique_ids, 0, "Select Id")
selected_id = st.sidebar.selectbox('See data by Id', unique_ids)

df["ActivityDate"] = pd.to_datetime(df['ActivityDate'])
times = df["ActivityDate"].unique()
times = times.tolist()
times.sort()
min_date = pd.to_datetime(times[0]).to_pydatetime()
max_date = pd.to_datetime(times[-1]).to_pydatetime()
start_date, end_date = st.sidebar.slider("Select Date Range", min_value=min_date, max_value=max_date, value=(min_date, max_date), format="YYYY-MM-DD")

time_df = df[(df['ActivityDate'] >= start_date) & (df['ActivityDate'] < end_date + pd.Timedelta(days=1))]

date_range_button = st.sidebar.button("Click to see data filtered by the chosen date range")

# Helper function for sleep analysis
def assignTimeBlock(hour):
    if 0 <= hour < 4:
        return '0-4'
    elif 4 <= hour < 8:
        return '4-8'
    elif 8 <= hour < 12:
        return '8-12'
    elif 12 <= hour < 16:
        return '12-16'
    elif 16 <= hour < 20:
        return '16-20'
    else:
        return '20-24'

def average_sleep(df_sleep, start_date, end_date):
    df_sleep = df_sleep.copy()
    df_sleep['date'] = pd.to_datetime(df_sleep['date'], format='%m/%d/%Y %I:%M:%S %p')
    
    df_sleep = df_sleep[(df_sleep['date'].dt.date >= start_date.date()) & 
                        (df_sleep['date'].dt.date <= end_date.date())]
    
    df_sleep['TimeBlock'] = df_sleep['date'].dt.hour.apply(assignTimeBlock)
    timeblock_total_sleep = df_sleep.groupby('TimeBlock')['value'].sum().reindex(['0-4', '4-8', '8-12', '12-16', '16-20', '20-24'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    timeblock_total_sleep.plot(kind='bar', color='mediumseagreen', edgecolor='black', ax=ax)
    ax.set_xlabel('Time Block (Hours)')
    ax.set_ylabel('Total Sleep Minutes')
    ax.set_title(f'Total Sleep Minutes per 4-Hour Block\n{start_date.date()} to {end_date.date()}')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    return fig

# Filtering data based on selected Id
filtered_df = df[df['Id'] == selected_id]

if gen:
    st.write("Non id-specific data will appear here.")
    col1, col2 = st.columns(2)
    
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
        user_counts = classified_df['Class'].value_counts()
        fig, ax = plt.subplots()
        user_counts = user_counts.reindex(['Light user', 'Moderate user', 'Heavy user'])
        ax.bar(user_counts.index, user_counts.values, color=['red', 'yellow', 'blue'])
        ax.set_xlabel('User Type')
        ax.set_ylabel('Count')
        ax.set_title('Number of Users by Type')
        st.pyplot(fig)

elif selected_id != 'Select Id' and not gen and not date_range_button:
    st.header(f"Showing the Data from ID {selected_id}")
    
    st.write("Total Active Minutes vs Calories")
    fig, ax = plt.subplots()
    for date, group in filtered_df.groupby('ActivityDate'):
        ax.scatter(group['TotalActiveMinutes'], group['Calories'], label=date)
    
    if not filtered_df.empty:
        z = np.polyfit(filtered_df['TotalActiveMinutes'], filtered_df['Calories'], 1)
        p = np.poly1d(z)
        ax.plot(filtered_df['TotalActiveMinutes'], p(filtered_df['TotalActiveMinutes']), "r--", label='Trend Line')
    
    ax.set_xlabel('Total Active Minutes')
    ax.set_ylabel('Calories')
    ax.set_title(f'Total Active Minutes vs Calories for Id {selected_id}')
    ax.legend(title='Activity Date', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)
    
    from fitbit import plot_heart_rate_intensity
    plot_heart_rate = plot_heart_rate_intensity(selected_id)
    st.write("Average Heart Rate and Total Intensity")
    
    if isinstance(plot_heart_rate, str):
        st.warning(plot_heart_rate)
    else:
        st.pyplot(plot_heart_rate)
    
    st.subheader("Sleep Related Data")

if date_range_button:
    st.write(f"Data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    st.subheader("Activity Summary")
    activity_summary = time_df[['LightlyActiveMinutes', 'FairlyActiveMinutes', 'VeryActiveMinutes', 'SedentaryMinutes']].mean()
    st.bar_chart(activity_summary)
    
    st.subheader("Average Steps per Day")
    daily_steps = time_df.groupby(time_df['ActivityDate'].dt.date)['TotalSteps'].mean()
    st.line_chart(daily_steps)
    
    st.subheader("Sleep Data")
    sleep_conn = sqlite3.connect('fitbit_database.db')
    sleep_data = pd.read_sql_query("SELECT * FROM minute_sleep", sleep_conn)
    sleep_conn.close()
    
    if not sleep_data.empty:
        sleep_fig = average_sleep(sleep_data, start_date, end_date)
        st.pyplot(sleep_fig)
    else:
        st.warning("No sleep data available for the selected date range")

conn.close()
