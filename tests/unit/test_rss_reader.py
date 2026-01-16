from unittest.mock import Mock, patch
from stonksfeed.models.article import Article
from stonksfeed.rss.rss_reader import RSSReader

_xml_content = """
<rss version="2.0">
<channel>
    <title>Foo Feed</title>
    <link>https://www.w3schools.com</link>
    <pubdate>2020-11-20</pubdate>
    <item>
    <title>Foo Article</title>
    <link>https://foo.com/article</link>
    <pubdate>2020-11-18</pubdate>
    </item>
</channel>
</rss>
"""


def test_rss_reader():
    rss_url = "https://foo.com/feed"
    feed_title = "foo-feed"
    publisher = "foo"

    foo_reader = RSSReader(
        publisher=publisher, feed_title=feed_title, rss_url=rss_url
    )

    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.content = _xml_content

    with patch("stonksfeed.rss.base.requests.get",
               return_value=response_mock) as get_mock:
        articles = foo_reader.get_articles()
        get_mock.assert_called_with(rss_url)

    assert isinstance(articles[0], Article)
    article = articles[0].asdict()

    assert article["source_type"] == "rss"
    assert article["publisher"] == publisher
    assert article["pubdate"] == 1605679200
    assert article["headline"] == "Foo Article"
    assert article["link"] == "https://foo.com/article"
    assert article["feed_title"] == "foo-feed"
    assert repr(articles[0]) == f"Article(headline='Foo Article' publisher={publisher})"
