import csv
import pandas as pd
from datetime import datetime
#import from a csv file to a data frame
df = pd.read_csv('weather_data.csv')
print(df.head())

#cLEANING THE DATA FRAME

#check for duplicates in the data frame
duplicates = df.duplicated()
print("Duplicates found:", duplicates.sum())
print("Duplicate rows:")
print(df[duplicates])

#check for null values in the data frame
null_values = df.isnull().sum()
print("Null values found:", null_values.sum())

# TRANSFORMING THE DATA FRAME

#convert weather to numerical values
df['Weather'] = df['Weather'].str.replace('°F', '').astype(int)
print(df.head())

#convert time to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%a %I:%M %p').dt.time
print(df.head())

# filter the data frame by continent
df_africa = df[df['Continent'] == 'Africa']
df_europe = df[df['Continent'] == 'Europe']
df_north_america = df[df['Continent'] == 'North America']
df_south_america = df[df['Continent'] == 'South America']

print(df_africa.head())