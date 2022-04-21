import pandas as pd 
import json
import requests
import feedparser
import re
import ast
from pytrends.request import TrendReq
from datetime import datetime, timedelta


def decode_response(response):
    
    """
    Decode response from API and convert it
    to the json
    """

    response = response.decode('unicode-escape').encode().decode('utf8')

    response = re.sub(r'("[\s\w]*)"([\s\w]*)"([\s\w]*")',  r'\1\2\3', response)

    response = re.sub('[\n]', '', response)

    response = response[5:]

    response = json.loads(response)

    return response


def get_trends(country):

    """
    Get hot topics for a specific country from 
    Google Trends API and save them as a dataframe
    """

    trends = []
    date_list = []

    for i in range(0,7):
        date = datetime.now() - timedelta(days=i)
        date = date.strftime('%Y%m%d')
        date_list.append(date)

    for date in date_list:

        print(date)

        response = requests.get(f'https://trends.google.com/trends/api/dailytrends?ed={date}&geo={country}')

        try:
            cleared_data = decode_response(response.content)
        except ValueError:
            print(f'Something wrong with JSON for date {date}')
            continue

        for item in  cleared_data['default']['trendingSearchesDays'][0]['trendingSearches']:
            trends.append(item['title']['query'])

    print(trends)

    return trends


def get_articles(source):

    """
    Parse an XML-source and pull from it each article
    in a dictionary format. Dictionary has next keys:
    {
         'title': 'Name of an article'
         'summary': 'Short description'
         'text': 'Full description'
         'link': 'Link to a source'
         'date': 'Date when the article was published'
    }
    """

    articles = []
    clean = re.compile('<[^<]+?>')

    feeds = feedparser.parse(source)['entries']
    for feed in feeds:
        article = dict(title=feed['title'], 
                       summary=feed['summary'], 
                       text=re.sub(clean, '', feed['content'][0]['value']),
                       link=feed['link'],
                       date=feed['published'].replace('+0300', ''))
        
        articles.append(article)

    return articles


def fetch_top_news(country, source):

    """
    Collect trends for specific country and also 
    get articles from a provided XML-source. Then filter articles
    by trend and choose only the top news
    """

    trends = get_trends(country)
    articles = get_articles(source)

    top_news = []

    for article in articles:
        for trend in trends:
            if trend.lower() in article['title'].lower():
                print(trend)
                print(f'{article["title"]}\n\n')
                top_news.append(article)
                break
    
    return top_news


