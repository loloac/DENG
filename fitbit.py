# fitbit.py 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statsmodels.formula.api as smf
import seaborn as sns
import sqlite3
import scipy.stats as stats
import streamlit as st
file = 'daily_acivity.csv' # 

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

    fig, ax = plt.subplots(figsize=(12, 7))
    total_distance.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    ax.set_xlabel("User ID")
    ax.set_ylabel("Total Distance")
    ax.set_title("Total Distance Tracked per User")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    return fig

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
    dates = pd.date_range(start=start_date, end=end_date)

    plt.figure(figsize=(12, 6))
    plt.bar(dates, calories_series, color='blue', edgecolor='black')
    plt.xlabel("Day")
    plt.ylabel("Total Calories")
    plt.title("Total Calories Burnt per Day by user %d" %id)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    return calories_per_day
df = read_csv_file(file)
calories_per_day(df, 1503960366, start_date="2016-03-25", end_date="2016-04-8")
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
#unique_users(df)
#total_distance_per_user(df)
#calories_per_day(df, 1503960366, start_date="2016-03-25", end_date="2016-04-8")
#workout_frequency_by_day(df)



activity=pd.read_csv("daily_acivity.csv")  # 
activity.head()

activity["Id"]=activity["Id"].astype("category")
activity.columns

caloriesvstotalsteps=smf.ols(formula="Calories~TotalSteps+Id",data=activity).fit()
#print(regression.summary())
#this linear regression shows the relationship between calories burnt and total steps taken by a given user


def plot_regression(activity, id):
    filtered_activity = activity[activity["Id"] == id]
    if filtered_activity.empty:
        print ("no data")
        return
    individual=smf.ols(formula="Calories~TotalSteps",data=filtered_activity).fit()
    filtered_activity["Predicted_Calories"]=individual.predict(filtered_activity["TotalSteps"])
    plt.figure(figsize=(8,6))
    sns.scatterplot(x=filtered_activity["TotalSteps"],y=filtered_activity["Calories"],label="data")
    sns.lineplot(x=filtered_activity["TotalSteps"],y=filtered_activity["Predicted_Calories"])
    plt.xlabel("Total Steps")
    plt.ylabel("Calories")
    plt.title("Calories Burnt vs Total Steps")
    plt.legend()
    plt.show()

# plot_regression(activity, 1503960366)
#plot of the regression line for user 1503960366

#effects of light activity on calories burnt
#activity["LightlyActiveMinutes"]=activity["LightlyActiveMinutes"].astype("float")
regression_light_activity = smf.ols(formula="Calories~LightlyActiveMinutes", data=activity).fit()
#print(regression_light_activity.summary())

def plot_light_activity_regression(activity):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=activity["LightlyActiveMinutes"], y=activity["Calories"], label="data")
    sns.lineplot(x=activity["LightlyActiveMinutes"], y=regression_light_activity.predict(activity["LightlyActiveMinutes"]), color='red')
    plt.xlabel("Lightly Active Minutes")
    plt.ylabel("Calories")
    plt.title("Calories Burnt vs Lightly Active Minutes")
    plt.legend()
    plt.show()

# plot_light_activity_regression(activity)
#as the plot shows, theres a slight effect of light activity on calories.
#no high burn of calories is recorded with a high number of lightly active minutes

#shows time spent on each activity type
'''
def most_common_act(df):
    types = df[['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes']].sum()
    types.index = ['Very Active', 'Fairly Active', 'Lightly Active', 'Sedentary']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    types.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    
    ax.set_xlabel("Activity Type")
    ax.set_ylabel("Total Minutes")
    ax.set_title("Total Minutes Spent on Each Activity Type")
    ax.set_xticklabels(types.index, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    st.pyplot(fig)
'''
# print("HEREEEEEEEE",most_common_act(activity))
#as one would expect, the most common activity is sedentary
# Fetching all table names from the database

# PART 3 ####################################################

print('\n\n\nPART 3\n\n\n')

conection = sqlite3.connect('fitbit_database.db')
cursor = conection.cursor()

query = "SELECT Id, COUNT(Id) FROM daily_activity GROUP BY Id"
df_activity = pd.read_sql_query(query, conection)
print(df_activity.head())

df_activity["Id"] = df_activity["Id"].astype(int)

def classify_user(count):
    if count <= 10:
        return "Light user"
    elif count <= 15:
        return "Moderate user"
    else:
        return "Heavy user"

df_activity["Class"] = df_activity[df_activity.columns[1]].apply(classify_user)
classified_df = df_activity[["Id", "Class"]]

