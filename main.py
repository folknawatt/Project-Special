# from utils import air_pollution_data, update_air_pollution_data
from utils import air_pollution_data
# ข้อมูลการเข้าถึง API ในที่นี้ใช้ latitude = 13.7563, longitude = 100.5018 ของประเทศไทย
token = "0148867a37d666e0e9d1202823b800fc"
lat = "13.7563"
lon = "100.5018"


# Usage Example
data = air_pollution_data(token, lat, lon)
print(data)