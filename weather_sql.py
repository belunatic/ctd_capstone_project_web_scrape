import sqlite3
import pandas as pd
import csv
import os

db_path = 'db/weather_data.db'
# #check if the database file exists
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect('db/weather_data.db')
conn.execute('PRAGMA foreign_keys = ON;')

cursor= conn.cursor()

##create the tables
#continent table
cursor.execute('''CREATE TABLE IF NOT EXISTS continent (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);''')

#country table
cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY,
    country_name TEXT NOT NULL,
    city_name TEXT NOT NULL,
    weather INTEGER NOT NULL,
    time TEXT NOT NULL,
    continent_id INTEGER NOT NULL,
    FOREIGN KEY (continent_id) REFERENCES continent(id)
);''')

conn.commit();

## dataframe from csv file
df = pd.read_csv('cleaned_weather_data.csv')

##get the continent data from the dataframe and insert it into the continent table
continents = df['Continent'].unique()
for continent in continents:
    cursor.execute('INSERT OR IGNORE INTO continent (name) VALUES (?)', (continent,))

##get the weather data from country, city, weather, time and continent_id and insert it into the weather table
for index, row in df.iterrows():
    #get the continent_id from the continent table
    continent_id = cursor.execute('SELECT id FROM continent WHERE name = ?', (row['Continent'],)).fetchone()[0]
    #insert the data into the weather table
    cursor.execute('INSERT INTO weather (country_name, city_name, weather, time, continent_id) VALUES (?, ?, ?, ?, ?)', (row['Country'], row['City'], row['Weather'], row['Time'], continent_id))

conn.commit()

conn.close()