# ui/chat_app.py

import streamlit as st
import requests

API_BASE = "http://localhost:8001"  # FastAPI backend base URL
API_MEM = "http://localhost:8000"  # FastAPI backend base URL

st.set_page_config(page_title="Chat with Memory", page_icon="💬", layout="centered")

st.title("💬 Chat with Memory Framework")

# Sidebar for settings
st.sidebar.header("Settings")
redis_url = st.sidebar.text_input("Redis REST URL", f"{API_MEM}/redis")
qdrant_url = st.sidebar.text_input("Qdrant REST URL", f"{API_MEM}/qdrant")
neo4j_url = st.sidebar.text_input("Neo4j REST URL", f"{API_MEM}/neo4j")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input("Type your message..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI backend
    try:
        resp = requests.post(f"{API_BASE}/message", json={"message": prompt})
        if resp.status_code == 200:
            data = resp.json()
            bot_reply = data.get("reply", "No response from backend.")
        else:
            bot_reply = f"❌ Error {resp.status_code}: {resp.text}"
    except Exception as e:
        bot_reply = f"🚨 Exception: {str(e)}"

    # Add bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

st.sidebar.markdown("### Debug Tools")
if st.sidebar.button("Check Redis"):
    r = requests.get(f"{redis_url}/keys")
    st.sidebar.json(r.json())

if st.sidebar.button("Check Qdrant"):
    q = requests.get(f"{qdrant_url}/scroll?collection_name=summaries&limit=5")
    st.sidebar.json(q.json())

if st.sidebar.button("Check Neo4j"):
    n = requests.get(f"{neo4j_url}/nodes")
    st.sidebar.json(n.json())
