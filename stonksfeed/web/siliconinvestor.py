from datetime import datetime
import pytz
from stonksfeed.base import Article, BaseReader


class SiliconInvestorPage(BaseReader):
    def __init__(self, title, url):
        self.root_url = "http://www.siliconinvestor.com/"
        self.source_type = "forum post"
        super().__init__("Silicon Investor", title, url)

    def _build_link(self, partial):
        return f"{self.root_url}{partial}"

    def get_articles(self):
        page = self._fetch_content()
        soup = self.soup(page, features=self.parser)
        articles = []

        for item in soup.select("a[href*=readmsg]"):
            publisher = self.author
            title = self.title
            headline = item.text
            link = self._build_link(item["href"])
            # FIXME: No easy way to get pub_date so using current time.
            pubdate = self.get_current_epoch()
            article = Article(publisher, title, headline, link, pubdate, self.source_type)
            articles.append(article)

        return articles

    def get_current_epoch(self):
        # Get the current time with timezone information
        current_time = datetime.now(pytz.timezone("GMT"))
        return int(current_time.timestamp())



si_ai_robotics_forum = SiliconInvestorPage(
    title="Artificial Intelligence, Robotics, Chat bots - ChatGPT",
    url="https://www.siliconinvestor.com/subject.aspx?subjectid=59856"
    )

si_amd_intel_nvda_forum = SiliconInvestorPage(
    title="AMD, ARMH, INTC, NVDA",
    url="https://www.siliconinvestor.com/subject.aspx?subjectid=58128"
)
