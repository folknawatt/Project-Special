# from utils import air_pollution_data, update_air_pollution_data
from utils import air_pollution_data
# ข้อมูลการเข้าถึง API ในที่นี้ใช้ latitude = 13.7563, longitude = 100.5018 ของประเทศไทย

# Usage Example
# air_pollution_data(token, lat, lon)
air_pollution_data(
    token = "0148867a37d666e0e9d1202823b800fc",
    lat = "4.7563",
    lon = "100.5018")

# # อัพเดตข้อมูลใหม่เพิ่มเข้าไปในไฟล์เดิม
# update_air_pollution_data(token, lat, lon, csv_file='air_pollution_data.csv')
