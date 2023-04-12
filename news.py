import json
import requests
from load_key_from_config import getConfigKey

newsAPIBaseURL = "https://bing-news-search1.p.rapidapi.com/news"

news_keywords_list = ['news', 'information', 'report', 'update', 'bulletin', 'headlines', 'gossip']
category_list = ['ScienceAndTechnology', 'business', 'entertainment', 'health', 'politics', 'products', 'scienceandtechnology', 'technology', 'science', 'sports', 'us', 'us_northeast', 'us_south', 'us_midwest', 'us_west', 'world', 'world_africa', 'world_americas', 'world_asia', 'world_europe', 'world_middleeast']


def geteHeader():
    headers = {
	    "X-BingApis-SDK": "true",
	    "X-RapidAPI-Key": getConfigKey("newsAPI"),
	    "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
    }
    return headers

def processTrendingRequest():
    url = f"{newsAPIBaseURL}/trendingtopics"
    querystring = {"textFormat":"Raw","safeSearch":"Off"}
    responseJSON = generateResponse(url, querystring, geteHeader())
    print(responseJSON)
    response = []
    for news in responseJSON['value']:
        response.append(news['query']['text'])
    return response

def processCategoryRequest(category):
    url = newsAPIBaseURL
    querystring = {"count":"5","category":category,"safeSearch":"Off","textFormat":"Raw"}
    responseJSON = generateResponse(url, querystring, geteHeader())
    response = []
    for news in responseJSON['value']:
        if '...' in news['name']:
            response.append(news['description'])
        else:
            response.append(news['name'])
    return response

def getNewsFromText(text):
    url = f"{newsAPIBaseURL}/search"
    querystring = {"q":text, "count":"5", "freshness":"Day","textFormat":"Raw","safeSearch":"Off"}
    responseJSON = generateResponse(url, querystring, geteHeader())
    response = []
    for news in responseJSON['value']:
        response.append(news['description'])
    if len(response) < 10:
        return "That News Query did not work, do you want to try something else?"
    else:
        return response


def processNewsRequest(text):
    text = text.lower()
    response = []
    if 'trending' in text:
        response = processTrendingRequest()

    elif 'category' in text:
        for topic in category_list:
            if topic in text:
                response = processCategoryRequest(topic)
    
    if len(response) < 10:
        response = getNewsFromText(text)

    return response
    

def generateResponse(url, querystring, headers):
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != 200:
        return "Error in loading news, please try again."
    responseJSON = json.loads(response.text)
    return responseJSON

processNewsRequest('trending')