# fitbit.py 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

file = 'DENG/daily_acivity.csv'

def read_csv_file(file):
    df = pd.read_csv(file)
    return df

# A) Count how many unique users there are in the dataset and then compute the total 
# distance the fitbits registered for each user. Display the results in a suitable graph.

def unique_users(df):
    users = df['Id'].nunique()
    print('Number of unique users: %d\n' %users)
    return users

def total_distance_per_user(df):
    total_distance = df.groupby('Id')['TotalDistance'].sum()
    print('Total distance per user:')
    print(total_distance)
    print('\n')

    plt.figure(figsize=(12, 6))
    total_distance.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.xlabel("User ID")
    plt.ylabel("Total Distance")
    plt.title("Total Distance Tracked per User")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    return total_distance

# B) To make it more user-specific, implement a function that takes as input a user
# Id and displays a line graph that shows the calories burnt on each day.
# Improve your function to select a specific range of dates in which results are shown.

def calories_per_day(df, id, start_date, end_date):
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], format='%m/%d/%Y')
    
    calories_per_day = []
    user = df[df['Id'] == id]

    while current_date <= end_date:
        daily_calories = user[user['ActivityDate'] == current_date]['Calories'].sum()
        calories_per_day.append(daily_calories)
        current_date += timedelta(days=1) 

    calories_series = pd.Series(calories_per_day, name="Calories Burnt")
    
    plt.figure(figsize=(12, 6))
    calories_series.plot(kind='bar', color='blue', edgecolor='black')
    plt.xlabel("Day")
    plt.ylabel("Total Calories")
    plt.title("Total Calories Burnt per Day by user %d" %id)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    return calories_per_day

# Use datetime or manually look op the day of the week for each date and make a barplot
# with the day on the x-axis and the frequency at which all individuals work out on the
# respective day on the y-axis.

def workout_frequency_by_day(df):
    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], format='%m/%d/%Y')

    df['DayOfWeek'] = df['ActivityDate'].dt.day_name()

    workout_counts = df['DayOfWeek'].value_counts()

    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    workout_counts = workout_counts.reindex(ordered_days, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.bar(workout_counts.index, workout_counts.values, color='blue', edgecolor='black')
    plt.xlabel("Day of the Week")
    plt.ylabel("Workout Frequency")
    plt.title("Workout Frequency by Day of the Week")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    return workout_counts


# Test Cases =================================================================

df = read_csv_file(file)
unique_users(df)
total_distance_per_user(df)
calories_per_day(df, 1503960366, start_date="2016-03-25", end_date="2016-04-8")
workout_frequency_by_day(df)