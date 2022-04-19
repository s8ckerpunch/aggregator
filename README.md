# News Aggregator

This project was made for collecting hot news.

## How To Launch

To set up this application on your own machine you just need to clone repo and then execute `docker-compose up -d --build` in its directory. 
After that wait a few minutes (maybe 2-3) and open `localhost:5000` to see a top new for the last couple of days. That's all. 

## Under The Hood

The whole system is quite simple. It requests most popular topics for a specific region (in this case - UA) from Google Trends and depending on them
it chooses news from some media RSS. Collected news goes to small Flask-app, which shows them in a table on routes `localhost:5000` and `localhost:5000/news`.

Data is refreshed every minute. Additional information you can find in comments in scripts.py

## Languages 

- Python
- Shell

## Technologies

 - Docker
 - Flask (Python framework)
 - Bootstrap5

 The list of all Python modules you can find in requirements.txt




