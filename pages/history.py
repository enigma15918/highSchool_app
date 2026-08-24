import streamlit as st
from models import Conversation,SessionLocal,Message


if "user_id" not in st.session_state or st.session_state["user_id"] is None:
    st.warning("You must go to signIn/SignUp")

db=SessionLocal()

current_user_id=st.session_state["user_id"]
st.title("Study Sessions")


user_conversations=db.query(Conversation).filter(Conversation.user_id==current_user_id).all()

if st.button("Add new icon ✚"):
    new_conv=Conversation(user_id=current_user_id,title="new study session")
    db.add(new_conv)
    db.commit()
    st.rerun()

conv_options={conv.id : conv.title for conv in user_conversations}

selected_conv_id=None
if conv_options:
    selected_conv_id=st.selectbox(
        "Choose a session",
        options=list(conv_options.keys()),
        format_func=lambda x: conv_options[x]
    )

    st.markdown("---")

    

    
    st.title("Details of session")
    st.write(f"Now we are in {selected_conv_id}")

    from models import Message

    messages=db.query(Message).filter(Message.Conversation_id==selected_conv_id).all()

    for msg in messages:
        with st.chat_message(msg.role):
            st.write(msg.content)

    user_input=st.chat_input("Enter your question here")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        new_user_msg=Message(
            Conversation_id=selected_conv_id,
            role="user",
            msg_type="text",
            content=user_input
        )

        db.add(new_user_msg)
        ai_response=f"hello {user_input}"

        with st.chat_message("assistant"):
            st.write(ai_response)

        new_ai_msg=Message(
            Conversation_id=selected_conv_id,
            role="assistant",
            msg_type="text",
            content=ai_response
        )
        db.add(new_ai_msg)
        db.commit()
else:
    st.info("Click on new study session to start (there is no history)")