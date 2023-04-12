import json
from flask import Flask, render_template, request, jsonify, url_for,redirect,make_response
import os

from flask_cors import CORS
import requests
from datetime import datetime
#from googletrans import Translator, constants
import time
import openai
import gradio as gr
from load_key_from_config import getConfigKey
from ner_test import getNER
from weather import weather_keyword_list, getWeather
from stocks import stock_keyword_list, getStocks
from oc_transpo_bus import bus_keyword, processBusRequest
from news import news_keywords_list, processNewsRequest
from google_drive_load_file import summary_keywords, processSummaryRequest
import os
from io import BytesIO
from load_key_from_config import getConfigKey

import spacy
text = ""
#engine = pyttsx3.init()
nlp = spacy.load('en_core_web_sm')


app = Flask(__name__)
cors = CORS(app)

openai.api_key = getConfigKey("opanaiAPI")
messages = [{"role": "system", "content": "You are a virtual assistant chatbot. Your name is Vision. You will help users with general queries."}]

from pprint import pprint
#M7E7BMSVG2N5CJKNZ23E6Y8C8


def tempCelcius(temp):
    temp = (temp-32) * (5//9)
    return temp

@app.route('/weather', methods=['POST','GET'])
def getWeather1():
    city = 'Ottawa'
    if request.method == 'POST':
        city = request.form.get('city')
    d1 = '2023-04-05'
    d2 = '2023-04-05'
    url=f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{d1}/{d2}?key=M7E7BMSVG2N5CJKNZ23E6Y8C8'
    r = requests.get(url).json()
    print(url)
    print(r)
    current ={}
    now = datetime.now()
    print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%H:%M:%S")
    dt_time = str(now.strftime("%H")) + ":00:00"
    print(dt_time)
    print("date and time =", dt_string)
    time_N = r['days'][0]['hours']
    date_record = ''
    for dt in time_N:
        if dt['datetime'] == dt_time:
            date_record = dt
            break
    # print(date_record)
    # print(time_N)

    current = {
        'city': r['address'],
        'latitude': r['latitude'],
        'longitude': r['longitude'],
        'resolvedAddress': r['resolvedAddress'],
        'timezone': r['timezone'],
        'tempMax': int(tempCelcius(r['days'][0]['tempmax'])),
        'tempMin': int(tempCelcius(r['days'][0]['tempmin'])),
        'temperature': int(tempCelcius(date_record['temp'])),
        'feelslike': int(tempCelcius(date_record['feelslike'])),
        'humidity': date_record['humidity'],
        'dew': int(tempCelcius(date_record['temp'])),
        'precip': date_record['precip'],
        'precipprob': date_record['precipprob'],
        'snow': date_record['snow'],
        'snowdepth': tempCelcius(date_record['temp']),
        'preciptype': date_record['preciptype'],
        'windgust': date_record['windgust'],
        'windspeed': date_record['windspeed'],
        'pressure': date_record['pressure'],
        'visibility': date_record['visibility'],
        'cloudcover': date_record['cloudcover'],
        'uvindex': date_record['uvindex'],
        'sunrise': r['days'][0]['sunrise'],
        'sunset': r['days'][0]['sunset'],
        'conditions': date_record['conditions'],
        'icon': date_record['icon'],
        'conditions_all': r['days'][0]['conditions'],
        'description': r['days'][0]['description']
    }

    try:
        current_conditions = r['currentConditions']
        current = {
            'alertsEvent': r['alerts'][0]['event'],
            'alertsHeadline': r['alerts'][0]['headline'],
            'alertsDesc': r['alerts'][0]['description']
        }
        if current_conditions !=None:
            current = {
                'city': r['address'],
                'latitude': r['latitude'],
                'longitude': r['longitude'],
                'resolvedAddress': r['resolvedAddress'],
                'timezone': r['timezone'],
                'tempMax': int(tempCelcius(r['days'][0]['tempmax'])),
                'tempMin': int(tempCelcius(r['days'][0]['tempmin'])),
                'feelslike': int(tempCelcius(r['currentConditions']['feelslike'])),
                'humidity': r['currentConditions']['humidity'],
                'dew': int(tempCelcius(r['currentConditions']['dew'])),
                'precip': r['currentConditions']['precip'],
                'precipprob': r['currentConditions']['precipprob'],
                'snow': r['currentConditions']['snow'],
                'snowdepth': r['currentConditions']['snowdepth'],
                'preciptype': r['currentConditions']['preciptype'],
                'windgust': r['currentConditions']['windgust'],
                'windspeed': r['currentConditions']['windspeed'],
                'pressure': r['currentConditions']['pressure'],
                'visibility': r['currentConditions']['visibility'],
                'cloudcover': r['currentConditions']['cloudcover'],
                'uvindex': r['currentConditions']['uvindex'],
                'sunrise': r['currentConditions']['sunrise'],
                'sunset': r['currentConditions']['sunset'],
                'conditions': r['currentConditions']['conditions'],
                'icon': r['currentConditions']['icon'],
                'conditions_all': r['days'][0]['conditions'],
                'description': r['days'][0]['description'],
                'alertsEvent': r['alerts'][0]['event'],
                'alertsHeadline': r['alerts'][0]['headline'],
                'alertsDesc': r['alerts'][0]['description']
            }

    except:
        pass

    print(current)
    return  current
    #return render_template('weather.html',weather= current)


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
        weather = {
            "city":city_name,
            "Temperature":str(round(data['main']['temp'] - 273.15, 2)),
            "WeatherDescription" : data['weather'][0]['description'],
            "WindSpeed" : str(data['wind']['speed'])
        }
        '''a = "Temperature:" + str(round(data['main']['temp'] - 273.15, 2)) + "°C"
        b = "Weather Description:" + data['weather'][0]['description']
        c = "Wind Speed:" + str(data['wind']['speed']) + "m/s"

        result = a + "\n" + b + "\n" + c
        '''
        return weather

    else:
        return "Error occurred while fetching weather info."

def getWeatherData(city):
        current = {}
        now = datetime.now()
        print("now =", now)
        # dd/mm/YY H:M:S
        date = str(now.strftime("%Y-%m-%d"))
        dt_string = now.strftime("%H:%M:%S")
        dt_time = str(now.strftime("%H")) + ":00:00"
        print(dt_time)
        print("date and time =", dt_string)
        print(date)
        d1 = date
        d2 = date
        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{d1}/{d2}?key=M7E7BMSVG2N5CJKNZ23E6Y8C8'
        r = requests.get(url).json()
        print(url)
        print(r)


        time_N = r['days'][0]['hours']
        date_record = ''
        for dt in time_N:
            if dt['datetime'] == dt_time:
                date_record = dt
                break
        # print(date_record)
        # print(time_N)

        current = {
            'city': r['address'],
            'latitude': r['latitude'],
            'longitude': r['longitude'],
            'resolvedAddress': r['resolvedAddress'],
            'timezone': r['timezone'],
            'tempMax': int(tempCelcius(r['days'][0]['tempmax'])),
            'tempMin': int(tempCelcius(r['days'][0]['tempmin'])),
            'temperature': int(tempCelcius(date_record['temp'])),
            'feelslike': int(tempCelcius(date_record['feelslike'])),
            'humidity': date_record['humidity'],
            'dew': int(tempCelcius(date_record['temp'])),
            'precip': date_record['precip'],
            'precipprob': date_record['precipprob'],
            'snow': date_record['snow'],
            'snowdepth': tempCelcius(date_record['temp']),
            'preciptype': date_record['preciptype'],
            'windgust': date_record['windgust'],
            'windspeed': date_record['windspeed'],
            'pressure': date_record['pressure'],
            'visibility': date_record['visibility'],
            'cloudcover': date_record['cloudcover'],
            'uvindex': date_record['uvindex'],
            'sunrise': r['days'][0]['sunrise'],
            'sunset': r['days'][0]['sunset'],
            'conditions': date_record['conditions'],
            'icon': date_record['icon'],
            'conditions_all': r['days'][0]['conditions'],
            'description': r['days'][0]['description']
        }

        try:
            current_conditions = r['currentConditions']
            current = {
                'alertsEvent': r['alerts'][0]['event'],
                'alertsHeadline': r['alerts'][0]['headline'],
                'alertsDesc': r['alerts'][0]['description']
            }
            if current_conditions != None:
                current = {
                    'city': r['address'],
                    'latitude': r['latitude'],
                    'longitude': r['longitude'],
                    'resolvedAddress': r['resolvedAddress'],
                    'timezone': r['timezone'],
                    'tempMax': int(tempCelcius(r['days'][0]['tempmax'])),
                    'tempMin': int(tempCelcius(r['days'][0]['tempmin'])),
                    'feelslike': int(tempCelcius(r['currentConditions']['feelslike'])),
                    'humidity': r['currentConditions']['humidity'],
                    'dew': int(tempCelcius(r['currentConditions']['dew'])),
                    'precip': r['currentConditions']['precip'],
                    'precipprob': r['currentConditions']['precipprob'],
                    'snow': r['currentConditions']['snow'],
                    'snowdepth': r['currentConditions']['snowdepth'],
                    'preciptype': r['currentConditions']['preciptype'],
                    'windgust': r['currentConditions']['windgust'],
                    'windspeed': r['currentConditions']['windspeed'],
                    'pressure': r['currentConditions']['pressure'],
                    'visibility': r['currentConditions']['visibility'],
                    'cloudcover': r['currentConditions']['cloudcover'],
                    'uvindex': r['currentConditions']['uvindex'],
                    'sunrise': r['currentConditions']['sunrise'],
                    'sunset': r['currentConditions']['sunset'],
                    'conditions': r['currentConditions']['conditions'],
                    'icon': r['currentConditions']['icon'],
                    'conditions_all': r['days'][0]['conditions'],
                    'description': r['days'][0]['description'],
                    'alertsEvent': r['alerts'][0]['event'],
                    'alertsHeadline': r['alerts'][0]['headline'],
                    'alertsDesc': r['alerts'][0]['description']
                }

        except:
            pass

        print(current)
        return current

@app.route('/news', methods=['POST','GET'])
def news():
    translator = Translator()
    news_dict = {}
    news =[]
    url = "https://newsapi.org/v2/everything?q=tesla&from=2023-03-09&sortBy=publishedAt&apiKey=45f7ab3c7b1241b88021bf121166b87f"
    r = requests.get(url).json()
    #print(url)
    print(r)
    #print(r['articles'])
    total = r['totalResults']
    for i in range(0,10):
        x = {}
        title = translator.translate(r['articles'][i]['title']).text
        x['title'] = title
        description = translator.translate(r['articles'][i]['description']).text
        x['description'] = description
        url = translator.translate(r['articles'][i]['url']).text
        x['url'] = url
        source_name = r['articles'][i]['source']['name']
        author = r['articles'][i]['author']
        x['author'] = author
        x['source'] = source_name
        news_dict[x['title']] = x
        if i <10:
            news.append(x)
    #print(news)
    return render_template('news.html', news_obj=news)

@app.route('/stocks',methods=['POST','GET'])
def getStocks1():
    stocks = {}
    stock = []
    url = "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2023-01-09?adjusted=true&apiKey=BEVh584XY8ypg7_ZwnmO1VuGGa4GKNyF"
    r = requests.get(url).json()
    c = r['count']
    print(c)
    print(r)
    for i in range(0,c):
        x={}
        x['Title']  = r['results'][i]['T']
        x['open']  = r['results'][i]['o']
        x['close']  = r['results'][i]['c']
        x['high']  = r['results'][i]['h']
        x['low']  = r['results'][i]['l']
        #x['transaction']  = r['results'][i]['n']
        #print(x)
        stocks[x['Title']] = x
        if i<10:
            stock.append(x)
    print(stocks)
    #specific stock
    filtered_dict = {k: v for k, v in stocks.items() if 'DXGE' in k}
    print(filtered_dict)
    return render_template('stocks.html',stocks=stock)



@app.route('/back',methods=['POST'])
def about():
    data = json.loads(request.data)
    doc = nlp(data)
    response_data = {}

    user_input = data
    print(user_input)
    messages.append({"role": "user", "content": user_input})

    tokens = getNER(user_input)
    print(tokens)

    if any(word in user_input for word in weather_keyword_list):
        gpe_entities = [ent.text for ent in tokens if ent.label_ == 'GPE']
        print(gpe_entities)
        if gpe_entities:
            chat_response = getWeather(gpe_entities[0])
            print(chat_response)
            response_data = jsonify({'weather': chat_response, "weather_flag": 1})

    elif any(word in user_input for word in stock_keyword_list):
        org_entities = [ent.text for ent in tokens if ent.label_ == 'ORG']
        print(org_entities)
        if org_entities:
            chat_response = getStocks(org_entities[0])
            print(chat_response)
            response_data = jsonify({'stocks': chat_response, 'stock_flag': 1})


    elif any(word in user_input for word in bus_keyword):
        user_input = "what time does the route 97 bus leave Hurdman Station"
        chat_response = processBusRequest(user_input)
        print("c",chat_response)
        response_data = jsonify({'buses': chat_response, "bus_flag": 1})

    elif any(word in user_input for word in news_keywords_list):
        chat_response = processNewsRequest(user_input)
        print("chat",chat_response)
        response_data = jsonify({'news': [chat_response], "news_flag": 1})


    elif any(word in user_input for word in summary_keywords):
        chat_response = processSummaryRequest(user_input)

    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        chat_response = response["choices"][0]["message"]["content"]
        response_data = jsonify({'chat': [chat_response], "chat_flag": 1})

    messages.append({"role": "assistant", "content": chat_response})
    #return chat_response
    '''
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
        if ent.label_ == 'GPE' and 'weather' in data:
            print('weather in ',ent.text)
            r = getWeatherData(ent.text)
            print(r)
    '''
    resp = make_response(response_data, 201)
    return resp

@app.route('/')
def start():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

'''
 now = datetime.now()
 print("now =", now)
 # dd/mm/YY H:M:S
 dt_string = now.strftime("%H:%M:%S")
 dt_time = str(now.strftime("%H"))+ ":00:00"
 print(dt_time)
 print("date and time =", dt_string)
 time_N = r['days'][0]['hours']
 date_record = ''
 for dt in time_N:
     if dt['datetime'] == dt_time:
         date_record = dt
         break
 #print(date_record)
 #print(time_N)
 current_conditions = r['currentConditions']
 print(current_conditions)

 current_weather= {
     'city': r['address'],
     'latitude': r['latitude'],
     'longitude': r['longitude'],
     'resolvedAddress': r['resolvedAddress'],
     'timezone': r['timezone'],
     'tempMax': tempCelcius(r['days'][0]['tempmax']),
     'tempMin': tempCelcius(r['days'][0]['tempmin']),
     'temperatureCurrent': tempCelcius(date_record['temp']),
     'feelslikeCurrent': tempCelcius(date_record['feelslike']),
     'humidityCurrent': date_record['humidity'],
     'dewCurrent': tempCelcius(date_record['temp']),
     'precipCurrent': date_record['temp'],
     'precipprobCurrent': date_record['precipprob'],
     'snowCurrent': tempCelcius(date_record['temp']),
     'snowdepthCurrent': tempCelcius(date_record['temp']),
     'preciptypeCurrent': date_record['preciptype'],
     'windgustCurrent': date_record['windgust'],
     'windspeedCurrent': date_record['windspeed'],
     'pressureCurrent': date_record['pressure'],
     'visibilityCurrent': date_record['visibility'],
     'cloudcoverCurrent': date_record['cloudcover'],
     'uvindexCurrent': date_record['uvindex'],
     'severeriskCurrent': date_record['severerisk'],
     'conditionsCurrent': date_record['conditions'],
     'iconCurrent': date_record['icon']

 }

 weather_Details = {
     'city':r['address'],
     'latitude':r['latitude'],
     'longitude':r['longitude'],
     'resolvedAddress':r['resolvedAddress'],
     'timezone':r['timezone'],
     'tempMax': tempCelcius(r['days'][0]['tempmax']),
     'tempMin': tempCelcius(r['days'][0]['tempmin']),
     'realfeeltempMax': tempCelcius(r['days'][0]['feelslikemax']),
     'realfeeltempMin': tempCelcius(r['days'][0]['feelslikemin']),
     'feelslike': tempCelcius(r['days'][0]['feelslike']),
     'dew': tempCelcius(r['days'][0]['dew']),
     'humidity': r['days'][0]['humidity'],
     'precip': r['days'][0]['precip'],
     'preciptype': r['days'][0]['preciptype'],
     'snow': r['days'][0]['snow'],
     'snowdepth': r['days'][0]['snowdepth'],
     'windgust': r['days'][0]['windgust'],
     'windspeed': r['days'][0]['windspeed'],
     'pressure': r['days'][0]['pressure'],
     'visibility': r['days'][0]['visibility'],
     'cloudcover': r['days'][0]['cloudcover'],
     'uvindex': r['days'][0]['uvindex'],
     'sunrise': r['days'][0]['sunrise'],
     'sunset': r['days'][0]['sunset'],
     'conditions': r['days'][0]['conditions'],
     'description': r['days'][0]['description'],
     'alertsEevnt':r['alerts'][0]['event'],
     'alertsHeadline':r['alerts'][0]['headline'],
     'alertsDesc':r['alerts'][0]['description']

 }
 '''