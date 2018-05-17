import requests
import csv
import datetime
import time

def Record_Curr_Weather(Latitude, Longitude):
    # api_string = 'http://api.openweathermap.org/data/2.5/weather?lat=' + str(Latitude) + '&lon=' + str(Longitude) + '&units=metric&APPID=cff8ba42de36c013f53acaa95cee63fc'
    # response = requests.get(api_string)
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Richmond,ca&units=metric&APPID=cff8ba42de36c013f53acaa95cee63fc')

    print (response.content)
    data = response.json()

    datestamp = datetime.datetime.now()

    # Temperature in C
    try:
        data["main"]["temp"]
    except KeyError:
        curr_temperature = 'NA'
    else:
        curr_temperature = data["main"]["temp"]

    # Air pressure
    try:
        data["main"]["pressure"]
    except KeyError:
        curr_pressure = 'NA'
    else:
        curr_pressure = data["main"]["pressure"]

    # Humidity
    try:
        data["main"]["humidity"]
    except KeyError:
        curr_humidity = 'NA'
    else:
        curr_humidity = data["main"]["humidity"]

    # Wind speed m/sec
    try:
        data["wind"]["speed"]
    except KeyError:
        curr_wind = 'NA'
    else:
        curr_wind = data["wind"]["speed"]

    # Wind direction degree
    try:
        data["wind"]["deg"]
    except KeyError:
        curr_wind_dir = 'NA'
    else:
        curr_wind_dir = data["wind"]["deg"]

    # Wind gust
    try:
        data["wind"]["gust"]
    except KeyError:
        curr_wind_gust = 'NA'
    else:
        curr_wind_gust = data["wind"]["gust"]

    # Clouds %
    try:
        data["clouds"]["all"]
    except KeyError:
        curr_clouds = 'NA'
    else:
        curr_clouds = data["clouds"]["all"]

    # Rain volume for last 3 hours
    try:
        data["rain"]["3h"]
    except KeyError:
        curr_rain3h = 'NA'
    else:
        curr_rain3h = data["rain"]["3h"]

    # Snow volume for last 3 hours
    try:
        data["snow"]["3h"]
    except KeyError:
        curr_snow3h = 'NA'
    else:
        curr_snow3h = data["snow"]["3h"]

    # Visibility m
    try:
        data["visibility"]
    except KeyError:
        curr_visibility = 'NA'
    else:
        curr_visibility = data["visibility"]

    # write to csv file
    if datetime.datetime.now().hour == 0 and datetime.datetime.now().minute == 0:
        fieldnames = ['Datestamp',
                      'Temperature',
                      'Preasure',
                      'Humidity',
                      'Wind_speed',
                      'Wind_dir',
                      'Wind_gust',
                      'Clouds',
                      'Rain',
                      'Snow',
                      'Visibility']
        with open(str(datetime.date.today()) + '.csv', 'a', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(fieldnames)
    fields = [datestamp,
              curr_temperature,
              curr_pressure,
              curr_humidity,
              curr_wind,
              curr_wind_dir,
              curr_wind_gust,
              curr_clouds,
              curr_rain3h,
              curr_snow3h,
              curr_visibility]
    with open(str(datetime.date.today()) + '.csv', 'a', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    print("Current weather at " + str(data["name"]) +", " + str(data["sys"]["country"]) + ":")
    print("Temperature: " + str(curr_temperature))
    print("Air pressure: " + str(curr_pressure) + " hPa")
    print("Humidity: " + str(curr_humidity) + " %")
    print("Wind: " + str(curr_wind) + " m/s, direction: " + str(curr_wind_dir) + " gust: " + str(curr_wind_gust))
    print("Clouds: " + str(curr_clouds) + "%")
    print("Precipitation: " + "Rain: " + str(curr_rain3h) + ", Snow: " + str(curr_snow3h))
    print("Visibility: " + str(curr_visibility) + " m")

while True:
    Record_Curr_Weather(49.1868035,-122.8519766) # Port Mann
    time.sleep(60)

