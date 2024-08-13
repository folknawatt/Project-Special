import pandas as pd
import requests
import datetime
import os

## ความเห็นจากกิว อยากให้โมดูลเขียน def แค่นี้น่าจะดีกว่า

def air_pollution_data(token, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Data retrieved successfully.")
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# def air_pollution_data(token: str, lat, lon):
#     url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={token}" #Current air pollution data

#     # Data Acquisition
#     res = requests.get(url)

#     # ตรวจสอบสถานะของการร้องขอ
#     if res.status_code == 200:
#         print("Data retrieved successfully.")
#         data = res.json()
#         print(data)
            
#         # Data Manipulation & Preparation
#         # แปลงข้อมูล JSON เป็น DataFrame
#         df = pd.json_normalize(data['list'])

#         # Data Cleansing
#         # ตรวจสอบค่า null หรือค่าที่ผิดปกติ
#         df.isnull().sum()
#         df.describe()

#         # แก้ไขชื่อคอลัมน์
#         new_name = {'main.aqi': 'AQI', 'components.co': 'CO', 'components.no': 'NO', 'components.no2': 'NO2', 'components.o3': 'O3', 'components.so2': 'SO2', 'components.pm2_5': 'PM2.5', 'components.pm10': 'PM10', 'components.nh3': 'NH3'}
#         df_new = df.rename(columns=new_name)
#         df_new['DateTime'] = datetime.datetime.now()
    
#         # ลบแถวที่มีค่า null
#         df_new.dropna(inplace=True)

#         # บันทึกข้อมูลลง CSV
#         csv_name = 'air_pollution_data.csv'
#         df_new.to_csv(csv_name, index=False)
#         print("Data saved successfully: '{}'".format(csv_name))
        
#     else:
#         print(f"Failed to retrieve data: {res.status_code}")

# def update_air_pollution_data(token, lat, lon, csv_file='air_pollution_data.csv'):
#     """
#     Update air pollution data from OpenWeather API and save to CSV file.

#     Parameters:
#     token (str): API token for OpenWeather
#     lat (str): Latitude of the location
#     lon (str): Longitude of the location
#     csv_file (str): Path to the CSV file to save the data
#     """
#     # Define the URL for the API request (ระบุ URL ของ API ที่จะใช้)
#     url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={token}"
    
#     # Make the API request (เรียกใช้ API)
#     res = requests.get(url)
    
#     # Check the status code of the response (ตรวจสอบสถานะของการร้องขอ)
#     status_code = res.status_code

#     if status_code == 200: # ถ้าสถานะเป็น 200
#         # Extract data in JSON format (Extract ข้อมูลในรูปแบบ JSON)
#         data = res.json()
        
#         # Convert JSON data to a DataFrame (แปลงข้อมูล JSON เป็น DataFrame)
#         df_new = pd.json_normalize(data['list'])
        
#         # Add a DateTime column with the current time (เพิ่มคอลัมน์ DateTime ด้วยเวลาปัจจุบัน)
#         df_new['DateTime'] = datetime.datetime.now()
        
#         # Reorder columns to match the existing CSV file (จัดลําดับคอลัมน์ให้ตรงกับไฟล์ CSV ที่มีอยู่)
#         columns = ['dt', 'main.aqi', 'components.co', 'components.no', 'components.no2', 'components.o3', 'components.so2', 'components.pm2_5', 'components.pm10', 'components.nh3', 'DateTime']
#         df_new = df_new.reindex(columns=columns)
        
#         # Rename columns for consistency (เปลี่ยนชื่อคอลัมน์ให้เหมือนกัน)
#         df_new.columns = ['dt', 'AQI', 'CO', 'NO', 'NO2', 'O3', 'SO2', 'PM2.5', 'PM10', 'NH3', 'DateTime']
        
#         # Load existing data if the CSV file exists (ถ้าไฟล์ CSV มีอยู่)
#         if os.path.exists(csv_file):
#             # Read existing data from the CSV file (อ่านข้อมูลจากไฟล์ CSV ที่มีอยู่)
#             df_existing = pd.read_csv(csv_file) 

#             # Append new data to the existing data (เพิ่มข้อมูลใหม่เข้าไปในข้อมูลที่มีอยู่)
#             df_combined = pd.concat([df_existing, df_new], ignore_index=True)
#         else:
#             df_combined = df_new
        
#         # Save the combined DataFrame to a CSV file with headers (DataFrame ของข้อมูลใหม่ที่รวมกับข้อมูลเก่า save ไปในไฟล์ CSV: csv_file )
#         df_combined.to_csv(csv_file, index=False)
        
#         print("Data has been successfully updated in", csv_file)
#     else:
#         print(f"Failed to retrieve data. Status code: {status_code}")