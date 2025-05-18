import requests
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY_NEWS = os.getenv('API_KEY_NEWS')
API_KEY_GNEWS = os.getenv('API_KEY_GNEWS')
API_KEY_NYTIMES = os.getenv('API_KEY_NYTIMES')
API_KEY_GUARDIAN = os.getenv('API_KEY_GUARDIAN')

def get_all_news():
    params = {
        'apiKey': API_KEY_NEWS,
        'language': 'en',
    }
    response = requests.get('https://newsapi.org/v2/top-headlines?',params=params)
    data = response.json()
    return data['articles']

def get_all_news_gnews():
    params = {
        'token': API_KEY_GNEWS,
        'lang': 'en',
    }

    response = requests.get('https://gnews.io/api/v4/top-headlines?',params=params)
    data = response.json()
    return data['articles']

def get_all_news_nytimes():
    params = {
        'api-key': API_KEY_NYTIMES
    }

    response = requests.get('https://api.nytimes.com/svc/topstories/v2/home.json?',params=params)
    data = response.json()
    return data['results']

def get_all_news_guardian():
    params = {
        'api-key': API_KEY_GUARDIAN,
        'show-fields': 'all',
        'page-size': 50
    }

    response = requests.get('https://content.guardianapis.com/search?',params=params)
    data = response.json()
    return data['response']['results']