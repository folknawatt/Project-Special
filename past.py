import requests
import datetime
import pandas as pd

def air_pollution_data(token, lat, lon, start, end):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Data retrieved successfully.")
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None