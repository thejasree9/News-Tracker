import streamlit as st
import pandas as pd
import plotly.express as px

# --- Auth ---
from auth.database import create_user_table, add_user, check_credentials
from auth.jwt_utils import create_jwt_token, verify_jwt_token

# --- News ---
from news.fetcher import fetch_news_from_gnews
from news.utils import combine_and_preprocess, build_word_counts

# --- NLP ---
from nlp.sentiment import analyze_sentiment, sentiment_analyzer
from nlp.ner import ner_model

# --- UI ---
from ui.helpers import load_css, logout

# -----------------------
# App Config
# -----------------------
st.set_page_config(page_title="Personalized News Tracker", layout="wide")
create_user_table()

CATEGORIES = [
    "business", "entertainment", "general", "health",
    "science", "sports", "technology", "education", "finance"
]

def main():
    load_css("style.css")
    st.title("🌐 Personalized News Tracker")

    # Sidebar: Menu
    st.sidebar.header("Account")
    menu = ["Home", "Login", "Sign Up"]

    if "token" in st.session_state and st.session_state.get("token"):
        payload = verify_jwt_token(st.session_state.get("token"))
        if payload:
            menu = ["Home", "News Tracker", "Logout"]
        else:
            st.session_state.pop("token", None)
            st.session_state.pop("username", None)

    choice = st.sidebar.selectbox("Menu", menu)

    # ------------------- Home -------------------
    if choice == "Home":
        st.markdown("""
        ## Welcome
        Use *Sign Up* to create a new account, then *Login*.
        After logging in visit *News Tracker* to select categories and fetch trending news.
        """)

    # ------------------- Sign Up -------------------
    elif choice == "Sign Up":
        st.header("Create Account")
        new_user = st.text_input("Username", key="reg_user")
        new_pass = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            if not new_user or not new_pass:
                st.warning("Enter both username and password.")
            else:
                created = add_user(new_user.strip(), new_pass)
                st.success("Account created.") if created else st.error("Username already exists.")

    # ------------------- Login -------------------
    elif choice == "Login":
        st.header("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if not username or not password:
                st.warning("Provide username and password.")
            elif check_credentials(username.strip(), password):
                token = create_jwt_token(username.strip())
                st.session_state["token"] = token
                st.session_state["username"] = username.strip()
                st.success(f"Welcome, {username.strip()}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    # ------------------- Logout -------------------
    elif choice == "Logout":
        st.header("Logout")
        if st.button("Confirm logout"):
            logout()

    # ------------------- News Tracker -------------------
    elif choice == "News Tracker":
        token = st.session_state.get("token")
        payload = verify_jwt_token(token) if token else None
        if not payload:
            st.error("You must be logged in to use the News Tracker.")
            return

        st.sidebar.markdown(f"Logged in as *{st.session_state.get('username')}*")
        if st.sidebar.button("Logout"):
            logout()

        cols = st.columns([2, 1])
        with cols[0]:
            selected = st.multiselect("Select categories", options=CATEGORIES, default=["general"])
            query = st.text_input("Optional keyword / search query", value="")
            country = st.selectbox("Country", options=[None, "us", "in", "gb", "au", "ca"], index=0)
            fetch_btn = st.button("Fetch Trending News")
        with cols[1]:
            page_size = st.number_input("Articles per category", min_value=10, max_value=100, value=50, step=5)

        if fetch_btn:
            api_key = st.secrets.get("GNEWS_API_KEY", None)
            if not api_key:
                st.error("GNews API Key is required.")
            elif not selected:
                st.warning("Please select at least one category.")
            else:
                frames = []
                for cat in selected:
                    try:
                        df = fetch_news_from_gnews(api_key=api_key, category=cat, q=query or None, country=country or None, page_size=int(page_size))
                    except Exception as e:
                        st.error(f"Error fetching category '{cat}': {e}")
                        df = pd.DataFrame()
                    if not df.empty:
                        df["category"] = cat
                        frames.append(df)

                if not frames:
                    st.warning("No articles returned.")
                    return

                # Combine & preprocess
                articles = combine_and_preprocess(frames)
                st.subheader(f"Ingested Articles ({len(articles)})")
                st.dataframe(articles[["title", "source_name", "publishedAt", "category"]])

                # --- Visualizations ---
                st.subheader("Visualizations")
                v1, v2 = st.columns(2)
                with v1:
                    if "source_name" in articles.columns:
                        src_counts = articles["source_name"].value_counts().reset_index()
                        src_counts.columns = ["source", "count"]
                        fig = px.bar(src_counts.head(20), x="source", y="count", title="Top sources")
                        st.plotly_chart(fig, use_container_width=True)
                with v2:
                    wc = build_word_counts(articles["combined_text"], top_n=30)
                    if not wc.empty:
                        fig2 = px.bar(wc, x="word", y="count", title="Top words")
                        st.plotly_chart(fig2, use_container_width=True)

                # --- Sentiment Analysis ---
                st.subheader("📊 Sentiment Analysis on News")
                sentiments = analyze_sentiment(articles["clean_title"].head(50))
                articles["sentiment"] = sentiments
                sentiment_counts = articles["sentiment"].value_counts().reset_index()
                sentiment_counts.columns = ["Sentiment", "Count"]
                fig = px.pie(sentiment_counts, names="Sentiment", values="Count",
                             title="Sentiment Distribution of News Articles",
                             color="Sentiment",
                             color_discrete_map={"POSITIVE": "green", "NEGATIVE": "red", "NEUTRAL": "gray"})
                st.plotly_chart(fig, use_container_width=True)

                # --- NER ---
                st.subheader("🔎 Named Entity Recognition (NER)")
                texts_for_ner = (articles["title"].fillna("") + " " + articles["description"].fillna("")).head(30).tolist()
                all_entities = []
                for text in texts_for_ner:
                    ents = ner_model(text)
                    for e in ents:
                        all_entities.append({"Entity": e["word"], "Label": e["entity_group"]})
                if all_entities:
                    st.dataframe(pd.DataFrame(all_entities))

                # --- Article Explorer ---
                st.subheader("📰 Article Explorer")
                emoji_map = {"POSITIVE": "✅😊", "NEGATIVE": "❌😞", "NEUTRAL": "😐"}
                for _, row in articles.iterrows():
                    with st.expander(f"🗞️ {row['title']} | {row['sentiment']} {emoji_map.get(row['sentiment'], '❓')}"):
                        st.write(f"**Source:** {row['source_name']}")
                        st.write(f"**Published At:** {row['publishedAt']}")
                        st.write(row["description"] if row["description"] else "No description available.")
                        if row.get("url"):
                            st.markdown(f"[🔗 Read full article]({row['url']})")

if __name__ == "__main__":
    main()
