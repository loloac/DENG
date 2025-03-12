import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#command to run streamlit:
#C:\Users\loloa\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\streamlit.exe
# Connect to the database
conn = sqlite3.connect('DENG/fitbit_database.db')#i put up my own filepath as i couldnt do it otherwise
cursor = conn.cursor()

# Retrieve data from the database
query = "SELECT * FROM daily_activity"  # Replace 'your_table_name' with the actual table name
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Add a new column 'TotalActiveMinutes' that sums 'LightlyActiveMinutes', 'VeryActiveMinutes', and 'FairlyActiveMinutes'
df['TotalActiveMinutes'] = df['LightlyActiveMinutes'] + df['VeryActiveMinutes'] + df['FairlyActiveMinutes']



# Streamlit sidebar to select unique Id
unique_ids = df['Id'].unique()
selected_id = st.sidebar.selectbox('See data by Id', unique_ids)

# Add a button on the sidebar for general statistics
if st.sidebar.button('General Statistics'):
    st.write("General statistics content will be added here.")
else:
    # Filter data based on selected Id
    filtered_df = df[df['Id'] == selected_id]




# Plot TotalActiveMinutes vs Calories for all dates for the selected Id
fig, ax = plt.subplots()
for date, group in filtered_df.groupby('ActivityDate'):
    ax.scatter(group['TotalActiveMinutes'], group['Calories'], label=date)
    # Add a trend line
    z = np.polyfit(filtered_df['TotalActiveMinutes'], filtered_df['Calories'], 1)
    p = np.poly1d(z)
    ax.plot(filtered_df['TotalActiveMinutes'], p(filtered_df['TotalActiveMinutes']), "r--")

ax.set_xlabel('Total Active Minutes')
ax.set_ylabel('Calories')
ax.set_title(f'Total Active Minutes vs Calories for Id {selected_id}')
ax.legend(title='Activity Date', bbox_to_anchor=(1.05, 1), loc='upper left')

st.pyplot(fig)


#what i got until now is the following:
#theres a sidebar in which you can pick an Id, and it will show the data available for each day.
