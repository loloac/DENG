# **FITBIT**

**Link to the dashboard**:https://xkcnjaizkukx95nkfa5kwg.streamlit.app/



In this project, we study a dataset with information obtained from fitbits generated by
33 respondents to an amazon survey in 2016 that submitted censored usage data. The
end product will be a dashboard that visualizes key statistics and trends related to health and fitness.

At what time a day people exercise the most? What day in the week do they exercise the most? Does weather and temperature affect people's workout schedules? How does exercise impact our sleep? This dashboard looked into the data to try and answer those questions and many more


### **The Database**

The Database, called **fitbit_database.db** consists of multiple tables with different data on the users
 
  • **daily_activity** : Various statistics that the participants of the survey reported daily.

  • **heart_rate** : Heart rate of each individual measured every 5 seconds.

  • **hourly_calories** : Calories burnt per hour.

  • **hourly_intensity** : Intensity of exercise, given both in total per hour and average per hour.

  • **hourly_steps** : Total amount of steps taken per hour

  • **minute_sleep** : Information on every minute that the participant is asleep.

  • **weight_log** : Information on the weight, fat, BMI for each of the participants.

### **The Dashboard**

The dashboard visualizes data through various graphs, providing insights into the relation between key variables to understand their impact on each other. The Dashboard shows user specific data, data filtered by date ranges and general statiscs, allowing a deeper analysis of trends and patterns to better help the understanding of overall health and fitness metrics.

![image](https://github.com/user-attachments/assets/162fa882-d20b-4519-9628-a13e7e340a6d)

![image](https://github.com/user-attachments/assets/30b2fe65-e2c7-410b-a2dc-3d3764fe402a)

![image](https://github.com/user-attachments/assets/692192f7-7a3f-4957-b8d3-0e3bb05a156c)





### **How to run**

To run it localy, you will first need to install a few libraries. Try `install {library}` or `pip install {library}` on Windows and download the following libraries:

• **pandas** 

• **numpy**

• **matplotlib.pyplot** 

• **datetime**

• **statsmodels.formula.api** 

• **seaborn**

• **sqlite3**

• **scipy.stats**

• **streamlit**

To run the dashboard run on the terminal `streamlit run {dashboard file}`
