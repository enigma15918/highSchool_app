import streamlit as st

st.title("Test some features")

with st.chat_message("ai"):
    st.write("hello")

st.chat_input("enter your question")