import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("OpenAI GPT-4o Chat")

# Input for API key (never stores it anywhere)
api_key = st.text_input("Enter your OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY") or "")

if not api_key:
    st.warning("Please enter your OpenAI API key above.")
    st.stop()

st.markdown("_Your key is only used in your browser session and never stored._")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Say something to GPT-4o...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare request
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o",
            "messages": st.session_state.messages
        }
    )
    response.raise_for_status()
    reply = response.json()["choices"][0]["message"]["content"]
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
