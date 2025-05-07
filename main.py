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

    score = 0.0
    counts = {}    

    for row in urls.itertuples(index=False):
        content = webscraper.get_text_from_url(row.URL)
        results = pipe(content)     
        score, counts = calculate_score(results, score, counts)

    # final report
    print(f"Final score: {score:.2f}")
    print("Counts:", counts)

    webscraper.close_window()

def calculate_score(results, score, counts):
    """
    results: list of dicts, each {'label': str, 'score': float}
    score:   running float total
    counts:  dict to accumulate label counts
    """
    for res in results:
        # the pipeline gives e.g. 'POSITIVE'
        label = res["label"].upper()

        # initialize count for this label if needed
        counts.setdefault(label, 0)
        counts[label] += 1

        # match against the uppercase labels
        if   label == "POSITIVE":
            score += 0.1
        elif label == "NEGATIVE":
            score -= 0.1        # neutral: no change

    return score, counts

    

# test for ticker based data
ticker_data("NVDA")