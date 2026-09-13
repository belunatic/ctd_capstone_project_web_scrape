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

#print out the city and temps
def print_continent_city_temp(row):
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; width: 100%;, padding-left:10px;padding-right:10px;margin-top:20px;">
        <span><strong>{row['Country']}, {row['City']}</strong></span>
        <span style="text-align: right;">{row['Weather']}°F</span>
        </div>
        """, unsafe_allow_html=True)

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
st.set_page_config(page_title=page_title, page_icon="🌞", layout="wide", initial_sidebar_state='expanded')


#sidebar
st.sidebar.title('Explore')
#app recap
with st.sidebar.expander('About the Weather App'):
    st.write(f'This app gives you a quick snapshot of real‑time temperatures across popular cities in Africa, Europe, North America, and South America, offering an easy way to compare weather conditions around the world. Using data retrieved from timeanddate.com, it presents a {collected_date}, {collected_time} snapshot that helps build awareness of global climate differences and gives users a simple, visual sense of what the weather feels like across continents.')

sidebar_option = st.sidebar.selectbox('Select Continent', continents_list)

#Main Content
st.title("Weather In Popular Cities")
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

    st.divider()

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
else:
    #get the filtered df from the original df
    df = df[df['Continent'] == sidebar_option]

    #get high, low, avg temp
    high, low, avg = get_high_low(df)

    #heading
    st.markdown(f'## {sidebar_option} Weather')

    #columns
    a,b,c = st.columns(3)
    st.divider()
    d,e = st.columns(2)

    #metrics
    with a:
        st.metric("Highest Temperature", f"{high} °F")
    with b:
        st.metric("Lowest Temperature", f"{low} °F")
    with c:
        st.metric("Average Temperature", f"{avg} °F")


    #sort and get the top 5 and bottom 5
    df_sorted_by_temp = df.sort_values(by='Weather', ascending=False)

    with d:
        #get the df with high and low
        df_high = df_sorted_by_temp.head(5)
        df_low = df_sorted_by_temp.tail(5)

        #bar graphs
        fig = px.bar(
            df_high,
            y=df_high['City'],
            x=df_high['Weather'],
            orientation='h',
            title=f'Highest Temperature Cities in {sidebar_option}',
            hover_data=["Country", "Time"],
            )
        fig.update_traces(marker_color='red')
        fig.update_xaxes(dtick=5, range=[0,df_high['Weather'].max()+10])

        st.plotly_chart(fig, use_container_width=True)

        fig = px.bar(
            df_low,
            y=df_low['City'],
            x=df_low['Weather'],
            orientation='h',
            title=f'Lowest Temperature Cities in {sidebar_option}',
            hover_data=["Country", "Time"],
            )

        fig.update_xaxes(dtick=5, range=[0,df_high['Weather'].max()+10])

        st.plotly_chart(fig, use_container_width=True)

    with e:
        #sort country
        df_sort_country = df.sort_values(by='Country')
        #heading
        st.markdown("### Country, City and Temperatures")
        #display continent country, city, and temp
        df_sort_country.apply(print_continent_city_temp, axis=1)

st.caption('Data is from [timeanddate.com](https://www.timeanddate.com/weather/)')

