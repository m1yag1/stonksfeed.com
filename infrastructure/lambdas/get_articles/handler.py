"""
Lambda handler for fetching articles from DynamoDB.

Returns articles sorted by pubdate (newest first).
"""

import json
import logging
import os
from decimal import Decimal
from typing import Any

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ.get("DYNAMODB_TABLE")
ORIGIN_VERIFY_HEADER = os.environ.get("ORIGIN_VERIFY_HEADER", "x-origin-verify")
ORIGIN_VERIFY_SECRET = os.environ.get("ORIGIN_VERIFY_SECRET")

# Use resource for easier querying with conditions
dynamodb = boto3.resource("dynamodb")


class DecimalEncoder(json.JSONEncoder):
    """JSON encoder that handles Decimal types from DynamoDB."""

    def default(self, o: Any) -> Any:
        if isinstance(o, Decimal):
            return int(o) if o % 1 == 0 else float(o)
        return super().default(o)


def get_articles(table_name: str, limit: int = 100) -> list[dict]:
    """
    Fetch articles from DynamoDB, sorted by pubdate descending.

    Since DynamoDB doesn't support sorting across partitions easily,
    we scan and sort in memory. For a small dataset this is fine.
    For larger datasets, consider a GSI with a fixed partition key.
    """
    table = dynamodb.Table(table_name)

    # Scan all items (for small datasets)
    response = table.scan(Limit=1000)  # Cap at 1000 to prevent runaway scans
    items = response.get("Items", [])

    # Handle pagination if needed
    while "LastEvaluatedKey" in response and len(items) < 1000:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    # Sort by pubdate descending (newest first)
    items.sort(key=lambda x: x.get("pubdate", 0), reverse=True)

    # Return requested limit
    return items[:limit]


def lambda_handler(event: dict, _context: Any) -> dict:
    """
    Handle API Gateway request for articles.

    Validates origin header and returns articles as JSON.
    """
    # Validate secret header
    headers = event.get("headers", {}) or {}
    # Headers are lowercase in API Gateway HTTP API
    origin_header = headers.get(ORIGIN_VERIFY_HEADER.lower())

    if ORIGIN_VERIFY_SECRET and origin_header != ORIGIN_VERIFY_SECRET:
        logger.warning("Invalid or missing origin verify header")
        return {
            "statusCode": 403,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Forbidden"}),
        }

    if not TABLE_NAME:
        logger.error("DYNAMODB_TABLE environment variable not set")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Configuration error"}),
        }

    # Parse query parameters
    query_params = event.get("queryStringParameters", {}) or {}
    limit = min(int(query_params.get("limit", 100)), 500)  # Cap at 500

    try:
        articles = get_articles(TABLE_NAME, limit=limit)
        logger.info(f"Returning {len(articles)} articles")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Cache-Control": "public, max-age=300",  # 5 minute cache
            },
            "body": json.dumps({"articles": articles}, cls=DecimalEncoder),
        }

    except Exception as e:
        logger.error(f"Error fetching articles: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
