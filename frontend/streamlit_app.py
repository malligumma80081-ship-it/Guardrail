import sys
from pathlib import Path

import streamlit as st  # type: ignore[import-not-found]

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import medical_chatbot

st.set_page_config(page_title="Medical Guardrail Assistant", page_icon="🩺")

st.title("Medical Guardrail Assistant")
st.caption("General medical education assistant with PII and safety guardrails.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ask a general medical question."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a medical question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        response = medical_chatbot(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)