"""Tests for configuration."""

from stonksfeed.config import RSS_FEEDS, SI_FORUMS


def test_rss_feeds_not_empty():
    """Test that RSS_FEEDS has entries."""
    assert len(RSS_FEEDS) > 0


def test_rss_feeds_have_required_fields():
    """Test that each RSS feed has required fields."""
    for feed in RSS_FEEDS:
        assert "publisher" in feed
        assert "feed_title" in feed
        assert "rss_url" in feed
        assert feed["rss_url"].startswith("http")


def test_si_forums_not_empty():
    """Test that SI_FORUMS has entries."""
    assert len(SI_FORUMS) > 0


def test_si_forums_have_required_fields():
    """Test that each forum has required fields."""
    for forum in SI_FORUMS:
        assert "title" in forum
        assert "url" in forum
        assert "siliconinvestor.com" in forum["url"]
