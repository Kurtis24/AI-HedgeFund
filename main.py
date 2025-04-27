from tools.webscrape import WebScrape
from transformers import pipeline

pipe = pipeline("text-classification", model="SeanD103/Longformer_for_financial_sentiment_analysis")

webscraper = WebScrape()
urls = webscraper.get_urls()

for row in urls.itertuples(index=False):
    url = row.URL
    content = webscraper.get_text_from_url(url)

    result = pipe(content)
    print(result)
