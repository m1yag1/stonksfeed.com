from .base import RSSReader


mw_marketpulse_rss_reader = RSSReader(
        publisher="Marketwatch",
        feed_title="Market Pulse",
        rss_url="https://feeds.content.dowjones.io/public/rss/mw_marketpulse",
    )

mw_top_stories_rss_reader = RSSReader(
    publisher="Marketwatch",
    feed_title="Top Stories",
    rss_url="https://feeds.content.dowjones.io/public/rss/mw_topstories",
)

mw_bulletins_rss_reader = RSSReader(
    publisher="Marketwatch",
    feed_title="Breaking News Bulletin",
    rss_url="https://feeds.content.dowjones.io/public/rss/mw_bulletins",
)

mw_realtime_rss_reader = RSSReader(
    publisher="Marketwatch",
    feed_title="Real-time Headlines",
    rss_url="https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines",
)