print(classified_df.head())



#whether duration of sleep is related to active minutes
query="SELECT * FROM minute_sleep"
minute_sleep=pd.read_sql_query(query,conection)


query="SELECT * from daily_activity"
daily_activity=pd.read_sql_query(query,conection)


#total active minutes column
daily_activity['TotalActiveMinutes'] = daily_activity['LightlyActiveMinutes'] + daily_activity['FairlyActiveMinutes']+daily_activity['VeryActiveMinutes']


minute_sleep['Date'] = pd.to_datetime(minute_sleep['date'], format='%m/%d/%Y %I:%M:%S %p').dt.date

# sum all value 1's for each Id/day to get the total minutes of sleep
sleep_sum = minute_sleep[minute_sleep['value'] == 1].groupby(['Id', 'Date'])['value'].sum().reset_index()


sleep_sum['Id'] = sleep_sum['Id'].astype(int)
daily_activity['Id'] = daily_activity['Id'].astype(int)
#rename the date column to match sleep table
daily_activity['ActivityDate'] = pd.to_datetime(daily_activity['ActivityDate'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
daily_activity.rename(columns={'ActivityDate': 'Date'}, inplace=True)
sleep_sum['Date'] = pd.to_datetime(sleep_sum['Date']).dt.strftime('%Y-%m-%d')

#finding the intersection of ids and dates in order to make the regression
common_ids_dates = set(sleep_sum[['Id', 'Date']].apply(tuple, axis=1)).intersection(set(daily_activity[['Id', 'Date']].apply(tuple, axis=1)))
#filtering the df´s
sleep_sum = sleep_sum[sleep_sum[['Id', 'Date']].apply(tuple, axis=1).isin(common_ids_dates)]
daily_activity = daily_activity[daily_activity[['Id', 'Date']].apply(tuple, axis=1).isin(common_ids_dates)]

sleep_and_minutes = pd.merge(sleep_sum, daily_activity, on=['Id', 'Date'])

#linear regression to see if there is a relationship between total active minutes and sleep

regression_active_minutes = smf.ols(formula="value ~ TotalActiveMinutes", data=sleep_and_minutes).fit()
print(regression_active_minutes.summary())

def plotregression(sleep_and_minutes):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=sleep_and_minutes["TotalActiveMinutes"], y=sleep_and_minutes["value"], label="data")
    sns.lineplot(x=sleep_and_minutes["TotalActiveMinutes"], y=regression_active_minutes.predict(sleep_and_minutes["TotalActiveMinutes"]), color='red')
    plt.xlabel("Total Active Minutes")
    plt.ylabel("Sleep minutes")
    plt.title("Effect of Total Active Minutes on sleep minutes")
    plt.legend()
    plt.show()

plotregression(sleep_and_minutes)

#the regression shows hardly any relationship btw sleep and minutes
#------------------------------------------------------------
#effects of sedentary minutes on sleep
regression_sedentary_minutes = smf.ols(formula="value ~ SedentaryMinutes", data=sleep_and_minutes).fit()
print(regression_sedentary_minutes.summary())

def plotregression_sedentary(sleep_and_minutes):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=sleep_and_minutes["SedentaryMinutes"], y=sleep_and_minutes["value"], label="data")
    sns.lineplot(x=sleep_and_minutes["SedentaryMinutes"], y=regression_sedentary_minutes.predict(sleep_and_minutes["SedentaryMinutes"]), color='red')
    plt.xlabel("Sedentary Minutes")
    plt.ylabel("Sleep minutes")
    plt.title("Effect of Sedentary Minutes on sleep minutes")
    plt.legend()
    plt.show()

plotregression_sedentary(sleep_and_minutes)
#the regression shows a low negative relationship

#Q Q plot to verify data is normally distributed


def qqnormality(regression_model):
    residuals = regression_model.resid
    plt.figure(figsize=(8, 6))
    stats.probplot(residuals, dist="norm", plot=plt)
    plt.title('Q-Q Plot')
    plt.xlabel('Theoretical Quantiles')
    plt.ylabel('Sample Quantiles')

    plt.show()

qqnormality(regression_sedentary_minutes)
#errors seem to be normally distributed

#Dividing the database in blocks of 4 hours
hourlySteps = pd.read_sql_query("SELECT * FROM hourly_steps", conection)
hourlySteps['ActivityHour'] = pd.to_datetime(hourlySteps['ActivityHour'])
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
hourlySteps['TimeBlock'] = hourlySteps['ActivityHour'].dt.hour.apply(assignTimeBlock)
averageStepsBlock = hourlySteps.groupby('TimeBlock')['StepTotal'].mean()

