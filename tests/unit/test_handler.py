"""Tests for the fetch_rss Lambda handler."""

import os
from unittest.mock import Mock, patch

import boto3
import pytest
from moto import mock_aws

# Import handler after setting up mocks
os.environ["DYNAMODB_TABLE"] = "test-articles-table"


@pytest.fixture
def dynamodb_table():
    """Create a mock DynamoDB table."""
    with mock_aws():
        dynamodb = boto3.client("dynamodb", region_name="us-east-1")
        dynamodb.create_table(
            TableName="test-articles-table",
            KeySchema=[
                {"AttributeName": "headline", "KeyType": "HASH"},
                {"AttributeName": "pubdate", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "headline", "AttributeType": "S"},
                {"AttributeName": "pubdate", "AttributeType": "N"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield dynamodb


@pytest.fixture
def mock_rss_response():
    """Mock RSS feed response."""
    return """
    <rss version="2.0">
    <channel>
        <title>Test Feed</title>
        <item>
            <title>Test Article</title>
            <link>https://example.com/article</link>
            <pubdate>Wed, 15 Jan 2025 10:00:00 GMT</pubdate>
        </item>
    </channel>
    </rss>
    """


@pytest.fixture
def mock_forum_response():
    """Mock Silicon Investor forum response."""
    return """
    <html>
    <body>
        <a href="readmsg.aspx?msgid=12345">Test Forum Post</a>
    </body>
    </html>
    """


def test_lambda_handler_inserts_articles(dynamodb_table, mock_rss_response, mock_forum_response):
    """Test that handler fetches and inserts articles."""
    from handler import lambda_handler

    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.raise_for_status = Mock()

    # Different responses for RSS vs forum
    def mock_get(url):
        mock = Mock()
        mock.raise_for_status = Mock()
        if "siliconinvestor" in url:
            mock.content = mock_forum_response.encode()
        else:
            mock.content = mock_rss_response.encode()
        return mock

    with patch("stonksfeed.rss.base.requests.get", side_effect=mock_get):
        with patch("handler.dynamodb_client", dynamodb_table):
            result = lambda_handler({}, {})

    assert result["statusCode"] == 200
    assert "Inserted" in result["body"]


def test_lambda_handler_skips_duplicates(dynamodb_table, mock_rss_response, mock_forum_response):
    """Test that handler skips duplicate articles."""
    from handler import lambda_handler

    def mock_get(url):
        mock = Mock()
        mock.raise_for_status = Mock()
        if "siliconinvestor" in url:
            mock.content = mock_forum_response.encode()
        else:
            mock.content = mock_rss_response.encode()
        return mock

    with patch("stonksfeed.rss.base.requests.get", side_effect=mock_get):
        with patch("handler.dynamodb_client", dynamodb_table):
            # First call inserts
            result1 = lambda_handler({}, {})
            # Second call should skip duplicates
            result2 = lambda_handler({}, {})

    assert result1["statusCode"] == 200
    assert result2["statusCode"] == 200
    assert "skipped" in result2["body"]


def test_lambda_handler_handles_missing_table_env():
    """Test that handler returns error if DYNAMODB_TABLE not set."""
    from handler import lambda_handler

    with patch.dict(os.environ, {"DYNAMODB_TABLE": ""}):
        # Need to reimport to pick up env change
        import importlib
        import handler
        importlib.reload(handler)

        result = handler.lambda_handler({}, {})

    assert result["statusCode"] == 500
    assert "DYNAMODB_TABLE" in result["body"]

    # Restore env for other tests
    os.environ["DYNAMODB_TABLE"] = "test-articles-table"
