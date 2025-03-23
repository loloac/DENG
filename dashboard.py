import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime


#i (lolo) gotta use this to run st
# Connect to the database

#only imported daily_activity from the database. if you import more tables make sure to add so they are filtered by date or id in the below code
#i indicated below where it is that you can add the charts and stats for each part of the dashboard

conn = sqlite3.connect('fitbit_database.db')
cursor = conn.cursor()


query = "SELECT * FROM daily_activity"
df = pd.read_sql_query(query, conn)
query = "SELECT * FROM minute_sleep"
sleep = pd.read_sql_query(query, conn)
quert="SELECT * FROM hourly_intensity"
hourly_intensity = pd.read_sql_query(query, conn)


conn.close()
sleep_by_date = sleep.groupby('date').size().reset_index(name='SleepMinutes')

st.title("Fitbit Dashboard")

df['TotalActiveMinutes'] = df['LightlyActiveMinutes'] + df['VeryActiveMinutes'] + df['FairlyActiveMinutes']

if "selected_id" not in st.session_state:  
    st.session_state.selected_id = "Select Id"

gen = st.sidebar.button("General Statistics", on_click=lambda: st.session_state.update(selected_id="Select Id"))

unique_ids = df['Id'].unique()
unique_ids = unique_ids.astype(object)
unique_ids = np.insert(unique_ids, 0, "Select Id")
selected_id = st.sidebar.selectbox('See data by Id', unique_ids, index=0, key="selected_id")
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

if gen: 

    st.subheader("General Statistics from 33 Users")
    col1,col2=st.columns(2)
    with col1:
        st.write("Average Time Spent in Different Activity Types")
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

        from fitbit import avarage_sleep
        avg_sleep = avarage_sleep()
        st.write("Average Sleep Data")
        st.write(avg_sleep)

        from fitbit import avg_number_of_steps
        avg_steps = avg_number_of_steps()
        st.write("Average Number of Steps")
        st.write(avg_steps)

        from fitbit import workout_frequency_by_day
        workout_counts = workout_frequency_by_day(df)
        st.write("Workout Frequency Data")
        st.bar_chart(workout_counts)

    with col2:
        from fitbit import classified_df
    
        user_counts = classified_df['Class'].value_counts()

        st.write("Number of Users by Type")
        fig, ax = plt.subplots()
        ax.pie(user_counts, labels=user_counts.index, autopct='%1.1f%%', colors=['brown', 'beige', 'blue'], startangle=90)
        ax.set_title("User Distribution by type")
        st.pyplot(fig)


        from fitbit import average_calories_burnt
        avg_calories = average_calories_burnt()
        st.write("Average Calories Burnt")
        st.write(avg_calories)

        df = 'daily_acivity.csv'
        from fitbit import read_csv_file
        df = read_csv_file(df)
        from fitbit import total_distance_per_user
        total_distance = total_distance_per_user(df)
        st.write("Total Distance Covered by Each User")
        st.write(total_distance)

        from fitbit import workout_frequency_by_day
        workout_counts = workout_frequency_by_day(df)
        st.write("                                                                            ")
        st.dataframe(workout_counts)
    st.write("weather related data (excluding lightly active minutes)")
    from fitbit import mergedstuff, temp_vs_activity, rain_vs_activity
    col1, col2 = st.columns(2)
    with col1:
        st.write("Temperature vs Activity")
        st.pyplot(temp_vs_activity(mergedstuff))
    with col2:
        st.write("Rain vs Activity")    
        st.pyplot(rain_vs_activity(mergedstuff))

######HERE in the if add the code for general statistics
#sleep, heart rate intensity, and minute_sleep, calories
elif selected_id != 'Select Id' and not gen and not date_range_button:
    st.header(f"Showing the Data from ID {selected_id}")

    # Plot TotalActiveMinutes vs Calories for all dates for the selected Id
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

    # Plot Heart Rate Intensity
    plot_heart_rate, ax = plt.subplots()
    from fitbit import plot_heart_rate_intensity 
    plot_heart_rate = plot_heart_rate_intensity(selected_id)

    st.write("Avarage Heart Rate and Total Intensity")
    # Check if the function returned a string (no overlapping data)
    if isinstance(plot_heart_rate, str):
        st.warning(plot_heart_rate) 
    else:
        st.pyplot(plot_heart_rate)

    # Sleep related data
    st.subheader("Sleep Related Data")

    from fitbit import plot_sedentary_sleep_correlation
    plot_sleep, ax = plt.subplots()
    plot_sleep = plot_sedentary_sleep_correlation(selected_id)
    st.write("Sedentary Minutes vs Sleep")
    if isinstance(plot_sleep, str):
        st.warning(plot_sleep)
    else:
        st.pyplot(plot_sleep)

    from fitbit import plot_very_active_sleep_correlation
    plot_sleep, ax = plt.subplots()
    plot_sleep = plot_very_active_sleep_correlation(selected_id)
    st.write("Very Active Minutes vs Sleep")
    if isinstance(plot_sleep, str):
        st.warning(plot_sleep)
    else:
        st.pyplot(plot_sleep)

    from fitbit import plot_intensity_sleep_correlation
    plot_sleep, ax = plt.subplots()
    plot_sleep = plot_intensity_sleep_correlation(selected_id)
    st.write("Intensity vs Sleep")
    if isinstance(plot_sleep, str):
        st.warning(plot_sleep)
    else:
        st.pyplot(plot_sleep)




######HERE in the if add the code for ID specific data, using filtered_df
elif date_range_button and selected_id == 'Select Id' and not gen:
    selected_id = "Select Id"
    st.write(f"Data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    st.subheader("Average Steps per Day")
    daily_steps = time_df.groupby(time_df['ActivityDate'].dt.date)['TotalSteps'].mean()
    st.line_chart(daily_steps)


######HERE in the if add the code for data to be filtered by dates

    st.subheader("Average Calories Burnt per Day")
    avg_calories = time_df.groupby(time_df['ActivityDate'].dt.date)['Calories'].mean()
    fig, ax = plt.subplots()
    ax.bar(avg_calories.index, avg_calories.values, color='blue', edgecolor='black')
    ax.set_xlabel('Date')
    ax.set_ylabel('Average Calories')
    ax.set_title('Average Calories Burnt per Day')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    

    def workout_frequency_by_day(df):
        df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], format='%Y-%m-%d')
        avg_calories = df.groupby('ActivityDate')['Calories'].mean()
        
        # Create positions for each bar
        positions = range(len(avg_calories))
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(positions, avg_calories.values, color='blue', edgecolor='black')
        ax.set_xlabel("Date")
        ax.set_ylabel("Average Calories")
        ax.set_title("Average Calories by Date")
        ax.set_xticks(positions)
        ax.set_xticklabels(avg_calories.index.strftime('%Y-%m-%d'), rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        return fig
    st.subheader("Average Calories by Date")
    fig = workout_frequency_by_day(time_df)
    st.pyplot(fig)
