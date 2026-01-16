"""Ticker symbol extraction from text."""

import re
from typing import List, Set

# Common stock tickers that appear frequently in financial news
# This helps catch tickers without $ prefix
COMMON_TICKERS: Set[str] = {
    # Mega caps
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "BRK",
    # Tech
    "AMD", "INTC", "AVGO", "QCOM", "CRM", "ORCL", "IBM", "CSCO", "ADBE",
    "NFLX", "PYPL", "SQ", "SHOP", "SNOW", "PLTR", "UBER", "LYFT", "ABNB",
    # Finance
    "JPM", "BAC", "WFC", "GS", "MS", "C", "AXP", "V", "MA", "BLK",
    # Healthcare
    "UNH", "JNJ", "PFE", "ABBV", "MRK", "LLY", "TMO", "ABT", "BMY", "AMGN",
    # Consumer
    "WMT", "HD", "MCD", "NKE", "SBUX", "TGT", "COST", "LOW", "DIS", "CMCSA",
    # Energy
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "HAL",
    # Industrial
    "CAT", "DE", "BA", "HON", "UPS", "FDX", "LMT", "RTX", "GE", "MMM",
    # Semiconductors
    "TSM", "ASML", "MU", "LRCX", "KLAC", "AMAT", "MRVL", "ON", "ADI", "TXN",
    # ETFs
    "SPY", "QQQ", "IWM", "DIA", "VTI", "VOO", "ARKK", "XLF", "XLE", "XLK",
    # Crypto-related
    "COIN", "MSTR", "RIOT", "MARA", "HUT",
    # Meme stocks
    "GME", "AMC", "BB", "BBBY", "WISH", "CLOV", "SOFI",
    # ARM
    "ARM", "ARMH",
}

# Words that look like tickers but aren't
FALSE_POSITIVES: Set[str] = {
    "A", "I", "AI", "CEO", "CFO", "CTO", "FDA", "SEC", "FED", "GDP", "IPO",
    "ETF", "NYSE", "NASDAQ", "DOW", "USA", "UK", "EU", "US", "IT", "PM",
    "AM", "CEO", "THE", "FOR", "AND", "NOT", "BUT", "ARE", "WAS", "HAS",
    "HAD", "CAN", "ALL", "NEW", "NOW", "MAY", "SAY", "SEE", "BIG", "TOP",
    "LOW", "HIGH", "UP", "DOWN", "Q1", "Q2", "Q3", "Q4", "YOY", "QOQ",
    "EPS", "PE", "PS", "PB", "ROE", "ROI", "M&A", "LLC", "INC", "LTD",
    "VS", "EST", "PST", "CST", "MST", "AT", "TO", "AS", "ON", "IN", "BY",
}


class TickerExtractor:
    """
    Extract stock ticker symbols from text.

    Uses multiple strategies:
    1. $SYMBOL pattern (explicit ticker mentions)
    2. Known ticker lookup (common stocks)
    3. Pattern matching for potential tickers (1-5 uppercase letters)
    """

    def __init__(self, include_potential: bool = False) -> None:
        """
        Initialize ticker extractor.

        :param include_potential: If True, include potential tickers that match
                                  the pattern but aren't in the known list.
                                  Can increase false positives.
        """
        self._include_potential = include_potential
        # Pattern for $SYMBOL format
        self._dollar_pattern = re.compile(r"\$([A-Z]{1,5})\b")
        # Pattern for potential tickers (1-5 uppercase letters as whole word)
        self._ticker_pattern = re.compile(r"\b([A-Z]{2,5})\b")

    def extract(self, text: str) -> List[str]:
        """
        Extract ticker symbols from text.

        :param text: Text to search for tickers
        :return: List of unique ticker symbols found (sorted)
        """
        tickers: Set[str] = set()

        # Strategy 1: Find explicit $SYMBOL mentions
        dollar_matches = self._dollar_pattern.findall(text)
        for match in dollar_matches:
            if match not in FALSE_POSITIVES:
                tickers.add(match)

        # Strategy 2 & 3: Find uppercase words that could be tickers
        potential_matches = self._ticker_pattern.findall(text)
        for match in potential_matches:
            if match in FALSE_POSITIVES:
                continue
            # If it's a known ticker, always include it
            if match in COMMON_TICKERS:
                tickers.add(match)
            # If include_potential is True, include any valid pattern
            elif self._include_potential and len(match) >= 2:
                tickers.add(match)

        return sorted(tickers)
