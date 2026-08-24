import streamlit  as st

import os 

from pypdf import PdfReader

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, SystemMessage

if "user_id" not in st.session_state or st.session_state["user_id"] is None:

    st.warning("You must go back and sign in")

    st.stop()