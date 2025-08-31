from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_ner_model():
    return pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

ner_model = load_ner_model()