import re
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

STOPWORDS = set(stopwords.words("english")) | set(ENGLISH_STOP_WORDS)
lemmatizer = WordNetLemmatizer()

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

def preprocess_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    if nlp:
        doc = nlp(" ".join(tokens))
        tokens = [tok.lemma_ for tok in doc if not tok.is_stop and tok.is_alpha]
    return " ".join(tokens)