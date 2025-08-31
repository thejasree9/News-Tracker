from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

sentiment_analyzer = load_sentiment_model()

def analyze_sentiment(texts):
    results = sentiment_analyzer(list(texts))
    sentiments = [res["label"] for res in results]
    return sentiments