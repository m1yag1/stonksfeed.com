"""Tests for Article model."""

from stonksfeed.models.article import Article


def test_article_creation():
    """Test creating an Article."""
    article = Article(
        publisher="Test Publisher",
        feed_title="Test Feed",
        headline="Test Headline",
        link="https://example.com/article",
        pubdate=1234567890,
        source_type="rss",
        author="Test Author",
    )

    assert article.publisher == "Test Publisher"
    assert article.feed_title == "Test Feed"
    assert article.headline == "Test Headline"
    assert article.link == "https://example.com/article"
    assert article.pubdate == 1234567890
    assert article.source_type == "rss"
    assert article.author == "Test Author"


def test_article_asdict():
    """Test Article.asdict() method."""
    article = Article(
        publisher="Test Publisher",
        feed_title="Test Feed",
        headline="Test Headline",
        link="https://example.com",
        pubdate=1234567890,
        source_type="rss",
    )

    result = article.asdict()

    assert isinstance(result, dict)
    assert result["publisher"] == "Test Publisher"
    assert result["headline"] == "Test Headline"
    assert result["author"] is None


def test_article_repr():
    """Test Article string representation."""
    article = Article(
        publisher="Test Publisher",
        feed_title="Test Feed",
        headline="This is a very long headline that should be truncated",
        link="https://example.com",
        pubdate=1234567890,
        source_type="rss",
    )

    repr_str = repr(article)

    assert "This is a very long headl" in repr_str
    assert "Test Publisher" in repr_str
