from tools.webscrape import WebScrape
from transformers import pipeline

pipe = pipeline("sentiment-analysis", model="tabularisai/multilingual-sentiment-analysis")

webscraper = WebScrape()
urls = webscraper.get_urls()

for row in urls.itertuples(index=False):
    url = row.URL
    content = webscraper.get_text_from_url(url)

    result = pipe(content)
    print(result)
