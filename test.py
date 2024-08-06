import requests
token = "0148867a37d666e0e9d1202823b800fc"
lat = "13.7563"
lon = "100.5018"
url = "http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}".format(lat,lon,token)

res = requests.get(url)
rescode = res.status_code 
print(rescode)

res_dict = res.json()
print(res_dict)