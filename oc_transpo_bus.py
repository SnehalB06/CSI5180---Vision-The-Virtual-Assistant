import json
import re
import pandas as pd
import requests
from load_key_from_config import getConfigKey

baseAPIOCTranspo = "https://api.octranspo1.com/v2.0"

bus_keyword = ["bus", "bus timing", "bus from", "next bus"]

errorMessage = "Error occured while loading bus times, please try again"


# The query string to get bus schedules is passed here
def processBusRequest(text):
    # Use regular expressions with named groups to extract the locations
    pattern = r'from (?P<from_location>[\w\s]+) to (?P<to_location>[\w\s]+)'
    match = re.search(pattern, text)

    if match:
        from_station = match.group('from_location').lower()
        to_station = match.group('to_location').lower()
        return (getBusSchedule(from_station, to_station))

    elif 'route' in text:
        text = text.lower()
        pattern = r'route (\d+)'
        match = re.search(pattern, text)
        if match:
            df = pd.read_csv('Database/oc_transpo_stops.csv').set_index('Stations')
            for index, row in df.iterrows():
                if index in text:
                    stopNo = row['StopNo']
            route_number = match.group(1)

            return getBusTimes(stopNo, route_number)


# Source Station and Destination Station names are passed here and based on the available routes, the bus schedule is loaded
def getBusSchedule(source, destination):
    df = pd.read_csv('Database/oc_transpo_stops.csv').set_index('Stations')
    stopNo = df.loc[source, 'StopNo']

    apiKey = getConfigKey("ocTranspoAPI")
    appId = getConfigKey("ocTranspoAppId")

    ocTranspoAPI = f"{baseAPIOCTranspo}/GetRouteSummaryForStop?appID={appId}&apiKey={apiKey}&stopNo={stopNo}&format=JSON"

    response = requests.request("GET", ocTranspoAPI)

    if response.status_code == 200:
        data = json.loads(response.text)

        baseResult = ""

        for route in data['GetRouteSummaryForStopResult']['Routes']['Route']:
            if (destination in route['RouteHeading'].lower()):
                baseResult += getBusTimes(stopNo, route['RouteNo'])

        return baseResult
    else:
        return errorMessage


# This method takes in Source Station number and the route number as parameters and based on both these parameters, the bus
# Schedule is loaded
def getBusTimes(stopNo, routeNo):
    apiKey = getConfigKey("ocTranspoAPI")
    appId = getConfigKey("ocTranspoAppId")

    ocTranspoAPI = f"{baseAPIOCTranspo}/GetNextTripsForStop?appID={appId}&apiKey={apiKey}&stopNo={stopNo}&routeNo={routeNo}&format=JSON"
    response = requests.request("GET", ocTranspoAPI)
    if response.status_code == 200:
        data = json.loads(response.text)
        routeDetails = data['GetNextTripsForStopResult']['Route']['RouteDirection']
        response = f"RouteNo: {routeDetails['RouteNo']}\nRoute Label: {routeDetails['RouteLabel']}\n"
        for trip in routeDetails['Trips']['Trip']:
            response += f"Destination: {trip['TripDestination']}, StartTime: {trip['TripStartTime']}\n"
        return response
    else:
        return errorMessage

print(processBusRequest('what time does the route 97 bus leave Hurdman Station?'))

