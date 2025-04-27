import time
import pandas as pd
import undetected_chromedriver as uc
import yfinance as yf

from pyfinviz.news import News
from trafilatura import extract


class WebScrape():
    def __init__(self):
        self.news = News()
        self.driver = self.setup_uc()

    # gets the url from pyfinviz, returns as a pd dataframe
    def get_finviz_urls(self) -> pd.DataFrame:
        url_df = pd.DataFrame(self.news.news_df["URL"])
        url_df.columns = ["URL"]
        return url_df

    def get_yfinance_url(self, ticker: str) -> pd.DataFrame:
        news_data = yf.Ticker(ticker)
        url_array = []

        for data in news_data.news:
            content = data["content"]
            url = content["clickThroughUrl"]

            if url is not None:
                url_array.append({"URL": url["url"]})

        return pd.DataFrame(url_array)

    # fetches text from a url, returns text as a list
    def get_text_from_url(self, url: str) -> str:
        self.driver.get(url)
        html = self.driver.page_source

        relevant_info = extract(html)
        return relevant_info

    # sets up the undetected chrome thing
    # makes it so that the window pops up for a sec real quick
    def setup_uc(self) -> uc.Chrome:
        opts = uc.ChromeOptions()
        opts.add_argument("--window-position=-32000,-32000")

        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument("--user-agent="
                          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0.0.0 Safari/537.36")
        driver = uc.Chrome(options=opts)
        return driver

    def close_window(self):
        self.driver.close()


# testing the method
if __name__ == "__main__":
    ws = WebScrape()
    df = ws.get_yfinance_url("AAPL")

    for row in df.itertuples(index=False):
        url = row.URL
        print(url)
        print(ws.get_text_from_url(url))
        # prevents ratelimit maybe
        time.sleep(0.1)

    # urls = ws.get_finviz_urls()
    #
    # for row in urls.itertuples(index=False):
    #     url = row.URL
    #     print(url)
    #     print(ws.get_text_from_url(url))
    #     # prevents ratelimit maybe
    #     time.sleep(0.1)
