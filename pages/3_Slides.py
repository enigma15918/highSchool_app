import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage 
from models import SessionLocal
if "user_id" not in st.session_state or st.session_state["user_id"] is None:
    st.warning("You must login !!!")
    st.stop()

db=SessionLocal()

current_user_id=st.session_state["user_id"]

st.title("Presentation and Slides generator ")

st.write("Transform your study to be visualized and organized")

with st.form("slides-form"):

    topic_input=st.text_area(
        "Enter the topic, text or main point of your slides will be",
        placeholder="e.g. Explain what is the transistors"
    )

    col1,col2=st.columns(2)

    with col1:
        num_slides=st.slider("Number of slides",min_value=3, max_value=16,value=5)

    with col2:
        target_audience=st.selectbox("Target Audience:", 
                            ["General Public","Academic / Students","Business","Professional","Technical","Developers"])
        theme_style = st.selectbox("Visual Theme:", ["Modern Dark", "Clean Light", "Gradient Tech"])

    submitted=st.form_submit_button("Generate Slides",type="primary")

if submitted:

    if not topic_input.strip():
        st.warning("Please enter a topic firstly")

    else:

        with st.spinner("it is generating"):
            API=""

            llm=ChatOpenAI(
                api_key=API,
                model="anthropic/claude-sonnet-5",
                base_url="https://ai.hackclub.com/proxy/v1"
            )

            system_prompt=SystemMessage(
                content=f"""
                You are an elite presentation designer and public speaking expert. 
                Create a professional, structured presentation with exactly {num_slides} slides based on the user's input.
                Target audience: {target_audience}.
                You are an expert web designer and presentation author. 
                Your task is to generate a fully self-contained single-file HTML/CSS presentation with exactly {num_slides} slides.
                Theme style: {theme_style}.
                
                Requirements for the HTML code:
                1. Include modern CSS styling (responsive, flexbox/grid, beautiful fonts, smooth transitions between slide cards).
                2. Include interactive charts using Chart.js (via CDN: https://cdn.jsdelivr.net/npm/chart.js) for relevant data/trends.
                3. Structure each slide cleanly with cards, icons (using SVG or unicode), bullet points, and high contrast.
                4. Output ONLY the raw valid standard HTML code without markdown code blocks (do not wrap in ```html ... ```).

            """
            )

            user_msg=HumanMessage(content=f"Topic/Content: {topic_input}")

            response=llm.invoke([system_prompt,user_msg])

            html_content=response.content.replace("```html", "").replace("```", "").strip()

            st.success("Slides generated successfully")

            st.divider()

            st.components.v1.html(html_content, height=650, scrolling=True)

            st.divider()


            st.download_button(
                label="Download html file",
                data=html_content,
                file_name="presentation.html",
                mime="text/html"
            )