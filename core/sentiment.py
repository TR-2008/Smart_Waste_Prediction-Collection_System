from pathlib import Path
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


def load_vader_analyzer(project_root):
    """
    Loads the bundled VADER lexicon from data/nltk_data.
    Expected NLTK resource layout:
      data/nltk_data/sentiment/vader_lexicon/vader_lexicon.txt
    """
    nltk_data_dir = Path(project_root) / "data" / "nltk_data"
    nltk.data.path.insert(0, str(nltk_data_dir))
    return SentimentIntensityAnalyzer()


def analyze_sentiment(text, analyzer):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return {"label": label, "scores": scores}
