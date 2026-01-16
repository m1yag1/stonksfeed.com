import requests

from bs4 import BeautifulSoup
from dateutil import parser


class BaseReader:
    # FIXME: lxml should be used here but not easy to use in AWS lambda.
    def __init__(self, publisher, title, url, parser="html.parser"):
        self.author = publisher
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
