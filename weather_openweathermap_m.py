import requests
import csv
import datetime
import time

while True:
    # Cities to get weather:
    # 6159905 Surrey, BC
    # 5911606 Burnaby, BC
    # 6111706 Coquitlam, BC
    # 6065686 Maple Ridge, BC
    # 6049429 Langley, BC
    # 6180961 Wight Rock, BC
    # 5937615 Delta, BC
    # 6122085 Richmond, BC
    # 6173331 Vancouver, BC
    response = requests.get('http://api.openweathermap.org/data/2.5/group?id=6159905,5911606,6111706,6065686,6049429,6180961,5937615,6122085,6173331&units=metric&APPID=cff8ba42de36c013f53acaa95cee63fc')


    print (response.content)
    data = response.json()
    print (data)
    # data1 = data[1]
    # print (data1)


    datestamp = datetime.datetime.now()

    i = 0


    # Temperature in C
    try:
        data['list'][i]['main']['temp']
    except KeyError:
        Temp = 'NA'
    else:
        Temp = data['list'][i]['main']['temp']

    print(Temp)

    # # Air pressure
    # try:
    #     data["main"]["pressure"]
    # except KeyError:
    #     curr_pressure = 'NA'
    # else:
    #     curr_pressure = data["main"]["pressure"]
    #
    # # Humidity
    # try:
    #     data["main"]["humidity"]
    # except KeyError:
    #     curr_humidity = 'NA'
    # else:
    #     curr_humidity = data["main"]["humidity"]
    #
    # # Wind speed m/sec
    # try:
    #     data["wind"]["speed"]
    # except KeyError:
    #     curr_wind = 'NA'
    # else:
    #     curr_wind = data["wind"]["speed"]
    #
    # # Wind direction degree
    # try:
    #     data["wind"]["deg"]
    # except KeyError:
    #     curr_wind_dir = 'NA'
    # else:
    #     curr_wind_dir = data["wind"]["deg"]
    #
    # # Wind gust
    # try:
    #     data["wind"]["gust"]
    # except KeyError:
    #     curr_wind_gust = 'NA'
    # else:
    #     curr_wind_gust = data["wind"]["gust"]
    #
    # # Clouds %
    # try:
    #     data["clouds"]["all"]
    # except KeyError:
    #     curr_clouds = 'NA'
    # else:
    #     curr_clouds = data["clouds"]["all"]
    #
    # # Rain volume for last 3 hours
    # try:
    #     data["rain"]["3h"]
    # except KeyError:
    #     curr_rain3h = 'NA'
    # else:
    #     curr_rain3h = data["rain"]["3h"]
    #
    # # Snow volume for last 3 hours
    # try:
    #     data["snow"]["3h"]
    # except KeyError:
    #     curr_snow3h = 'NA'
    # else:
    #     curr_snow3h = data["snow"]["3h"]
    #
    # # Visibility m
    # try:
    #     data["visibility"]
    # except KeyError:
    #     curr_visibility = 'NA'
    # else:
    #     curr_visibility = data["visibility"]
    #
    # # write to csv file
    # if datetime.datetime.now().hour == 0 and datetime.datetime.now().minute == 0:
    #     fieldnames = ['Datestamp',
    #                   'Temperature',
    #                   'Preasure',
    #                   'Humidity',
    #                   'Wind_speed',
    #                   'Wind_dir',
    #                   'Wind_gust',
    #                   'Clouds',
    #                   'Rain',
    #                   'Snow',
    #                   'Visibility']
    #     with open(str(datetime.date.today()) + '.csv', 'a', newline = '') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(fieldnames)
    # fields = [datestamp,
    #           curr_temperature,
    #           curr_pressure,
    #           curr_humidity,
    #           curr_wind,
    #           curr_wind_dir,
    #           curr_wind_gust,
    #           curr_clouds,
    #           curr_rain3h,
    #           curr_snow3h,
    #           curr_visibility]
    # with open(str(datetime.date.today()) + '.csv', 'a', newline = '') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(fields)



    time.sleep(60)

