"""Sentiment analysis using VADER."""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """
    Analyze sentiment of financial news headlines using VADER.

    VADER (Valence Aware Dictionary and sEntiment Reasoner) is specifically
    tuned for social media and news text, handling:
    - Capitalization (ALL CAPS = more intense)
    - Punctuation (exclamation marks)
    - Negation
    - Financial terminology
    """

    def __init__(self) -> None:
        self._analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment of text.

        :param text: Text to analyze (typically a headline)
        :return: Dict with score (-1 to 1) and label (bullish/bearish/neutral)
        """
        scores = self._analyzer.polarity_scores(text)
        compound = scores["compound"]

        # Classify based on compound score
        # Using financial terminology: bullish (positive), bearish (negative)
        if compound >= 0.05:
            label = "bullish"
        elif compound <= -0.05:
            label = "bearish"
        else:
            label = "neutral"

        return {
            "score": round(compound, 3),
            "label": label,
        }
