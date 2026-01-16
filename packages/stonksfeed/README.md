# Stonksfeed

Stock news aggregator - RSS feeds and forum scrapers.

## Installation

```bash
# Install with uv
uv sync

# Install with dev dependencies
uv sync --all-extras
```

## Usage

### CLI

```bash
# Fetch all articles (RSS feeds + forums)
uv run stonksfeed

# Fetch RSS feeds only
uv run stonksfeed --rss-only

# Fetch forum posts only
uv run stonksfeed --forums-only

# Output as JSON
uv run stonksfeed --format json

# Save to file
uv run stonksfeed --format json -o articles.json
```

### Python API

```python
from stonksfeed import RSSReader, SiliconInvestorPage
from stonksfeed.config import RSS_FEEDS, SI_FORUMS

# Fetch from an RSS feed
reader = RSSReader(
    publisher="Marketwatch",
    feed_title="Breaking News",
    rss_url="https://feeds.content.dowjones.io/public/rss/mw_bulletins"
)
articles = reader.get_articles()

# Fetch from Silicon Investor forum
scraper = SiliconInvestorPage(
    title="AMD, ARMH, INTC, NVDA",
    url="https://www.siliconinvestor.com/subject.aspx?subjectid=58128"
)
posts = scraper.get_articles()
```

## Development

```bash
# Run tests
make test

# Run tests with coverage
make coverage

# Lint code
make lint

# Format code
make format

# Type check
make typecheck
```

## Configuration

Edit `src/stonksfeed/config.py` to add/remove RSS feeds or forum sources.
