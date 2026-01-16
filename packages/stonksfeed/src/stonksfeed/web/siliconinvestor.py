"""Silicon Investor forum scraper."""

import re
from datetime import datetime
from typing import Optional

import pytz
import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from stonksfeed.models.article import Article
from stonksfeed.rss.base import BaseReader


class SiliconInvestorPage(BaseReader):
    """Scraper for Silicon Investor forum pages."""

    ROOT_URL = "http://www.siliconinvestor.com/"
    TIMEZONE = pytz.timezone("US/Pacific")

    def __init__(self, title: str, url: str):
        """
        Initialize the Silicon Investor scraper.

        :param title: Name of the forum/thread
        :param url: URL of the forum page
        """
        self.source_type = "forum post"
        super().__init__("Silicon Investor", title, url)

    def _build_link(self, partial: str) -> str:
        """Build full URL from partial path."""
        if partial.startswith("http"):
            return partial
        return f"{self.ROOT_URL}{partial}"

    def _extract_message_id(self, href: str) -> Optional[str]:
        """Extract message ID from href like 'readmsg.aspx?msgid=35394904'."""
        match = re.search(r"msgid=(\d+)", href)
        return match.group(1) if match else None

    def _fetch_post_date(self, post_url: str) -> Optional[int]:
        """
        Fetch the actual post date from an individual post page.

        The date location varies:
        - Original posts: date is next to "From:" row
        - Reply posts: date is next to "To:" row, "From:" row has message number

        :param post_url: URL of the individual post
        :return: Unix epoch timestamp or None if parsing fails
        """
        try:
            response = requests.get(post_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, features=self.parser)

            # Find the div containing the message content
            msg_div = soup.find("div", id="msgcontentDiv")
            if not msg_div:
                return None

            # Find the table inside the message div
            table = msg_div.find("table")
            if not table:
                return None

            # Look through rows for the date
            # Priority: "To:" row (for replies), then "From:" row (for original posts)
            date_text = None

            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) >= 2:
                    first_cell_text = cells[0].get_text(strip=True)

                    # For replies, the date is in the "To:" row
                    if first_cell_text.startswith("To:"):
                        candidate = cells[1].get_text(strip=True)
                        # Verify it looks like a date (contains / and numbers)
                        if "/" in candidate and any(c.isdigit() for c in candidate):
                            date_text = candidate
                            break

                    # For original posts, the date is in the "From:" row
                    # But only if it's not a message number (contains "of")
                    if first_cell_text.startswith("From:"):
                        candidate = cells[1].get_text(strip=True)
                        # Check if it looks like a date, not message number
                        if "/" in candidate and "of" not in candidate:
                            date_text = candidate
                            break

            if date_text:
                return self._parse_post_date(date_text)

            return None
        except (requests.RequestException, ValueError, AttributeError):
            return None

    def _parse_post_date(self, date_text: str) -> Optional[int]:
        """
        Parse a date string like "1/16/2026 10:29:34 AM" to epoch timestamp.

        :param date_text: The date string from the post page
        :return: Unix epoch timestamp or None if parsing fails
        """
        try:
            # Parse the date string (dateutil handles various formats)
            dt = date_parser.parse(date_text)
            # Localize to Pacific time if no timezone info
            if dt.tzinfo is None:
                dt = self.TIMEZONE.localize(dt)
            return int(dt.timestamp())
        except (ValueError, TypeError):
            return None

    def get_articles(self) -> list[Article]:
        """
        Fetch and parse forum posts from Silicon Investor.

        This method:
        1. Fetches the forum list page
        2. Extracts post links from the table
        3. Fetches each individual post page to get the accurate date
        """
        page = self._fetch_content()
        soup = self.soup(page, features=self.parser)
        articles = []
        seen_msg_ids = set()

        # Fallback timestamp if we can't get the real date
        now = datetime.now(self.TIMEZONE)
        fallback_timestamp = int(now.timestamp())

        # Find all rows in the message table
        for row in soup.find_all("tr", align="left"):
            cells = row.find_all("td")
            if len(cells) < 4:
                continue

            # Extract message link and headline (cell 2)
            msg_cell = cells[1]
            link_tag = msg_cell.find("a", href=re.compile(r"readmsg"))
            if not link_tag:
                continue

            href = str(link_tag.get("href", ""))
            msg_id = self._extract_message_id(href)

            # Skip duplicates within this page
            if msg_id and msg_id in seen_msg_ids:
                continue
            if msg_id:
                seen_msg_ids.add(msg_id)

            headline = link_tag.get_text(strip=True)
            if not headline:
                continue

            link = self._build_link(href)

            # Extract author (cell 3)
            author_cell = cells[2]
            author_tag = author_cell.find("a", href=re.compile(r"profile"))
            author = author_tag.get_text(strip=True) if author_tag else ""

            # Fetch the actual date from the individual post page
            pubdate = self._fetch_post_date(link)
            if pubdate is None:
                pubdate = fallback_timestamp

            article = Article(
                publisher=self.author,
                feed_title=self.title,
                headline=headline,
                link=link,
                pubdate=pubdate,
                source_type=self.source_type,
                author=author,
            )
            articles.append(article)

        return articles


# Pre-configured forum instances
si_ai_robotics_forum = SiliconInvestorPage(
    title="Artificial Intelligence, Robotics, Chat bots - ChatGPT",
    url="https://www.siliconinvestor.com/subject.aspx?subjectid=59856",
)

si_amd_intel_nvda_forum = SiliconInvestorPage(
    title="AMD, ARMH, INTC, NVDA",
    url="https://www.siliconinvestor.com/subject.aspx?subjectid=58128",
)
