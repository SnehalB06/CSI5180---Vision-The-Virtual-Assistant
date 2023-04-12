import requests
from load_key_from_config import getConfigKey

weather_keyword_list = ['weather', 'temperature', 'pressure', 'snow', 'humidity', 'cloud cover', 'climate']

def getWeather(city_name):

    # Enter your OpenWeatherMap API key
    api_key = getConfigKey('weatherAPI')

    # Enter the city name for which you want to fetch the weather info
    # city_name = input("Enter the city name: ")

    # Create the URL to fetch the weather information
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    # Make a GET request to the OpenWeatherMap API
    response = requests.get(url)

    # If the response code is 200 OK, then display the weather information
    if response.status_code == 200:
        data = response.json()
        a = "Temperature:"+ str(round(data['main']['temp'] - 273.15, 2))+ "°C"
        b = "Weather Description:"+ data['weather'][0]['description']
        c = "Wind Speed:"+ str(data['wind']['speed'])+ "m/s"

        result = a + "\n" + b + "\n" + c

        return result
        
    else:
        return "Error occurred while fetching weather info."