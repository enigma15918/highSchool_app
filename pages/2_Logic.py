import streamlit as st
import os
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

from models import SessionLocal, Conversation, Message

from langchain_openai import ChatOpenAI

if "user_id" not in st.session_state or st.session_state["user_id"] is None:
    st.warning("Please go back and login")
    st.stop()

db=SessionLocal()

current_user_id=st.session_state["user_id"]

st.title("Logic & Simplify")

st.write("I am here to help you break down complex topics and present the simplest explanation ")

if st.button("✚ New Session"):

    new_conv=Conversation(user_id=current_user_id,title="Logic & Simplify",)
    db.add(Conversation)
    db.add(new_conv)
    db.commit()
    st.rerun()

user_conversations=db.query(Conversation).filter(Conversation.user_id==current_user_id).all()

conv_options={conv.id : conv.title for conv in user_conversations}


if conv_options:

    selected_conv_id=st.selectbox(
        "Select Session:",
        options=list(conv_options.keys()),
        format_func=lambda x : conv_options[x]
    )

    st.divider()

    messages=db.query(Message).filter(Message.conversation_id==selected_conv_id).all()

    langchain_messages=[]

    langchain_messages.append(
        SystemMessage(
            content=""
        )
    )

    for msg in messages:

        with st.chat_message(msg.role):
            st.write(msg.content)

        if msg.role == "user":
            langchain_messages.append(
                HumanMessage(content=msg.content)
            )

        elif msg.role == "assistant":
            langchain_messages.append(
                AIMessage(content="")
            )

    user_input=st.chat_input("Type your problem or logic question")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        new_user_msg=Message(Conversation_id=selected_conv_id,role="user",msg_type="text",content=user_input)