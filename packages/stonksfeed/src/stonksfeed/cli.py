"""Command-line interface for stonksfeed."""

import argparse
import json
import sys
from typing import Optional

from stonksfeed.config import RSS_FEEDS, SI_FORUMS
from stonksfeed.rss.rss_reader import RSSReader
from stonksfeed.web.siliconinvestor import SiliconInvestorPage


def fetch_rss_articles() -> list[dict]:
    """Fetch articles from all configured RSS feeds."""
    articles = []
    for feed in RSS_FEEDS:
        try:
            reader = RSSReader(
                publisher=feed["publisher"],
                feed_title=feed["feed_title"],
                rss_url=feed["rss_url"],
            )
            feed_articles = reader.get_articles()
            articles.extend([a.asdict() for a in feed_articles])
            print(f"Fetched {len(feed_articles)} articles from {feed['feed_title']}")
        except Exception as e:
            print(f"Error fetching {feed['feed_title']}: {e}", file=sys.stderr)
    return articles


def fetch_forum_posts() -> list[dict]:
    """Fetch posts from all configured Silicon Investor forums."""
    articles = []
    for forum in SI_FORUMS:
        try:
            scraper = SiliconInvestorPage(
                title=forum["title"],
                url=forum["url"],
            )
            forum_articles = scraper.get_articles()
            articles.extend([a.asdict() for a in forum_articles])
            print(f"Fetched {len(forum_articles)} posts from {forum['title']}")
        except Exception as e:
            print(f"Error fetching {forum['title']}: {e}", file=sys.stderr)
    return articles


def main(args: Optional[list[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Stonksfeed - Stock news aggregator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--rss-only",
        action="store_true",
        help="Only fetch RSS feeds",
    )
    parser.add_argument(
        "--forums-only",
        action="store_true",
        help="Only fetch forum posts",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file (default: stdout)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )

    parsed = parser.parse_args(args)

    articles = []

    if not parsed.forums_only:
        articles.extend(fetch_rss_articles())

    if not parsed.rss_only:
        articles.extend(fetch_forum_posts())

    # Output results
    if parsed.format == "json":
        output = json.dumps(articles, indent=2)
    else:
        output = f"\nTotal articles fetched: {len(articles)}\n"
        for article in articles[:10]:  # Show first 10
            output += f"  - {article['headline'][:60]}... ({article['publisher']})\n"
        if len(articles) > 10:
            output += f"  ... and {len(articles) - 10} more\n"

    if parsed.output:
        with open(parsed.output, "w") as f:
            f.write(output)
        print(f"Output written to {parsed.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
