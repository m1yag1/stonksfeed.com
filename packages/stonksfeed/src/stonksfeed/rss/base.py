"""Base reader class for fetching and parsing content."""

import requests
from bs4 import BeautifulSoup
from dateutil import parser


class BaseReader:
    """Base class for content readers (RSS feeds, web scrapers)."""

    def __init__(self, publisher: str, title: str, url: str, parser_type: str = "html.parser"):
        """
        Initialize the reader.

        :param publisher: Name of the content publisher
        :param title: Title/name of the feed or page
        :param url: URL to fetch content from
        :param parser_type: BeautifulSoup parser to use
        """
        self.author = publisher
        self.title = title
        self.url = url
        self.parser = parser_type
        self.soup = BeautifulSoup
        self._raw_content: bytes | None = None

    def _fetch_content(self) -> bytes:
        """Fetch content from the URL."""
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()
        self._raw_content = response.content
        return self._raw_content

    def get_articles(self) -> list:
        """
        Get articles from the source.

        Override this method in subclasses.
        """
        raise NotImplementedError("Subclasses must implement get_articles()")

    def convert_pubdate_to_epoch(self, pubdate_string: str) -> int:
        """Convert a date string to Unix epoch timestamp."""
        dt_object = parser.parse(pubdate_string)
        return int(dt_object.timestamp())
