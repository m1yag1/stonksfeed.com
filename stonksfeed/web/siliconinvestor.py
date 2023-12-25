from stonksfeed.base import Article, BaseReader


class SiliconInvestorPage(BaseReader):
    def __init__(self, title, url):
        self.root_url = "http://www.siliconinvestor.com/"
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
            # FIXME: No easy way to get pub_date using only requests ATM.
            pub_date = None
            article = Article(publisher, title, headline, link, pub_date)
            articles.append(article)

        return articles


si_ai_robotics_forum = SiliconInvestorPage(
    title="Artificial Intelligence, Robotics, Chat bots - ChatGPT",
    url="https://www.siliconinvestor.com/subject.aspx?subjectid=59856"
    )

si_amd_intel_nvda_forum = SiliconInvestorPage(
    title="AMD, ARMH, INTC, NVDA",
    url="https://www.siliconinvestor.com/subject.aspx?subjectid=58128"
)
