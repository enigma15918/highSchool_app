import streamlit as st

NAME="Study Hero"

if "user_id" not in st.session_state or st.session_state["user_id"] is None:
    st.warning("You should SignIn Firstly")

    st.stop()

st.title(f"Welcome {NAME}")

st.subheader("Your Teacher Assistant ")

st.divider()

st.markdown(f"""
# Welcome to your comprehensive education platform. 
### {NAME} is created to help you go from zero to hero in your study by support the best LLMs and AI generative in specific fields 
- you can summarize your notes,books, and etc
- you can see or get a simple explanation for anything you need by 'Claude" and others models
- you can notice the name of pages in sidebar and choose the specific part which you want

""")

col1,col2=st.columns(2)

with col1:
    st.info("**Simplify and Logic:**\nBreaking down complex problems and explanation them step by step")

    st.info("**Tasks & Slides:**\n you can create quiz or slides for presentation and related objects ")

    st.info("**Mind Maps:**\n Here after understanding you can do a visualize and good summary file for what you have studied")

with col2:
    st.success("**SmartSummary:**\n Here you can get the best summary and after you get it pass it through the 'Mind Map' and you will get a better result")

    st.success("**RAG System:** Here you can upload your PDF file and you will get the information from it by the best way")

    st.success("**Chat History:** You can access all of your previous conversations")

st.divider()

st.caption("I made it to help me in my senior year")

