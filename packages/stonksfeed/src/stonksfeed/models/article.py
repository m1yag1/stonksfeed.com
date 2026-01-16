"""Article model for stonksfeed."""

from dataclasses import asdict, dataclass, field
from typing import List, Optional


@dataclass
class Article:
    """Represents a news article or forum post."""

    publisher: str
    feed_title: str
    headline: str
    link: str
    pubdate: int
    source_type: str
    author: Optional[str] = None
    # NLP enrichment fields
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    tickers: List[str] = field(default_factory=list)

    def asdict(self) -> dict:
        """Convert article to dictionary."""
        return asdict(self)

    def __repr__(self) -> str:
        return f"Article(headline='{self.headline[:25]}...' publisher={self.publisher})"
