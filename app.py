# streamlit_app.py
import os
import streamlit as st
from mistralai import Mistral

st.set_page_config(page_title="Mistral Chat", page_icon="🤖")

# --- API key handling ---
api_key = os.getenv("MISTRAL_API_KEY") or st.sidebar.text_input(
    "MISTRAL_API_KEY", type="password", help="Prefer Streamlit Secrets in production."
)
if not api_key:
    st.info("Add your MISTRAL_API_KEY in Streamlit → Settings → Secrets, or paste it in the sidebar.")
    st.stop()

# --- Client & model ---
client = Mistral(api_key=api_key)
MODEL = "mistral-large-latest"
SYSTEM_PROMPT = "You are a friendly assistant. Keep answers short and helpful."

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

st.title("🤖 Mistral Chat")

# Display history (hide the system message)
for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.markdown(m["content"])

# --- Input box ---
user_msg = st.chat_input("Type your message...")
if user_msg:
    # show user msg
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    # call Mistral
    try:
        resp = client.chat.complete(
            model=MODEL,
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=400,
        )
        bot_reply = resp.choices[0].message.content
    except Exception as e:
        bot_reply = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

# --- Clear chat ---
if st.sidebar.button("Clear chat"):
    st.session_state.clear()
    st.rerun()
