
from stonksfeed.models.article import Article
from stonksfeed.rss.base import BaseReader


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
            link = item.find("link").next_sibling.replace("\n", "").replace("\t", "").strip()
            pubdate = self.convert_pubdate_to_epoch(item.find("pubdate").text)
            source_type = self.source_type

            article = Article(
                publisher,
                feed_title,
                headline,
                link,
                pubdate,
                source_type,
                author=author,
            )
            articles.append(article)

        return articles
