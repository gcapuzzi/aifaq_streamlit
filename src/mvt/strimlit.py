from utils import load_yaml_file
from main import get_ragchain
import streamlit as st

config_path = "config.yaml"

logo_path = "https://github.com/gcapuzzi/aifaq_streamlit/blob/main/images/logo.png?raw=true"

config_data = load_yaml_file(config_path)

rag_chain = get_ragchain()

prompt_to_user="How may I help you?"

st.title("AIFAQ ChatBot")
"""
An AI chatbot powered by https://github.com/hyperledger-labs/aifaq
"""

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": prompt_to_user}]

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "assistant":
        message["avatar"] = logo_path
    with st.chat_message(message["role"], avatar=logo_path):
        st.write(message["content"])

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message(name='assistant', avatar=logo_path):
        with st.spinner("Thinking..."):
            response = rag_chain.invoke({"input": prompt}) 
            st.markdown(response["answer"])
    message = {"role": "assistant", "content": response["answer"]}
    st.session_state.messages.append(message)