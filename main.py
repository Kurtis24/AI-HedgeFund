from tools.webscrape import WebScrape
from transformers import pipeline

pipe = pipeline("text-classification", model="SeanD103/Longformer_for_financial_sentiment_analysis")

webscraper = WebScrape()

# sample usage of sentiment analysis of industry based news
def industry_data():
    urls = webscraper.get_finviz_urls()

    #  general industry based data
    for row in urls.itertuples(index=False):
        url = row.URL
        content = webscraper.get_text_from_url(url)

        result = pipe(content)
        print(result)

    webscraper.close_window()

# sample usage of sentiment analysis for ticker based news
def ticker_data(ticker):
    urls = webscraper.get_yfinance_url(ticker)

    for row in urls.itertuples(index=False):
        url = row.URL
        content = webscraper.get_text_from_url(url)

        result = pipe(content)
        print(result)

    webscraper.close_window()

# test for ticker based data
ticker_data("AAPL")