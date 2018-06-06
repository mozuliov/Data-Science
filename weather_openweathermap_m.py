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
    data = response.json()
    print (data)

    record = []     # This list will contain data for the new line to write to csv file
    wind_dir = ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA']   # In case wind direction not available we will be using most recent available data

    record.append(datetime.datetime.now())        # date and time key of the record

    record.append(datetime.datetime.now().month)  # season (month)

    # Write down the part of the day as one of the feature:
    #  1 for sunrise to midpoint between sunrise and sunset interval
    #  2 for interval between midpoint and sunset
    #  3 for interval between sunset and midpoint between sunset and sunrise (same day for simplification)
    #  4 for interval between midpoint between sunset and sunrise and sunrise
    if (datetime.datetime.now().timestamp() - data['list'][0]['sys']['sunset']) > 0:        # after sunset
        day_quadrant = 3
        print ("After sunset")
    else:
        if (datetime.datetime.now().timestamp() - data['list'][0]['sys']['sunrise']) > 0:   # day
            if (datetime.datetime.now().timestamp() - ((data['list'][0]['sys']['sunset'] - data['list'][0]['sys']['sunrise']) / 2 + data['list'][0]['sys']['sunrise'])) > 0:
                day_quadrant = 2
            else:
                day_quadrant = 1
        else:                                                                   # before sunrise
            if (datetime.datetime.now().timestamp() - ((data['list'][0]['sys']['sunrise'] - (data['list'][0]['sys']['sunset'] - 86400)) / 2 + (data['list'][0]['sys']['sunset'] - 86400))) > 0:
                day_quadrant = 4
            else:
                day_quadrant = 3

    record.append(day_quadrant)

    for city in range(9):
        # Temperature in C
        try:
            data['list'][city]['main']['temp']
        except KeyError:
            record.append('NA')
        else:
            record.append(data['list'][city]['main']['temp'])

        # Air pressure
        try:
            data['list'][city]['main']['pressure']
        except KeyError:
            record.append('NA')
        else:
            record.append(data['list'][city]['main']['pressure'])

        # Humidity
        try:
            data['list'][city]['main']['humidity']
        except KeyError:
            record.append('NA')
        else:
            record.append(data['list'][city]['main']['humidity'])

        # Wind speed m/sec
        try:
            data['list'][city]['wind']['speed']
        except KeyError:
            record.append('NA')
        else:
            record.append(data['list'][city]['wind']['speed'])

        # Wind direction degree
        try:
            data['list'][city]['wind']['deg']
        except KeyError:
            record.append(wind_dir[city])
        else:
            if data['list'][city]['wind']['deg'] == "NA":
                record.append(wind_dir[city])
            else:
                record.append(data['list'][city]['wind']['deg'])
                wind_dir[city] = data['list'][city]['wind']['deg']

        # Wind gust considered here as an addition m/sec to wind speed
        try:
            data['list'][city]['wind']['gust']
        except KeyError:
            record.append(0)
        else:
            record.append(data['list'][city]['wind']['gust']-data['list'][city]['wind']['speed'])

        # Clouds %
        try:
            data['list'][city]['clouds']['all']
        except KeyError:
            record.append('NA')
        else:
            record.append(data['list'][city]['clouds']['all'])

        # Rain volume for last 3 hours
        try:
            data['list'][city]['rain']['3h']
        except KeyError:
            record.append('NA')
        else:
            record.append(data['list'][city]['rain']['3h'])

        # Snow volume for last 3 hours
        try:
            data['list'][city]['snow']['3h']
        except KeyError:
            record.append('NA')
        else:
             record.append(data['list'][city]['snow']['3h'])

    try:
        with open(str(datetime.date.today()) + '.csv', 'r') as f:
            with open(str(datetime.date.today()) + '.csv', 'a', newline = '') as f:
                writer = csv.writer(f)
                writer.writerow(record)
    except IOError as x:
        fieldnames = ['Datestamp', 'Month', 'Day_Quadrant',
                      '0_Temp', '0_Pressure', '0_Humidity', '0_Wind_Speed', '0_Wind_Dir', '0_Wind_Gust', '0_Clouds',
                      '0_Rain', '0_Snow',
                      '1_Temp', '1_Pressure', '1_Humidity', '1_Wind_Speed', '1_Wind_Dir', '1_Wind_Gust', '1_Clouds',
                      '1_Rain', '1_Snow',
                      '2_Temp', '2_Pressure', '2_Humidity', '2_Wind_Speed', '2_Wind_Dir', '2_Wind_Gust', '2_Clouds',
                      '2_Rain', '2_Snow',
                      '3_Temp', '3_Pressure', '3_Humidity', '3_Wind_Speed', '3_Wind_Dir', '3_Wind_Gust', '3_Clouds',
                      '3_Rain', '3_Snow',
                      '4_Temp', '4_Pressure', '4_Humidity', '4_Wind_Speed', '4_Wind_Dir', '4_Wind_Gust', '4_Clouds',
                      '4_Rain', '4_Snow',
                      '5_Temp', '5_Pressure', '5_Humidity', '5_Wind_Speed', '5_Wind_Dir', '5_Wind_Gust', '5_Clouds',
                      '5_Rain', '5_Snow',
                      '6_Temp', '6_Pressure', '6_Humidity', '6_Wind_Speed', '6_Wind_Dir', '6_Wind_Gust', '6_Clouds',
                      '6_Rain', '6_Snow',
                      '7_Temp', '7_Pressure', '7_Humidity', '7_Wind_Speed', '7_Wind_Dir', '7_Wind_Gust', '7_Clouds',
                      '7_Rain', '7_Snow',
                      '8_Temp', '8_Pressure', '8_Humidity', '8_Wind_Speed', '8_Wind_Dir', '8_Wind_Gust', '8_Clouds',
                      '8_Rain', '8_Snow']

        with open(str(datetime.date.today()) + '.csv', 'a', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(fieldnames)

    time.sleep(180)

