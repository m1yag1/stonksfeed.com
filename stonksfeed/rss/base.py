import requests
from bs4 import BeautifulSoup


class Article:
    def __init__(self, publisher, feed_title, headline, link, pubdate):
        self.publisher = publisher
        self.feed_title = feed_title
        self.headline = headline
        self.link = link
        self.pubdate = pubdate

    def __repr__(self):
        return f"Article(headline='{self.headline}')"

    def asdict(self):
        return self.__dict__


class RSSReader:
    def __init__(self, publisher, feed_title, rss_url):
        self.publisher = publisher
        self.feed_title = feed_title
        self.rss_url = rss_url

    def _get_feed(self):
        return requests.get(self.rss_url).content

    def get_articles(self):
        feed = self._get_feed()
        soup = BeautifulSoup(feed, features="xml")
        articles = []

        for item in soup.find_all("item"):
            publisher = self.publisher
            feed_title = self.feed_title
            headline = item.find("title").text
            link = item.find("link").text
            pubdate = item.find("pubDate")
            article = Article(publisher, feed_title, headline, link, pubdate)
            articles.append(article)

        return articles
