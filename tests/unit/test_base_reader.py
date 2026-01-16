import pytest

from stonksfeed.rss.base import BaseReader


def test_base_reader():
    publisher = "foo"
    title = "foo-feed"
    url = "https://foo.com/feed"

    foo_reader = BaseReader(publisher=publisher, title=title, url=url)

    with pytest.raises(NotImplementedError):
        foo_reader.get_articles()
