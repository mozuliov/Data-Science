import requests
import json

#response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Richmond,ca&units=metric&APPID=cff8ba42de36c013f53acaa95cee63fc')
response = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=49.1865575&lon=-122.8518093&units=metric&APPID=cff8ba42de36c013f53acaa95cee63fc')
print (response.content)

data = response.json()

curr_temperature = data["main"]["temp"]
curr_pressure = data["main"]["pressure"]
curr_humidity = data["main"]["humidity"]
curr_wind = data["wind"]["speed"]
curr_wind_dir = data["wind"]["deg"]
curr_clouds = data["clouds"]["all"]
curr_visibility = data["visibility"]

print("Current weather at " + str(data["name"]) +", " + str(data["sys"]["country"]) + ":")
print("Temperature: " + str(curr_temperature))
print("Air pressure: " + str(curr_pressure) + " hPa")
print("Humidity: " + str(curr_humidity) + " %")
print("Wind: " + str(curr_wind) + " m/s, direction: " + str(curr_wind_dir))
print("Clouds: " + str(curr_clouds) + "%")
print("Visibility: " + str(curr_visibility) + " km")