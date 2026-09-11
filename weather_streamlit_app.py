import pandas as pd
import streamlit as st
import sqlite3
# import plotly.express as px

#connect to the SQLite database
conn = sqlite3.connect('db/weather_data.db')
conn.execute('PRAGMA foreign_keys = ON;')

#sql to df
sql_statement = """
SELECT w.country_name AS Country, w.city_name AS City, w.weather AS Weather, w.time AS Time, w.collected_date AS Collected_Date, w.collected_time AS Collected_Time, c.name AS Continent
FROM weather w
JOIN continent c ON w.continent_id = c.id
"""

#data frame from sql query
df = pd.read_sql_query(sql_statement, conn)

#filter the data frame by continent
df_africa = df[df['Continent'] == 'Africa']
df_europe = df[df['Continent'] == 'Europe']
df_north_america = df[df['Continent'] == 'North America']
df_south_america = df[df['Continent'] == 'South America']

#get a list of unique continents from the data frame
continents_list = df['Continent'].unique().tolist()
#add another option to the list of continents for all continents
continents_list.append('All Continents')
continents_list.sort()

#since the collected date and time are the same for all rows, we can get the first row's collected date and time
collected_date = df['Collected_Date'].iloc[0]
collected_time = df['Collected_Time'].iloc[0]

#convert the collected date and time to a more readable format
collected_date = pd.to_datetime(collected_date).strftime('%B %d, %Y')
collected_time = pd.to_datetime(collected_time).strftime('%I:%M %p')    

#page config
page_title = "Weather Data As of " + collected_date + " at " + collected_time;
st.set_page_config(page_title=page_title, page_icon="🌞", layout="wide")


#sidebar
st.sidebar.title('Explore')
sidebar_option = st.sidebar.selectbox('Select Continent', continents_list)

#Main Content
st.title("Weather For Popular Cities")
st.markdown('This data was collected from *timeanddate.com* on ' + collected_date + ' at ' + collected_time + ' (local time).')

#display for 'All continent' VS 'A continent'
if sidebar_option == 'All Continents':
    st.metric(f"${df['Country'].values[0]}", f"{df['Weather'].values[0]} F")