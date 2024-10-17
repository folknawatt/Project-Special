import pandas as pd
import requests
from datetime import datetime
import os
import pytz

def air_pollution_data(token, lat, lon):
    # token = "0148867a37d666e0e9d1202823b800fc"
    # lat = "4.7563"
    # lon = "100.5018"

    # os.makedirs("/home/airflow/data", exist_ok=True)
    os.makedirs("D:/Project-Special/data", exist_ok=True)
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={token}"

    try:
        res = requests.get(url)
        print(res)
        if res.status_code == 200:
            print("Data retrieved successfully.")
            data = res.json()
            print(data)
            print(data['list'])
            print("*"*50)
        else:
            raise Exception(f"API request failed with status code: {res.status_code}")
    except Exception as e:
        raise Exception(f"API error: {e}")

    df = pd.json_normalize(data['list'])
    print(df)

    new_name = {
        'main.aqi': 'AQI', 'components.co': 'CO', 'components.no': 'NO', 'components.no2': 'NO2',
        'components.o3': 'O3', 'components.so2': 'SO2', 'components.pm2_5': 'PM2.5',
        'components.pm10': 'PM10', 'components.nh3': 'NH3'
    }
    df_new = df.rename(columns=new_name)
    # ตั้งค่าโซนเวลาเป็น Thailand
    th_timezone = pytz.timezone('Asia/Bangkok')

    # ปรับโซนเวลาเป็นเวลาประเทศไทย
    df_new["DateTime"] = datetime.now(th_timezone).strftime("%Y-%m-%d %H:%M:%S")


    # df_new.drop(columns=['dt'], inplace=True)
    df_new.dropna(inplace=True)

    data_path = "D:/Project-Special/data/air_pollution_data.csv"  # ตรวจสอบว่าตำแหน่งนี้เข้าถึงได้

    # ตรวจสอบว่าไฟล์มีอยู่แล้วหรือไม่
    if os.path.exists(data_path):
        # ถ้ามีอยู่แล้ว อ่านไฟล์เดิมและเพิ่มข้อมูลใหม่
        existing_df = pd.read_csv(data_path)
        updated_df = pd.concat([existing_df, df_new], ignore_index=True)
    else:
        # ถ้ายังไม่มีไฟล์ ใช้ข้อมูลใหม่ทั้งหมด
        updated_df = df_new

    # บันทึกข้อมูลลง CSV โดยไม่ทับไฟล์เดิม
    updated_df.to_csv(data_path, index=False)
    print(f"Data saved successfully: '{data_path}'")


def update_air_pollution_data(token, lat, lon, csv_file='air_pollution_data.csv'):
    """
    Update air pollution data from OpenWeather API and save to CSV file.

    Parameters:
    token (str): API token for OpenWeather
    lat (str): Latitude of the location
    lon (str): Longitude of the location
    csv_file (str): Path to the CSV file to save the data
    """
    # Define the URL for the API request (ระบุ URL ของ API ที่จะใช้)
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={token}"

    # Make the API request (เรียกใช้ API)
    res = requests.get(url)

    # Check the status code of the response (ตรวจสอบสถานะของการร้องขอ)
    status_code = res.status_code

    if status_code == 200: # ถ้าสถานะเป็น 200
        # Extract data in JSON format (Extract ข้อมูลในรูปแบบ JSON)
        data = res.json()

        # Convert JSON data to a DataFrame (แปลงข้อมูล JSON เป็น DataFrame)
        df_new = pd.json_normalize(data['list'])

        # Add a DateTime column with the current time (เพิ่มคอลัมน์ DateTime ด้วยเวลาปัจจุบัน)
        df_new['DateTime'] = datetime.datetime.now()

        # Reorder columns to match the existing CSV file (จัดลําดับคอลัมน์ให้ตรงกับไฟล์ CSV ที่มีอยู่)
        columns = ['dt', 'main.aqi', 'components.co', 'components.no', 'components.no2', 'components.o3', 'components.so2', 'components.pm2_5', 'components.pm10', 'components.nh3', 'DateTime']
        df_new = df_new.reindex(columns=columns)

        # Rename columns for consistency (เปลี่ยนชื่อคอลัมน์ให้เหมือนกัน)
        df_new.columns = ['dt', 'AQI', 'CO', 'NO', 'NO2', 'O3', 'SO2', 'PM2.5', 'PM10', 'NH3', 'DateTime']

        # Load existing data if the CSV file exists (ถ้าไฟล์ CSV มีอยู่)
        if os.path.exists(csv_file):
            # Read existing data from the CSV file (อ่านข้อมูลจากไฟล์ CSV ที่มีอยู่)
            df_existing = pd.read_csv(csv_file)

            # Append new data to the existing data (เพิ่มข้อมูลใหม่เข้าไปในข้อมูลที่มีอยู่)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new

        # Save the combined DataFrame to a CSV file with headers (DataFrame ของข้อมูลใหม่ที่รวมกับข้อมูลเก่า save ไปในไฟล์ CSV: csv_file )
        df_combined.to_csv(csv_file, index=False)

        print("Data has been successfully updated in", csv_file)
    else:
        print(f"Failed to retrieve data. Status code: {status_code}")
