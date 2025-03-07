# fitbit.py 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statsmodels.formula.api as smf
import seaborn as sns
import sqlite3
import scipy.stats as stats
file = 'daily_acivity.csv'

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



activity=pd.read_csv("daily_acivity.csv")
activity.head()

activity["Id"]=activity["Id"].astype("category")
activity.columns

#regression=smf.ols(formula="Calories~TotalSteps+Id",data=activity).fit()
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
def most_common_act(df):
    types = df[['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes']].sum()
    most_common = types.idxmax()
    types.index = ['Very Active', 'Fairly Active', 'Lightly Active', 'Sedentary']
    plt.figure(figsize=(12, 6))
    types.plot(kind='bar', color='skyblue', edgecolor='black')
    
    plt.xlabel("Activity Type")
    plt.ylabel("Total Minutes")
    plt.title("Total Minutes Spent on Each Activity Type")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    return most_common, types[most_common]

# most_common_act(activity)
#as one would expect, the most common activity is sedentary

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
result_df = df_activity[["Id", "Class"]]

print(result_df.head())



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
plt.figure(figsize=(10, 6))
averageStepsBlock = averageStepsBlock.reindex(['0-4', '4-8', '8-12', '12-16', '16-20', '20-24'])
averageStepsBlock.plot(kind='bar', color='skyblue', edgecolor='black')
plt.xlabel('Time Block (Hours)')
plt.ylabel('Average Steps')
plt.title('Average Steps Taken in 4-Hour Blocks')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#Barplot for average calories burnt
hourlyCalories = pd.read_sql_query("SELECT * FROM hourly_calories", conection)
hourlyCalories['ActivityHour'] = pd.to_datetime(hourlyCalories['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')
hourlyCalories['TimeBlock'] = hourlyCalories['ActivityHour'].dt.hour.apply(assignTimeBlock)
timeblock_avg_calories = hourlyCalories.groupby('TimeBlock')['Calories'].mean().reindex(['0-4', '4-8', '8-12', '12-16', '16-20', '20-24'])
plt.figure(figsize=(10, 6))
timeblock_avg_calories.plot(kind='bar', color='lightcoral', edgecolor='black')
plt.xlabel('Time Block (Hours)')
plt.ylabel('Average Calories Burned')
plt.title('Average Calories Burned per 4-Hour Block')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
#According to the dataset, it makes sense how the average calories are burnt throughout the 6 blocks of 
#4 hours, it also makes sense that calories are burnt at times where the user might be sleeping,
#this is because you also burn calories when you sleep.

#Barplot for average sleep
df_sleep = pd.read_sql_query("SELECT * FROM minute_sleep", conection)
# Convert the date column to full day
df_sleep['date'] = pd.to_datetime(df_sleep['date'], format='%m/%d/%Y %I:%M:%S %p')
df_sleep['TimeBlock'] = df_sleep['date'].dt.hour.apply(assignTimeBlock)
timeblock_total_sleep = df_sleep.groupby('TimeBlock')['value'].sum().reindex(['0-4', '4-8', '8-12', '12-16', '16-20', '20-24'])
plt.figure(figsize=(10, 6))
timeblock_total_sleep.plot(kind='bar', color='mediumseagreen', edgecolor='black')
plt.xlabel('Time Block (Hours)')
plt.ylabel('Total Sleep Minutes')
plt.title('Total Sleep Minutes per 4-Hour Block')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#weather relationship to activity
weather=pd.read_csv("DENG/chicago.csv")
weather=weather[["datetime","temp","precip"]]

activitee = sleep_and_minutes[["Id", "Date", "TotalActiveMinutes"]]

#ensuring the date formats match
weather['datetime'] = pd.to_datetime(weather['datetime'], format='%Y-%m-%d')
activitee['Date'] = pd.to_datetime(activitee['Date'], format='%Y-%m-%d')

#merging the weather and activity dataframes on the date
merged_df = pd.merge(activitee, weather, left_on='Date', right_on='datetime')
print(merged_df.head())
def plot_weather_vs_activity(merged_df):
    plt.figure(figsize=(14, 6))

    # Precipitation vs Active Minutes
    plt.subplot(1, 2, 1)
    sns.scatterplot(x=merged_df['precip'], y=merged_df['TotalActiveMinutes'], label="data")
    sns.lineplot(x=merged_df['precip'], y=smf.ols(formula="TotalActiveMinutes ~ precip", data=merged_df).fit().predict(merged_df['precip']), color='red')
    plt.xlabel("Precipitation")
    plt.ylabel("Total Active Minutes")
    plt.title("Total Active Minutes vs Precipitation")
    plt.legend()

    # Temperature vs Active Minutes
    plt.subplot(1, 2, 2)
    sns.scatterplot(x=merged_df['temp'], y=merged_df['TotalActiveMinutes'], label="data")
    sns.lineplot(x=merged_df['temp'], y=smf.ols(formula="TotalActiveMinutes ~ temp", data=merged_df).fit().predict(merged_df['temp']), color='red')
    plt.xlabel("Temperature")
    plt.ylabel("Total Active Minutes")
    plt.title("Total Active Minutes vs Temperature")
    plt.legend()

    plt.tight_layout()
    plt.show()

#plot_weather_vs_activity(merged_df)

#prof said we should do an interaction plot as well... unfinished business


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

#---------
