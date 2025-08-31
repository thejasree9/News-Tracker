import pandas as pd
from collections import Counter
from nlp.preprocessing import preprocess_text

def combine_and_preprocess(frames: list) -> pd.DataFrame:
    if not frames:
        return pd.DataFrame()
    articles = pd.concat(frames, ignore_index=True)
    articles["clean_title"] = articles["title"].apply(preprocess_text)
    articles["clean_description"] = articles["description"].apply(preprocess_text)
    articles["combined_text"] = (
        articles["clean_title"].fillna("") + " " + articles["clean_description"].fillna("")
    ).str.strip()
    if "url" in articles.columns:
        articles = articles.drop_duplicates(subset=["url"])
    else:
        articles = articles.drop_duplicates(subset=["title"])
    return articles

def build_word_counts(series: pd.Series, top_n: int = 25):
    counter = Counter()
    for doc in series.fillna(""):
        counter.update(doc.split())
    return pd.DataFrame(counter.most_common(top_n), columns=["word", "count"])