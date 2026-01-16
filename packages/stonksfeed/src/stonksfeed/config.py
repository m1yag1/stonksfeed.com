"""Configuration for RSS feeds and forum sources."""

# RSS feeds to fetch
RSS_FEEDS = [
    {
        "publisher": "Marketwatch",
        "feed_title": "Breaking News Bulletin",
        "rss_url": "https://feeds.content.dowjones.io/public/rss/mw_bulletins",
    },
    {
        "publisher": "Marketwatch",
        "feed_title": "Real-time Headlines",
        "rss_url": "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines",
    },
    {
        "publisher": "Wallstreet Journal",
        "feed_title": "Technology: What's News",
        "rss_url": "https://feeds.a.dj.com/rss/RSSWSJD.xml",
    },
]

# Silicon Investor forums to scrape
SI_FORUMS = [
    {
        "title": "Artificial Intelligence, Robotics, Chat bots - ChatGPT",
        "url": "https://www.siliconinvestor.com/subject.aspx?subjectid=59856",
    },
    {
        "title": "AMD, ARMH, INTC, NVDA",
        "url": "https://www.siliconinvestor.com/subject.aspx?subjectid=58128",
    },
]
