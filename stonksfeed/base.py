import pytz
import requests
from datetime import datetime

from bs4 import BeautifulSoup
from dateutil import parser


class Article:
    def __init__(
        self, publisher, feed_title, headline, link, pubdate, source_type, author=None
    ):
        self.publisher = publisher
        self.feed_title = feed_title
        self.headline = headline
        self.link = link
        self.pubdate = pubdate
        self.author = author
        self.source_type = source_type

    def __repr__(self):
        return f"Article(headline='{self.headline[0:25]}' publisher={self.publisher})"

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

    def convert_pubdate_to_epoch(self, pubdate_string):
        dt_object = parser.parse(pubdate_string)
        epoch_time = int(dt_object.timestamp())
        return epoch_time


class RSSReader(BaseReader):
    def __init__(self, publisher, feed_title, rss_url):
        super().__init__(publisher, feed_title, rss_url)
        self.source_type = "rss"

    def get_articles(self):
        feed = self._fetch_content()
        soup = self.soup(feed, features=self.parser)
        articles = []

        for item in soup.find_all("item"):
            publisher = self.author
            feed_title = self.title
            headline = item.find("title").text
            author = item.find("author").text if item.find("author") else ""
            link = item.find("link").next_sibling.replace("\n", "").replace("\t", "")
            pubdate = self.convert_pubdate_to_epoch(item.find("pubdate").text)
            source_type = self.source_type

            article = Article(
                publisher, feed_title, headline, link, pubdate, source_type, author=author
            )
            articles.append(article)

        return articles
