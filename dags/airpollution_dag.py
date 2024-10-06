from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG
import pandas as pd
import requests
import os


# ฟังก์ชันสำหรับดึงข้อมูลจาก API
def call_api():
    token = "0148867a37d666e0e9d1202823b800fc"
    lat = "13.7563"
    lon = "100.5018"
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={token}"

    os.makedirs("/home/airflow/data", exist_ok=True)

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        raise Exception("API error! : {}".format(e))

    data_path = "/home/airflow/data/air_pollution_data.csv"
    df = pd.json_normalize(data["list"])
    df["DateTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.drop(columns="dt", inplace=True)

    # ถ้ามีไฟล์อยู่แล้ว อ่านไฟล์เดิมและเพิ่มข้อมูลใหม่
    if os.path.exists(data_path):
        existing_df = pd.read_csv(data_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        updated_df = df

    updated_df.to_csv(data_path, index=False)


# ฟังก์ชันสำหรับจัดการข้อมูล
def manipulate_data():
    data_path = "/home/airflow/data/air_pollution_data.csv"
    result_path = "/home/airflow/data/result.csv"

    df = pd.read_csv(data_path)

    # กำหนดคอลัมน์ใหม่
    new_name = {
        "main.aqi": "AQI",
        "components.co": "CO",
        "components.no": "NO",
        "components.no2": "NO2",
        "components.o3": "O3",
        "components.so2": "SO2",
        "components.pm2_5": "PM2.5",
        "components.pm10": "PM10",
        "components.nh3": "NH3",
    }
    df_new = df.rename(columns=new_name)
    df_new.dropna(inplace=True)

    df_new.to_csv(result_path, index=False)


default_args = {
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "airpollution",
    default_args=default_args,
    description="DAG to run air pollution flow",
    schedule_interval=timedelta(hours=1),  # Runs daily
    start_date=datetime(2024, 10, 6),
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="fetch_and_save_air_pollution_data", python_callable=call_api
    )
    t2 = PythonOperator(task_id="save_data_task", python_callable=manipulate_data)

    t1 >> t2
