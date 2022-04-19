import pandas as pd 
import json
import requests
import feedparser
import re
from pytrends.request import TrendReq


def get_trends(country):

    """
    Get hot topics for a specific country from 
    Google Trends API and save them as a dataframe
    """

    pytrend = TrendReq(timeout=(10,25))
    trends = pytrend.trending_searches(pn=country)
    trends.columns=['Topics']

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
        for trend in trends['Topics']:
            if trend.lower() in article['title'].lower():
                print(trend)
                print(f'{article["title"]}\n\n')
                top_news.append(article)
                break
    
    return top_news
            
