import csv
import pandas as pd
from datetime import datetime
#import from a csv file to a data frame
df = pd.read_csv('weather_data.csv')
print(df.head())

#cLEANING THE DATA FRAME

#check for duplicates in the data frame
duplicates = df.duplicated()
print("\nDuplicates found:", duplicates.sum())


#in-case of duplicate  drop the the row
df = df.drop_duplicates()
print("\nData frame after dropping duplicates:")
print(df.head())

#check for null values in the data frame
null_values = df.isnull().sum()
print("\nNull values found:", null_values.sum())

#drop rows with null values
df = df.dropna()
print("\nData frame after dropping rows with null values:")
print(df.head())

# TRANSFORMING THE DATA FRAME

#convert weather to numerical values
df['Weather'] = df['Weather'].str.replace('°F', '').astype(int)
print("\nData Frame after converting Weather to numerical values and replacing °F:")
print(df.head())

#convert time to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%a %I:%M %p').dt.time
print("\nData Frame after converting Time to datetime format:")
print(df.head())

# filter the data frame by continent
df_africa = df[df['Continent'] == 'Africa']
df_europe = df[df['Continent'] == 'Europe']
df_north_america = df[df['Continent'] == 'North America']
df_south_america = df[df['Continent'] == 'South America']

print("\nData Frame for Africa:")
print(df_africa.head())

print("\nData Frame for Europe:")
print(df_europe.head())

print("\nData Frame for North America:")
print(df_north_america.head())

print("\nData Frame for South America:")
print(df_south_america.head())

#save the cleaned data frame to a new csv file
df.to_csv('cleaned_weather_data.csv', index=False)