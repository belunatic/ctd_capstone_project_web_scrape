import pandas as pd
import streamlit as st
import sqlite3
import plotly.express as px  
import numpy as np

#get high, low and average temp
def get_high_low(df):
    high_temp = df['Weather'].max()
    low_temp = df['Weather'].min()
    avg_temp = df['Weather'].mean().round(1)

    return high_temp, low_temp, avg_temp

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
continents_list.sort()
#add to the front of the list
continents_list.insert(0,'All Continents')

#since the collected date and time are the same for all rows, we can get the first row's collected date and time
collected_date = df['Collected_Date'].iloc[0]
collected_time = df['Collected_Time'].iloc[0]

#convert the collected date and time to a more readable format
collected_date = pd.to_datetime(collected_date).strftime('%B %d, %Y')
collected_time = pd.to_datetime(collected_time).strftime('%I:%M')    

#get high, low, average temp from the continents
a_high, a_low, a_avg = get_high_low(df_africa)
e_high, e_low, e_avg = get_high_low(df_europe)
na_high, na_low, na_avg = get_high_low(df_north_america)
sa_high, sa_low, sa_avg = get_high_low(df_south_america)
all_high, all_low, all_avg = get_high_low(df)

#page config
page_title = "Weather Data As of " + collected_date + " at " + collected_time;
st.set_page_config(page_title=page_title, page_icon="🌞", layout="wide")


#sidebar
st.sidebar.title('Explore')
sidebar_option = st.sidebar.selectbox('Select Continent', continents_list)

#Main Content
st.title("Weather For Popular Cities")
st.markdown('This data was collected from *timeanddate.com* on ' + collected_date + ' at ' + collected_time + ' PST.')
# st.markdown(f"From {", ".join(continents_list[1:])}")

#display for 'All continent' VS 'A continent'
if sidebar_option == 'All Continents':

    #DISPLAY THE SLIDER ON SIDEBAR
    temp_range = st.sidebar.slider("Temperature", all_low, all_high + 5, all_high)

    ##DISPLAY THE METRICS
    a, b,c,d = st.columns(4)

    a.subheader('Africa')
    a.metric("Highest Temperature", f"{a_high} °F")
    a.metric("Lowest Temperature", f"{a_low} °F")
    a.metric("Average Temperature", f"{a_avg} °F")

    b.subheader('Europe')
    b.metric("Highest Temperature", f"{e_high} °F")
    b.metric("Lowest Temperature", f"{e_low} °F")
    b.metric("Average Temperature", f"{e_avg} °F")

    c.subheader('North America')
    c.metric("Highest Temperature", f"{na_high} °F")
    c.metric("Lowest Temperature", f"{na_low} °F")
    c.metric("Average Temperature", f"{na_avg} °F")

    d.subheader('South America')
    d.metric("Highest Temperature", f"{sa_high} °F")
    d.metric("Lowest Temperature", f"{sa_low} °F")
    d.metric("Average Temperature", f"{sa_avg} °F")

    ## DISPLAY THE SCATTERED PLOT
    #get the hour
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
    #convert the hour to int
    df['Hour'] = df['Hour'].astype(int)
    print(df.head(20))

    # Sort by actual time
    df = df.sort_values( by='Hour', ascending=True)


    # Plot
    fig = px.scatter(
        df[df['Weather'] <= temp_range],
        x='Hour',
        y='Weather',
        color='Continent',
        symbol='Continent',
        title='Weather Data from Africa, Europe, N.America, and S.America',
        hover_data=["Country", "City", "Time"]
    )

    # Label the x-axis
    fig.update_xaxes(title_text="Hours (24hrs) ", dtick=2)
    fig.update_yaxes(title_text="Weather (°F) ", dtick=10)
    st.plotly_chart(fig)