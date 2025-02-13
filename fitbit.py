# fitbit.py 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

file = 'daily_acivity.csv'

def read_csv_file(file):
    df = pd.read_csv(file)
    return df

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

    calories_df = pd.DataFrame({'Date': pd.date_range(start=start_date, end=end_date), 'Calories': calories_per_day})
    
    plt.figure(figsize=(12, 6))
    calories_df.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.xlabel("Day")
    plt.ylabel("Total Calories")
    plt.title("Total Calories Burnt per Day by user %d" %id)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    return calories_per_day



df = read_csv_file(file)
unique_users(df)
total_distance_per_user(df)
calories_per_day(df, 1503960366, start_date="2016-04-12", end_date="2016-05-12")