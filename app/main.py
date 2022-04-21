from flask import Blueprint, render_template, request, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from .scripts import fetch_top_news

main = Blueprint('main', __name__)

NEWS = []

def update_news():
    global NEWS 
    NEWS = fetch_top_news('UA', 'https://www.segodnya.ua/xml/rss')
    print(NEWS)

sched = BackgroundScheduler(daemon=True)
sched.add_job(update_news, 'interval',  minutes=1)
sched.start()

@main.route('/')
@main.route('/news')
def show_news():
    return  render_template('news.html', headings=['Trends', 'News', 'Summary', 'Text', 'Publication Date'], data=NEWS)




