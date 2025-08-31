import requests
import pandas as pd
import streamlit as st

DEFAULT_GNEWS_ENDPOINT = "https://gnews.io/api/v4"

@st.cache_data(ttl=300)
def fetch_news_from_gnews(api_key: str, category: str = None, q: str = None, country: str = None, page_size: int = 50):
    url = f"{DEFAULT_GNEWS_ENDPOINT}/top-headlines"
    params = {"apikey": api_key, "max": page_size, "lang": "en"}

    if country:
        params["country"] = country
    if category and category != "general":
        params["topic"] = category
    if q:
        params["q"] = q

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    articles = data.get("articles", [])
    df = pd.DataFrame(articles)
    if df.empty:
        return df
    if "publishedAt" in df.columns:
        df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors="coerce")
    if "source" in df.columns:
        df["source_name"] = df["source"].apply(lambda s: s.get("name") if isinstance(s, dict) else s)
        df = df.drop(columns=["source"])
    keep = [c for c in ["source_name", "title", "description", "url", "publishedAt"] if c in df.columns]
    return df[keep]