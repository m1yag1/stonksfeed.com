class Article:
    def __init__(
        self, publisher, feed_title, headline, link, pubdate, source_type, author=None
    ):
        self.publisher = publisher
        self.feed_title = feed_title
        self.headline = headline
        self.link = link
        self.pubdate = pubdate
        self.author = author
        self.source_type = source_type

    def __repr__(self):
        return (f"Article(headline='{self.headline[0:25]}' "
                f"publisher={self.publisher})")

    def asdict(self):
        return self.__dict__
