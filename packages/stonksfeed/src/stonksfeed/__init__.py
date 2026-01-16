"""Stonksfeed - Stock news aggregator."""

from stonksfeed.models.article import Article
from stonksfeed.rss.rss_reader import RSSReader
from stonksfeed.web.siliconinvestor import SiliconInvestorPage

__all__ = ["Article", "RSSReader", "SiliconInvestorPage"]
__version__ = "0.1.0"
