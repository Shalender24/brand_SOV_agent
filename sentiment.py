# sentiment.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize analyzer once
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str):
    """
    Analyzes sentiment using VADER.
    Returns a tuple: (sentiment_label, sentiment_score).
    """
    if not text or not text.strip():
        return "NEUTRAL", 0.0

    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        return "POSITIVE", compound
    elif compound <= -0.05:
        return "NEGATIVE", compound
    else:
        return "NEUTRAL", compound
