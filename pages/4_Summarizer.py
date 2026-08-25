import streamlit  as st

import os 

from pypdf import PdfReader

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, SystemMessage

if "user_id" not in st.session_state or st.session_state["user_id"] is None:

    st.warning("You must go back and sign in")

    st.stop()

if "summary_html" not in st.session_state:
    st.session_state["summary_html"]=None

st.title("Interactive Smart Summarize Model ")

st.write("Upload your file as pdf, text files or copy text")

tab1,tab2=st.tabs(["Upload File(PDF,TXT)","Paste Direct Text"])

input_text=""

with tab1:
    uploaded_file=st.file_uploader("Upload PDF or TXT reference",type=["pdf","txt"])

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".pdf"):

            pdf_reader=PdfReader(uploaded_file)

            for page in pdf_reader.pages:

                extracted=page.extract_text()

                if extracted:
                    input_text+=extracted+ "\n"

        elif uploaded_file.name.endswith(".txt"):
            input_text=uploaded_file.read().decode("utf-8")

with tab2:

    pasted_text=st.text_area("Paste reference text")

    if pasted_text.strip():
        input_text=pasted_text

st.divider()


col1,col2=st.columns(2)

with col1:
    summary_type=st.selectbox(
        "Summary Style",
        options=["Key Bullet Points","Comprehensive Study Guide","QA & Glossary"]

    )

with col2:

    theme_choice=st.selectbox(
        "visual theme",
        options=["Modern Dark","Clean Soft Light","Ocean Blue"]
    )

if st.button("Generate Summary ",type="primary"):

    if not input_text.strip():
        st.warning("Please upload file ot paste the text")
    else:

        with st.spinner("It is creating ..."):

            API=""

            llm=ChatOpenAI(
                api_key=API,
                model="google/gemini-2.5-pro",
                base_url="https://ai.hackclub.com/proxy/v1"
            )

            system_prompt=SystemMessage(
                content=
            f"""You are an expert educational designer and front-end creator.
                Create a standalone HTML summary document based on the input text.
                Style choice: {summary_type}. Visual theme: {theme_choice}.
                
                HTML Requirements:
                1. Use embedded modern CSS (responsive cards, clean fonts, badge highlights for key terms, callout boxes).
                2. Structure into clear sections (Overview, Core Concepts, Key Takeaways).
                3. Add visual hierarchy (colored sidebars, clean margins, high contrast).
                4. Output ONLY standard valid raw HTML code without markdown code fences (no ```html ... ```)."""

            )

            user_msg=HumanMessage(
                content=f""""
                    Source text :\n {input_text[:50000]}
                """
            )

            response=llm.invoke([system_prompt,user_msg])


            st.session_state["summary_html"]=response.content.replace("```html","").replace("```","").strip()


if st.session_state["summary_html"]:

    st.divider()

    st.subheader("Visualize Summary")

    st.components.v1.html(st.session_state["summary_html"],height=600,scrolling=True)

    st.divider()
    file_name=st.text_input("enter the name of the file",value="summarized file")
    st.download_button(
        "Download the file",
        data=st.session_state["summary_html"],
        file_name=file_name+".html",
        mime="text/html"
    )