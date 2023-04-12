import json
from urllib import request
import requests
import pandas as pd

stock_keyword_list = ["stock", "trading", "stock price", "share price"]

def load_ticker(org_entity):
    mapping_df = pd.read_csv('Database/nasdaq_company_list.csv')
    ticker_symbol = mapping_df[mapping_df['Name'].str.contains(org_entity, case=False)]['Symbol'].values[0]
    return ticker_symbol


def getStocks(company_name):
    ticker = load_ticker(company_name)
    url = f"https://realstonks.p.rapidapi.com/{ticker}"

    headers = {
	    "X-RapidAPI-Key": "d1898a8e69msh518f9c5d0083e18p1af82ejsnbae3d87bc231",
	    "X-RapidAPI-Host": "realstonks.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:

        data = json.loads(response.text)
        # Extract the values of each constant
        stock = {
        "Company_name":company_name,
        "price" : data["price"],
        "change_point" : data["change_point"],
        "change_percentage" : data["change_percentage"],
        "total_vol" : data["total_vol"]
        }

        #details = f"Price of {ticker} is : {price}\nChange Point is : {change_point}\nChange Percentage is : {change_percentage}\nTotal Volume is : {total_vol}"

        return stock
    else:
        return "Error in loading stock details. Please try again."
