from pathlib import Path
import pandas as pd
import streamlit as st
from core.ui import apply_theme,section_header
from core.sentiment import load_vader_analyzer,analyze_sentiment,detect_topics
ROOT=Path(__file__).resolve().parents[1]; apply_theme(st.session_state.get('ui_theme','Dark'))
section_header('Collection Comments','VADER sentiment and configured keyword-topic detection.')
text=st.text_area('Enter feedback',placeholder='The collection was late and the bin overflowed.')
if st.button('Analyze feedback',type='primary',disabled=not text.strip()):
    topics=detect_topics(text,ROOT/'data'/'topic_keywords.json'); st.write('Topic matches:',', '.join(topics) if topics else 'No configured topic matched.')
    try:
        analyzer=load_vader_analyzer(ROOT); result=analyze_sentiment(text,analyzer)
        a,b=st.columns(2); a.metric('Sentiment',result['label'].title()); b.metric('Compound score',f"{result['scores']['compound']:.3f}"); st.json(result['scores'])
    except LookupError:
        st.warning('VADER lexicon is missing. Topic matching works, but sentiment scoring is unavailable until data/nltk_data/sentiment/vader_lexicon/vader_lexicon.txt is restored. No sentiment is fabricated.')
    except Exception as e: st.error(f'Sentiment analysis unavailable: {e}')
p=ROOT/'data'/'feedback.csv'
if p.exists():
    d=pd.read_csv(p); st.markdown('### Supplied reference comments'); st.dataframe(d,use_container_width=True,hide_index=True)
    st.caption('30 authored English classroom examples with supplied reference labels; not real customer feedback.')
