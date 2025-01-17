from utils import load_yaml_file
from main import get_ragchain
import streamlit as st

config_data = load_yaml_file("config.yaml")

rag_chain = get_ragchain()

prompt_to_user="How may I help you?"

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": prompt_to_user}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

 # User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = rag_chain.invoke({"input": prompt}) 
            st.markdown(response["answer"])
    message = {"role": "assistant", "content": response["answer"]}
    st.session_state.messages.append(message)