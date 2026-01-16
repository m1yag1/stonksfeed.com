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
        "publisher": "Seeking Alpha",
        "feed_title": "Latest Articles",
        "rss_url": "https://seekingalpha.com/feed.xml",
    },
    {
        "publisher": "CNBC",
        "feed_title": "Markets",
        "rss_url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258",
    },
    {
        "publisher": "Investing.com",
        "feed_title": "News",
        "rss_url": "https://www.investing.com/rss/news.rss",
    },
    {
        "publisher": "Motley Fool",
        "feed_title": "Investing",
        "rss_url": "https://www.fool.com/feeds/index.aspx",
    },
    {
        "publisher": "BizToc",
        "feed_title": "Business News",
        "rss_url": "https://biztoc.com/feed",
    },
    {
        "publisher": "PR Newswire",
        "feed_title": "Financial Services",
        "rss_url": "https://www.prnewswire.com/rss/financial-services-latest-news/financial-services-latest-news-list.rss",
    },
    {
        "publisher": "GlobeNewswire",
        "feed_title": "Earnings",
        "rss_url": "https://globenewswire.com/RssFeed/subjectcode/13-Earnings/feedTitle/GlobeNewswire%20-%20Earnings",
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
