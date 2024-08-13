from past import air_pollution_data
import datetime
import pandas as pd
token = "0148867a37d666e0e9d1202823b800fc"
lat = "13.7563"
lon = "100.5018"

# 30 วันย้อนหลัง
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=30)

start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

data = air_pollution_data(token, lat, lon, start_timestamp, end_timestamp)

# Process the data if retrieved
if data:
    data_list = []
    for entry in data.get('list', []):
        # แยกส่วนที่เกี่ยวข้องออกจากข้อมูล JSON
        record = {
            'date': datetime.datetime.fromtimestamp(entry['dt']),
            'aqi': entry['main']['aqi'],
            'co': entry['components'].get('co'),
            'no': entry['components'].get('no'),
            'no2': entry['components'].get('no2'),
            'o3': entry['components'].get('o3'),
            'so2': entry['components'].get('so2'),
            'pm2_5': entry['components'].get('pm2_5'),
            'pm10': entry['components'].get('pm10'),
            'nh3': entry['components'].get('nh3')
        }
        data_list.append(record)

    # Convert list to df
    df = pd.DataFrame(data_list)

    print(df)