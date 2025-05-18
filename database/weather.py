import requests
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()


api_key = os.getenv('API_KEY')
MY_URL = os.getenv('MY_URL')

def get_weather(city):
    weather_info = []
    parameters = {
        'q': city,
        'appid': api_key,
        'cnt': 10
    }
    response = requests.get(MY_URL, params=parameters)
    weather_data = response.json()

    for day in weather_data['list']:
        day_info = {}

        # Extract date and convert from timestamp to human-readable format
        day_info['date'] = datetime.utcfromtimestamp(day['dt']).strftime('%Y-%m-%d')

        # Extract weather condition
        weather = day['weather'][0]
        day_info['weather_main'] = weather['main']
        day_info['weather_description'] = weather['description']
        day_info['weather_icon'] = weather['icon']

        # Extract temperatures
        temp = day['temp']
        day_info['day_temp'] = temp['day'] - 273.15  # Convert from Kelvin to Celsius
        day_info['night_temp'] = temp['night'] - 273.15
        day_info['eve_temp'] = temp['eve'] - 273.15
        day_info['morn_temp'] = temp['morn'] - 273.15
        day_info['min_temp'] = temp['min'] - 273.15
        day_info['max_temp'] = temp['max'] - 273.15

        # Extract feels-like temperatures
        feels_like = day['feels_like']
        day_info['feels_like_day'] = feels_like['day'] - 273.15
        day_info['feels_like_night'] = feels_like['night'] - 273.15
        day_info['feels_like_eve'] = feels_like['eve'] - 273.15
        day_info['feels_like_morn'] = feels_like['morn'] - 273.15

        # Extract atmospheric pressure and humidity
        day_info['pressure'] = day['pressure']
        day_info['humidity'] = day['humidity']

        # Extract wind speed, gust, and direction
        day_info['wind_speed'] = day['speed']
        day_info['wind_deg'] = day['deg']
        day_info['wind_gust'] = day['gust']

        # Extract cloudiness
        day_info['clouds'] = day['clouds']

        # Extract precipitation probability (pop)
        day_info['pop'] = day['pop']

        # Extract rain (if any)
        if 'rain' in day:
            day_info['rain'] = day['rain']
        else:
            day_info['rain'] = 0

        # Append the information for each day to the list
        weather_info.append(day_info)

    return weather_info
