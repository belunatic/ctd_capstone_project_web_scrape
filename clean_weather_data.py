import csv
import pandas as pd
from datetime import datetime
#import from a csv file to a data frame
df = pd.read_csv('weather_data.csv')
print(df.head())
print("\nData Frame info:")
print(df.info())

#cLEANING THE DATA FRAME

#check for duplicates in the data frame
duplicates = df.duplicated()
print("\nDuplicates found:", duplicates.sum())

#in-case of duplicate drop the row(s) with the duplicate values
df = df.drop_duplicates()
print("\nData frame after dropping duplicates:")
print(df.head())
print("\nData Frame info after dropping duplicates:")
print(df.info())

#check for null values in the data frame
null_values = df.isnull().sum()
print("\nNull values found:", null_values.sum())

#drop rows with null values
df = df.dropna()
print("\nData frame after dropping rows with null values:")
print(df.head())
print("\nData Frame info after dropping rows with null values:")
print(df.info())

# TRANSFORMING THE DATA FRAME

#convert weather to numerical values
df['Weather'] = df['Weather'].str.replace('°F', '').astype(int)
print("\nData Frame after converting Weather to numerical values and replacing °F:")
print(df.head())

#convert time to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%a %I:%M %p').dt.time
print("\nData Frame after converting Time to datetime format:")
print(df.head())

#save the cleaned data frame to a new csv file
df.to_csv('cleaned_weather_data.csv', index=False)