import streamlit as st

def load_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def logout():
    st.session_state.pop("token", None)
    st.session_state.pop("username", None)
    st.rerun()