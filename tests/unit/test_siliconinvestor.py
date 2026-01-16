from unittest.mock import Mock, patch

import pytest

from stonksfeed.web.siliconinvestor import SiliconInvestorPage


@pytest.mark.parametrize("content_data", ["siliconinvestor.html"], indirect=True)
def test_siliconinvestor_forum(content_data):
    si_forum_title = "AMD, ARMH, INTC, NVDA"
    forum_url = "https://www.siliconinvestor.com/subject.aspx?subjectid=58128"
    si_test_forum = SiliconInvestorPage(title=si_forum_title, url=forum_url)

    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.content = content_data

    with patch("stonksfeed.rss.base.requests.get", return_value=response_mock) as get_mock:
        articles = si_test_forum.get_articles()
        get_mock.assert_called_with(forum_url)

    article = articles[0].asdict()
    assert article["feed_title"] == si_forum_title
    assert article["headline"] == "Hey. It's all about percentages."
    assert (
        article["link"] == "http://www.siliconinvestor.com/readmsg.aspx?msgid=34589932"
    )
    assert article["source_type"] == "forum post"
