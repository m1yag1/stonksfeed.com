import os
import requests

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


class Article:
    def __init__(self, publisher, feed_name, headline, link, pubdate):
        self.publisher = publisher
        self.feed_name = feed_name
        self.headline = headline
        self.link = link
        self.pubdate = pubdate

    def __repr__(self):
        return f"Article(headline='{self.headline}')"

    def asdict(self):
        return self.__dict__


class RSSReader:
    def __init__(self, publisher, name, rss_url):
        self.publisher = publisher
        self.name = name
        self.rss_url = rss_url

    def _get_feed(self):
        return requests.get(self.rss_url).content

    def get_articles(self):
        feed = self._get_feed()
        soup = BeautifulSoup(feed, features="xml")
        articles = []

        for item in soup.find_all("item"):
            publisher = self.publisher
            feed_name = self.name
            headline = item.find("title").text
            link = item.find("link").text
            pubdate = item.find("pubDate")
            article = Article(publisher, feed_name, headline, link, pubdate)
            articles.append(article)

        return articles


def build_site(build_path, template_path):
    jinja_env = Environment(loader=FileSystemLoader([template_path]), autoescape=True)

    mw_bulletins_rss_reader = RSSReader(
        publisher="Marketwatch",
        name="Breaking News Bulletin",
        rss_url="https://feeds.content.dowjones.io/public/rss/mw_bulletins",
    )

    mw_realtime_rss_reader = RSSReader(
        publisher="Marketwatch",
        name="Real-time Headlines",
        rss_url="https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines"
    )

    mw_bulletin_articles = mw_bulletins_rss_reader.get_articles()
    mw_realtime_articles = mw_realtime_rss_reader.get_articles()

    articles = mw_bulletin_articles + mw_realtime_articles

    with open(os.path.join(build_path, "index.html"), "w") as outfile:
        template = jinja_env.get_template("index.html")
        rendered_template = template.render(articles=articles)
        outfile.write(rendered_template)


if __name__ == "__main__":
    site_path = os.getcwd()
    template_path = os.path.join(site_path, "templates")
    build_path = os.path.join(site_path, "_build")

    build_site(build_path, template_path)
