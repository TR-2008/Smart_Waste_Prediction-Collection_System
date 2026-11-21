from pathlib import Path
import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def load_vader_analyzer(project_root):
    data_dir=Path(project_root)/'data'/'nltk_data'
    nltk.data.path.insert(0,str(data_dir))
    return SentimentIntensityAnalyzer()

def analyze_sentiment(text, analyzer):
    scores=analyzer.polarity_scores(text); c=scores['compound']
    label='positive' if c>=0.05 else ('negative' if c<=-0.05 else 'neutral')
    return {'label':label,'scores':scores}

def detect_topics(text, keywords_path):
    path=Path(keywords_path)
    if not path.exists(): return []
    data=json.loads(path.read_text(encoding='utf-8')); low=str(text).casefold()
    return [topic for topic, words in data.items() if any(str(word).casefold() in low for word in words)]