#Barplot for average number of steps
def avg_number_of_steps():
    hourlySteps = pd.read_sql_query("SELECT * FROM hourly_steps", sqlite3.connect('fitbit_database.db'))
    hourlySteps['ActivityHour'] = pd.to_datetime(hourlySteps['ActivityHour'])
    hourlySteps['TimeBlock'] = hourlySteps['ActivityHour'].dt.hour.apply(assignTimeBlock)
    averageStepsBlock = hourlySteps.groupby('TimeBlock')['StepTotal'].mean()
    averageStepsBlock = averageStepsBlock.reindex(['0-4', '4-8', '8-12', '12-16', '16-20', '20-24'])

    fig, ax = plt.subplots(figsize=(10, 6))
    averageStepsBlock.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    ax.set_xlabel('Time Block (Hours)')
    ax.set_ylabel('Average Steps')
    ax.set_title('Average Steps Taken in 4-Hour Blocks')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    return fig

#Barplot for average calories burnt
def average_calories_burnt():
    conection = sqlite3.connect('fitbit_database.db')
    
    hourlyCalories = pd.read_sql_query("SELECT * FROM hourly_calories", conection)
    
    conection.close()
    
    hourlyCalories['ActivityHour'] = pd.to_datetime(hourlyCalories['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')
    hourlyCalories['TimeBlock'] = hourlyCalories['ActivityHour'].dt.hour.apply(assignTimeBlock)
    timeblock_avg_calories = hourlyCalories.groupby('TimeBlock')['Calories'].mean().reindex(['0-4', '4-8', '8-12', '12-16', '16-20', '20-24'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    timeblock_avg_calories.plot(kind='bar', color='lightcoral', edgecolor='black', ax=ax)
    ax.set_xlabel('Time Block (Hours)')
    ax.set_ylabel('Average Calories Burned')
    ax.set_title('Average Calories Burned per 4-Hour Block')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    return fig
#According to the dataset, it makes sense how the average calories are burnt throughout the 6 blocks of 
#4 hours, it also makes sense that calories are burnt at times where the user might be sleeping,
#this is because you also burn calories when you sleep.

#Barplot for average sleep
def avarage_sleep():
    conection = sqlite3.connect('fitbit_database.db')
    df_sleep = pd.read_sql_query("SELECT * FROM minute_sleep", conection)
    
    conection.close()
    
    df_sleep['date'] = pd.to_datetime(df_sleep['date'], format='%m/%d/%Y %I:%M:%S %p')
    df_sleep['TimeBlock'] = df_sleep['date'].dt.hour.apply(assignTimeBlock)
    
    timeblock_total_sleep = df_sleep.groupby('TimeBlock')['value'].sum().reindex(['0-4', '4-8', '8-12', '12-16', '16-20', '20-24'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    timeblock_total_sleep.plot(kind='bar', color='mediumseagreen', edgecolor='black', ax=ax)
    ax.set_xlabel('Time Block (Hours)')
    ax.set_ylabel('Total Sleep Minutes')
    ax.set_title('Total Sleep Minutes per 4-Hour Block')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    return fig

#weather relationship to activity
weather=pd.read_csv("chicago.csv")
weather=weather[["datetime","temp","precip"]]

activitee = sleep_and_minutes[["Id", "Date", "TotalActiveMinutes","VeryActiveMinutes","FairlyActiveMinutes","LightlyActiveMinutes"]]

#ensuring the date formats match
weather['datetime'] = pd.to_datetime(weather['datetime'], format='%Y-%m-%d')
activitee['Date'] = pd.to_datetime(activitee['Date'], format='%Y-%m-%d')


mergedstuff = pd.merge(activitee, weather, left_on='Date', right_on='datetime')
# Define quintiles and corresponding labels
quintiles = pd.qcut(mergedstuff['temp'], 5, labels=["Very Cold", "Cold", "Mildly cold", "Mild", "Mildly warm"])

# Add the quintile labels to the dataframe
mergedstuff['temp_feel'] = quintiles

quartiles = pd.qcut(
    mergedstuff['precip'], 
    4, 
    labels=["Very Dry", "Dry", "Mildly Wet", "Wet"], 
    duplicates="drop"
)
mergedstuff['precip_feel'] = quartiles

def temp_vs_activity(mergedstuff):
    # Calculate the average minutes for each activity type per temperature feel
    activity_avg_by_temp = mergedstuff.groupby('temp_feel')[['VeryActiveMinutes', 'FairlyActiveMinutes']].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    activity_avg_by_temp.plot(kind='bar', stacked=True, color=['red', 'orange'], edgecolor='black', ax=ax)
    ax.set_xlabel('Temperature Feel')
    ax.set_ylabel('Average Minutes')
    ax.set_title('Average Activity Minutes by Temperature Feel')
    ax.set_xticklabels(activity_avg_by_temp.index, rotation=45)
    ax.legend(title='Activity Type')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    return fig

def rain_vs_activity(mergedstuff):
    # Calculate the average minutes for each activity type per precipitation feel
    activity_avg_by_rain = mergedstuff.groupby('precip_feel')[['VeryActiveMinutes', 'FairlyActiveMinutes']].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    activity_avg_by_rain.plot(kind='bar', stacked=True, color=['blue', 'cyan'], edgecolor='black', ax=ax)

    ax.set_xlabel('Precipitation Feel')
    ax.set_ylabel('Average Minutes')
    ax.set_title('Average Activity Minutes by Precipitation Feel')
    ax.set_xticklabels(activity_avg_by_rain.index, rotation=45)
    ax.legend(title='Activity Type')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    return fig

#prof said we should do an interaction plot as well... unfinished business

# Write a function that takes an Id as input and returns a figure that contains
# heart rate of this individual and the total intensity of the exercise taken

def plot_heart_rate_intensity(id):
    conection = sqlite3.connect('fitbit_database.db')
    
    query = f"SELECT * FROM heart_rate WHERE Id = {id}"
    heart_rate = pd.read_sql_query(query, conection)

    query = f"SELECT * FROM hourly_intensity WHERE Id = {id}"
    hourly_intensity = pd.read_sql_query(query, conection)

    heart_rate['Time'] = pd.to_datetime(heart_rate['Time'], format='%m/%d/%Y %I:%M:%S %p')
    hourly_intensity['ActivityHour'] = pd.to_datetime(hourly_intensity['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')

    heart_rate['Hour'] = heart_rate['Time'].dt.floor('H')
    avg_heart_rate_per_hour = heart_rate.groupby('Hour')['Value'].mean().reset_index()
    avg_heart_rate_per_hour.rename(columns={'Value': 'AvgHeartRate'}, inplace=True)

    merged_df = pd.merge(avg_heart_rate_per_hour, hourly_intensity, left_on='Hour', right_on='ActivityHour')

    if merged_df.empty:
        return f"Unfortunately, there is no overlapping data for user {id}."

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Average Heart Rate', color='tab:blue')
    ax1.plot(merged_df['Hour'], merged_df['AvgHeartRate'], label='Average Heart Rate', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Total Intensity', color='tab:red')
    ax2.plot(merged_df['Hour'], merged_df['TotalIntensity'], label='Total Intensity', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    fig.tight_layout()
    plt.title(f"Average Heart Rate and Total Intensity per Hour - User {id}")

    return fig

plot_heart_rate_intensity(4558609924)

#PART 4 - DATA WRANGLING ####################################################
query="SELECT * FROM weight_log"
weight_log=pd.read_sql_query(query,conection)
print(weight_log.head())
# length
print(weight_log.shape) #33 rows and 4 columns

missing_values = weight_log.isnull().sum()
print("Missing values per column in weight_log:")
print(missing_values)

#31 missing values in fat out of 33
#2 out of 33 in weight kg
#replacing weight kg with weight pounds times 0.453592(1 pound = 0.453592 kg)
weight_log['WeightKg']=weight_log['WeightKg'].fillna(weight_log['WeightPounds']/0.453592)
#for fat, we only have 2 values out of 33. therefore, we can drop the column
weight_log.drop('Fat',axis=1,inplace=True)

dailyQuery = "SELECT * FROM daily_activity"
daily_log = pd.read_sql_query(dailyQuery, conection)
grouped = daily_log.groupby("Id")
correlations = grouped.apply(lambda x: x["TotalSteps"].corr(x["TotalDistance"]))
print(correlations)

#Plotting the correlation between sedentary minutes and minutes of sleep
def plot_sedentary_sleep_correlation(id):
    connection = sqlite3.connect('fitbit_database.db')

    query = f"SELECT * FROM minute_sleep WHERE Id = {id}"
    minute_sleep = pd.read_sql_query(query, connection)
    query = f"SELECT * FROM daily_activity WHERE Id = {id}"
    daily_activity = pd.read_sql_query(query, connection)

    minute_sleep['Date'] = pd.to_datetime(minute_sleep['date']).dt.date
    daily_activity['Date'] = pd.to_datetime(daily_activity['ActivityDate']).dt.date
    
    sleep_by_date = minute_sleep.groupby('Date').size().reset_index(name='SleepMinutes')
    merged_df = pd.merge(sleep_by_date, daily_activity, on='Date', how='inner')

    if merged_df.empty:
        return f"Unfortunately, there is no overlapping data for user {id}."
    
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    x = [str(date) for date in merged_df['Date']]
    x_pos = np.arange(len(x))
    width = 0.35
    
    bars1 = ax1.bar(x_pos - width/2, merged_df['SedentaryMinutes'], width, color='tab:blue', label='Sedentary')
    ax1.set_ylabel('Sedentary Minutes', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x_pos + width/2, merged_df['SleepMinutes'], width, color='tab:red', label='Sleep')
    ax2.set_ylabel('Sleep Minutes', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    ax1.set_xlabel('Date')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(x, rotation=45, ha='right') 
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')
    
    plt.title(f"Sedentary vs Sleep Minutes for ID: {id}")
    plt.tight_layout()

    return fig

plot_sedentary_sleep_correlation(1503960366)

def plot_very_active_sleep_correlation(id):
    connection = sqlite3.connect('fitbit_database.db')

    query = f"SELECT * FROM minute_sleep WHERE Id = {id}"
    minute_sleep = pd.read_sql_query(query, connection)
    query = f"SELECT * FROM daily_activity WHERE Id = {id}"
    daily_activity = pd.read_sql_query(query, connection)

    minute_sleep['Date'] = pd.to_datetime(minute_sleep['date']).dt.date
    daily_activity['Date'] = pd.to_datetime(daily_activity['ActivityDate']).dt.date
    
    sleep_by_date = minute_sleep.groupby('Date').size().reset_index(name='SleepMinutes')
    merged_df = pd.merge(sleep_by_date, daily_activity, on='Date', how='inner')

    if merged_df.empty:
        return f"Unfortunately, there is no overlapping data for user {id}."

    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    x = [str(date) for date in merged_df['Date']]
    x_pos = np.arange(len(x))
    width = 0.35
    
    bars1 = ax1.bar(x_pos - width/2, merged_df['VeryActiveMinutes'], width, color='tab:blue', label='ActiveMinutes')
    ax1.set_ylabel('Active Minutes', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x_pos + width/2, merged_df['SleepMinutes'], width, color='tab:red', label='Sleep')
    ax2.set_ylabel('Sleep Minutes', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    ax1.set_xlabel('Date')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(x, rotation=45, ha='right') 
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')
    
    plt.title(f"Active Minutes vs Sleep Minutes for ID: {id}")
    plt.tight_layout()
    plt.show()

    return fig

plot_very_active_sleep_correlation(1503960366)

def plot_intensity_sleep_correlation(id):
    connection = sqlite3.connect('fitbit_database.db')
    
    query = f"SELECT * FROM hourly_intensity WHERE Id = {id}"
    hourly_intensity = pd.read_sql_query(query, connection)
    query = f"SELECT * FROM minute_sleep WHERE Id = {id}"
    minute_sleep = pd.read_sql_query(query, connection)
    
    minute_sleep['Date'] = pd.to_datetime(minute_sleep['date']).dt.date
    hourly_intensity['Date'] = pd.to_datetime(hourly_intensity['ActivityHour']).dt.date
    
    sleep_by_date = minute_sleep.groupby('Date').size().reset_index(name='SleepMinutes')
    intensity_by_date = hourly_intensity.groupby('Date')['AverageIntensity'].mean().reset_index()

    merged_df = pd.merge(sleep_by_date, intensity_by_date, on='Date', how='inner')

    if merged_df.empty:
        return f"Unfortunately, there is no overlapping data for user {id}."

    merged_df['DateStr'] = merged_df['Date'].astype(str)
    
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    x = merged_df['DateStr']
    x_pos = np.arange(len(x))
    width = 0.35
    
    bars1 = ax1.bar(x_pos - width/2, merged_df['AverageIntensity'], width, color='tab:blue', label='AverageIntensity')
    ax1.set_ylabel('Average Intensity', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x_pos + width/2, merged_df['SleepMinutes'], width, color='tab:red', label='Sleep')
    ax2.set_ylabel('Sleep Minutes', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_xlabel('Date')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(x, rotation=45, ha='right')
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')
    
    plt.title(f"Average Intensity vs Sleep Minutes for ID: {id}")
    plt.tight_layout()
    plt.show()

    return fig
    #
plot_intensity_sleep_correlation(1503960366)
#---------

