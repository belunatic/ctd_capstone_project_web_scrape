import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import csv
from datetime import datetime

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# hold the results for each continent
weather_data = []

def get_weather_data(driver, continent):
    results=[]
    
    table_body_row = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')    
    if len(table_body_row) > 0 and table_body_row: 
        for row in table_body_row:
            result_dict={}
            cells = row.find_elements(By.TAG_NAME, 'td')
            #get the country and city
            if cells:
                country_city = cells[0].find_element(By.TAG_NAME, 'a').text
                # Split the country and city
                if ', ' in country_city:
                    the_split= country_city.split(', ')
                    result_dict['Country'] = the_split[0]
                    result_dict['City'] = the_split[1]
                else:
                    result_dict['Country'] = country_city
                    # result_dict['City'] = None
                #get the current time and weather
                result_dict['Time'] = cells[1].text
                result_dict['Weather'] = cells[3].text
                result_dict['Continent'] = continent
                #append the result_dict to the results list
                results.append(result_dict)
    return results


#web scraping for weather data from timeanddate.com for Africa, Europe, North America, and South America
try:
    
    # get the weather data for Africa, Europe, North America, and South America
    driver.get("https://www.timeanddate.com/weather/?continent=africa&sort=1&low=4")
    print("Retrieving weather data for Africa...")
    #use extend to add the results to the weather_data list
    weather_data.extend(get_weather_data(driver, "Africa"))
    print("Weather data for Africa retrieved successfully.")
    time.sleep(random.randint(5, 7))  # Random sleep to mimic human behavior
    driver.get("https://www.timeanddate.com/weather/?continent=europe&sort=1&low=4")
    print("Retrieving weather data for Europe...")
    weather_data.extend(get_weather_data(driver, "Europe"))
    print("Weather data for Europe retrieved successfully.")
    time.sleep(random.randint(5, 7))  # Random sleep to mimic human behavior
    driver.get("https://www.timeanddate.com/weather/?continent=namerica&sort=1&low=4")
    print("Retrieving weather data for North America...")
    weather_data.extend(get_weather_data(driver, "North America"))
    print("Weather data for North America retrieved successfully.")
    time.sleep(random.randint(5, 7))  # Random sleep to mimic human behavior
    driver.get("https://www.timeanddate.com/weather/?continent=samerica&sort=1&low=4")
    print("Retrieving weather data for South America...")       
    weather_data.extend(get_weather_data(driver, "South America"))
    print("Weather data for South America retrieved successfully.")

except Exception as e:
    print('An error occurred while retrieving data:', e)
finally:
    driver.quit()


#save it to csv files
try:
    #write to CSV
    # Save extracted data to a CSV file
    with open('weather_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Country", "City", "Time", "Weather", "Continent"])
        for result in weather_data:
            writer.writerow([result["Country"], result["City"], result["Time"], result["Weather"], result["Continent"]])
        print("Weather data saved to weather_data.csv successfully.")
except Exception as e:
    print('An error occurred while saving data to CSV:', e)
