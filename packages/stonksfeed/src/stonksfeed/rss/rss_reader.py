"""RSS feed reader."""

from stonksfeed.models.article import Article
from stonksfeed.rss.base import BaseReader


class RSSReader(BaseReader):
    """Reader for RSS feeds."""

    def __init__(self, publisher: str, feed_title: str, rss_url: str):
        """
        Initialize the RSS reader.

        :param publisher: Name of the publisher
        :param feed_title: Title of the RSS feed
        :param rss_url: URL of the RSS feed
        """
        super().__init__(publisher, feed_title, rss_url)
        self.source_type = "rss"

    def get_articles(self) -> list[Article]:
        """Fetch and parse articles from the RSS feed."""
        feed = self._fetch_content()
        soup = self.soup(feed, features=self.parser)
        articles = []

        for item in soup.find_all("item"):
            publisher = self.author
            feed_title = self.title
            headline = item.find("title").text
            author = item.find("author").text if item.find("author") else ""

            # Link handling - some feeds have link as text, others as next sibling
            link_tag = item.find("link")
            if link_tag.string:
                link = link_tag.string.strip()
            elif link_tag.next_sibling:
                link = link_tag.next_sibling.replace("\n", "").replace("\t", "").strip()
            else:
                link = ""

            pubdate_tag = item.find("pubdate")
            pubdate = self.convert_pubdate_to_epoch(pubdate_tag.text) if pubdate_tag else 0

            article = Article(
                publisher=publisher,
                feed_title=feed_title,
                headline=headline,
                link=link,
                pubdate=pubdate,
                source_type=self.source_type,
                author=author,
            )
            articles.append(article)

        return articles
