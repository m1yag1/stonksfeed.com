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


class BaseReader:
    def __init__(self, author, title, url, parser="html.parser"):
        self.author = author
        self.title = title
        self.url = url
        self.parser = parser
        # BeautifulSoup is used parse the response
        self.soup = BeautifulSoup

    def _fetch_content(self):
        r = requests.get(self.url)
        r.raise_for_status()
        self._raw_content = r.content
        return self._raw_content

    def get_articles(self):
        # Overide this function depending on the use case
        raise NotImplementedError


class RSSReader(BaseReader):
    def __init__(self, publisher, feed_title, rss_url):
        super().__init__(publisher, feed_title, rss_url)

    def get_articles(self):
        feed = self._fetch_content()
        soup = self.soup(feed, features=self.parser)
        articles = []

        for item in soup.find_all("item"):
            publisher = self.author
            feed_title = self.title
            headline = item.find("title").text
            link = item.find("link").text
            pubdate = item.find("pubDate")
            article = Article(publisher, feed_title, headline, link, pubdate)
            articles.append(article)

        return articles
