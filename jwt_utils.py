import jwt
import time
import streamlit as st

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60

JWT_SECRET_KEY = st.secrets.get("JWT_SECRET_KEY", "secret")

def create_jwt_token(username: str) -> str:
    now = int(time.time())
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + JWT_EXPIRE_MINUTES * 60
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token if isinstance(token, str) else token.decode("utf-8")

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        st.warning("Session expired. Please log in again.")
        return None
    except jwt.InvalidTokenError:
        return None