from stonksfeed.base import RSSReader


wsj_tech_news_rss_reader = RSSReader(
    publisher="Wallstreet Journal",
    feed_title="Technology: What's News",
    rss_url="https://feeds.a.dj.com/rss/RSSWSJD.xml"
)
