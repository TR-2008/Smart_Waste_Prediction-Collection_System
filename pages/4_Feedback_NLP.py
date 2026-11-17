from pathlib import Path
import pandas as pd
import streamlit as st
from core.ui import render_sidebar, apply_theme, section_header
from core.sentiment import load_vader_analyzer, analyze_sentiment, detect_topics

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="Feedback Intelligence", page_icon="💬", layout="wide")
render_sidebar(ROOT)
apply_theme(st.session_state.get("ui_theme", "Dark"))
section_header("Feedback Intelligence", "Lexicon-based sentiment and keyword topic detection.")

try:
    analyzer = load_vader_analyzer(ROOT)
    text = st.text_area("Enter feedback", placeholder="Example: The collection was late and the bin overflowed.")
    if st.button("Analyze feedback", type="primary", disabled=not text.strip()):
        result = analyze_sentiment(text, analyzer)
        topics = detect_topics(text, ROOT / "data" / "topic_keywords.json")
        a, b = st.columns(2)
        a.metric("Sentiment", result["label"].title())
        b.metric("Compound score", f'{result["scores"]["compound"]:.3f}')
        st.write("Topic matches:", ", ".join(topics) if topics else "No configured keyword topic found.")
        st.json(result["scores"])
except Exception as exc:
    st.error(f"VADER could not be initialized: {exc}")

feedback_path = ROOT / "data" / "feedback.csv"
if feedback_path.exists():
    with st.expander("View supplied classroom reference examples"):
        st.dataframe(pd.read_csv(feedback_path), use_container_width=True, hide_index=True)
        st.caption("These are 30 authored classroom examples, not real customer survey responses.")
