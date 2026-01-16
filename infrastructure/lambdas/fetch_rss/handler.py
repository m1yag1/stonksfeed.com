"""
Lambda handler for fetching RSS feeds and storing articles in DynamoDB.
"""

import os

import boto3

from stonksfeed.rss.marketwatch import (
    mw_bulletins_rss_reader,
    mw_realtime_rss_reader,
)

dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = os.environ.get("DYNAMODB_TABLE")


def insert_item(client, table_name: str, item: dict) -> bool:
    """Insert an article item into DynamoDB."""
    client.put_item(TableName=table_name, Item=item)
    return True


def lambda_handler(event, context):
    """
    Fetch articles from RSS feeds and store in DynamoDB.

    :param event: Lambda event (not used)
    :param context: Lambda context
    :return: Response with status code and message
    """
    mw_bulletins_articles = [
        article.asdict() for article in mw_bulletins_rss_reader.get_articles()
    ]
    mw_realtime_articles = [
        article.asdict() for article in mw_realtime_rss_reader.get_articles()
    ]

    articles = mw_bulletins_articles + mw_realtime_articles

    inserted_count = 0
    for article in articles:
        article_item = {
            "headline": {"S": article["headline"]},
            "pubdate": {"N": str(article["pubdate"])},
            "feed_title": {"S": article["feed_title"]},
            "link": {"S": article["link"]},
            "source_type": {"S": article["source_type"]},
            "author": {"S": article["author"] if article["author"] else ""},
            "publisher": {"S": article["publisher"]},
        }
        insert_item(dynamodb_client, TABLE_NAME, article_item)
        inserted_count += 1

    return {
        "statusCode": 200,
        "body": f"Successfully inserted {inserted_count} articles!",
    }
