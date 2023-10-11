import requests
from bs4 import BeautifulSoup
import csv

# List of URLs for the countries you want to scrape
data_sources = [
    {'url': 'https://www.weather.com/weather/today/l/New-York-NY-USNY0996:1:US', 'country': 'USA', 'location': 'New York'},
    {'url': 'https://www.weather.com/weather/today/l/Paris-FRXX0076:1:FR', 'country': 'France', 'location': 'Paris'},
    {'url': 'https://www.weather.com/weather/today/l/Toronto-CAQC0086:1:CA', 'country': 'Canada', 'location': 'Toronto'},
    {'url': 'https://www.weather.com/weather/today/l/Mumbai-INXX0096:1:IN', 'country': 'India', 'location': 'Mumbai'},
]

# Specific humidity values for each location
humidity_values = [50, 60, 40, 70]  # Adjust these values as needed

# Create a list to store weather data for each country
weather_data = []

# Loop through each URL and scrape data
for i, source in enumerate(data_sources):
    response = requests.get(source['url'])
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find temperature
        temperature_element = soup.find('span', class_='CurrentConditions--tempValue--MHmYY')
        temperature = temperature_element.get_text() if temperature_element else "N/A"

        # Use the corresponding humidity value from the list
        humidity = humidity_values[i]

        # Location
        location = source['location']

        weather_data.append({'Location': location, 'Country': source['country'], 'Temperature': temperature, 'Humidity': humidity})
    else:
        print(f"Failed to retrieve data from {source['url']}. Status code:", response.status_code)

# Create a CSV file to save the data
with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Location', 'Country', 'Temperature', 'Humidity']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row in the CSV file
    writer.writeheader()

    # Write the scraped data to the CSV file
    writer.writerows(weather_data)

print("Weather data has been scraped and saved to 'data.csv'.")
