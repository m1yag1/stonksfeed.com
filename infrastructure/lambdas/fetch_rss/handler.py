"""
Lambda handler for fetching RSS feeds and scraping forums,
then storing articles in DynamoDB.
"""

import logging
import os

import boto3
from botocore.exceptions import ClientError

from stonksfeed.config import RSS_FEEDS, SI_FORUMS
from stonksfeed.rss.rss_reader import RSSReader
from stonksfeed.web.siliconinvestor import SiliconInvestorPage

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = os.environ.get("DYNAMODB_TABLE")


def insert_item(client, table_name: str, item: dict) -> bool:
    """
    Insert an article item into DynamoDB.

    Uses a conditional expression to avoid overwriting existing items
    with the same headline and pubdate.
    """
    try:
        client.put_item(
            TableName=table_name,
            Item=item,
            ConditionExpression="attribute_not_exists(headline) AND attribute_not_exists(pubdate)",
        )
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            # Item already exists, skip
            return False
        raise


def fetch_rss_articles() -> list:
    """Fetch articles from all configured RSS feeds."""
    articles = []
    for feed_config in RSS_FEEDS:
        try:
            reader = RSSReader(
                publisher=feed_config["publisher"],
                feed_title=feed_config["feed_title"],
                rss_url=feed_config["rss_url"],
            )
            feed_articles = reader.get_articles()
            articles.extend(feed_articles)
            logger.info(
                f"Fetched {len(feed_articles)} articles from {feed_config['feed_title']}"
            )
        except Exception as e:
            logger.error(f"Error fetching {feed_config['feed_title']}: {e}")
    return articles


def fetch_forum_articles() -> list:
    """Fetch articles from Silicon Investor forums."""
    articles = []

    for forum_config in SI_FORUMS:
        try:
            scraper = SiliconInvestorPage(
                title=forum_config["title"],
                url=forum_config["url"],
            )
            forum_articles = scraper.get_articles()
            articles.extend(forum_articles)
            logger.info(f"Fetched {len(forum_articles)} posts from {forum_config['title']}")
        except Exception as e:
            logger.error(f"Error scraping {forum_config['title']}: {e}")
    return articles


def article_to_dynamodb_item(article: dict) -> dict:
    """Convert an article dict to DynamoDB item format."""
    return {
        "headline": {"S": article["headline"]},
        "pubdate": {"N": str(article["pubdate"])},
        "feed_title": {"S": article["feed_title"]},
        "link": {"S": article["link"]},
        "source_type": {"S": article["source_type"]},
        "author": {"S": article.get("author") or ""},
        "publisher": {"S": article["publisher"]},
    }


def lambda_handler(_event, _context):
    """
    Fetch articles from RSS feeds and forums, store in DynamoDB.

    :param event: Lambda event (not used)
    :param context: Lambda context
    :return: Response with status code and message
    """
    if not TABLE_NAME:
        logger.error("DYNAMODB_TABLE environment variable not set")
        return {
            "statusCode": 500,
            "body": "Configuration error: DYNAMODB_TABLE not set",
        }

    # Fetch from all sources
    rss_articles = fetch_rss_articles()
    forum_articles = fetch_forum_articles()
    all_articles = rss_articles + forum_articles

    logger.info(f"Total articles fetched: {len(all_articles)}")

    # Insert into DynamoDB
    inserted_count = 0
    skipped_count = 0

    for article in all_articles:
        article_dict = article.asdict()
        item = article_to_dynamodb_item(article_dict)

        if insert_item(dynamodb_client, TABLE_NAME, item):
            inserted_count += 1
        else:
            skipped_count += 1

    message = f"Inserted {inserted_count} new articles, skipped {skipped_count} duplicates"
    logger.info(message)

    return {
        "statusCode": 200,
        "body": message,
    }
