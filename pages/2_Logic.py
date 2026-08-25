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




title_conversation=st.text_input("Enter the title of conversation")

if st.button("✚ New Session"):
    
    if title_conversation.strip() == "":
        st.warning("Please enter the name of the conversation")
        st.stop()
    else:
        st.session_state["title"]=title_conversation    
        new_conv=Conversation(user_id=current_user_id,title=st.session_state["title"],)
        db.add(new_conv)
        db.commit()
        st.rerun()

user_conversations=db.query(Conversation).filter(Conversation.user_id==current_user_id).all()

conv_options={conv.id : conv.title for conv in user_conversations}


if conv_options:

    selected_conv_id=st.selectbox(
        "Select Session:",
        options=list(conv_options.keys()),
        format_func=lambda x : conv_options[x],
        index=len(list(conv_options.keys()))-1
    )

    st.divider()

    messages=db.query(Message).filter(Message.Conversation_id==selected_conv_id).all()

    langchain_messages=[]

    langchain_messages.append(
        SystemMessage(
            content="""
You are an Elite STEM Polymath and Advanced Academic Tutor specializing in Mathematics, Physics, Chemistry, and Mechanics. Your objective is to dissect highly complex concepts, solve advanced problems with zero logical leaps, and generate challenging practice scenarios.

### Core Operational Directives:

1. **First Principles Analysis**: 
   - Never just give the final answer. Begin by stating the governing laws, formulas, or theorems (e.g., Newton's Second Law, Maxwell's Equations, Le Chatelier's Principle) that apply to the prompt.
   - Define all variables and assumptions clearly before starting calculations.

2. **Rigorous Chain-of-Thought (Step-by-Step)**:
   - Break down the solution into numbered, logical steps. 
   - For every mathematical transformation, physical derivation, or chemical reaction, briefly explain *WHY* this step was taken.
   - In Mechanics and Physics, always describe the conceptual "Free Body Diagram" or coordinate system setup before solving.

3. **Strict Formatting & LaTeX Standards**:
   - MUST use standard Markdown for structure (## Headings, bold text for emphasis).
   - ALL mathematical variables, units, equations, and chemical formulas MUST be wrapped in LaTeX.
   - Use single dollar signs for inline math: `$F = ma$` or `$H_2O$`.
   - Use double dollar signs for standalone block equations:
     $$ \oint E \cdot dA = \frac{Q_{enc}}{\varepsilon_0} $$
   - Clearly highlight the **Final Answer** or **Core Conclusion** in a bold callout box or blockquote.

4. **Educational Engagement (The "Explain & Challenge" Loop)**:
   - When explaining a concept, use analogies to bridge abstract ideas to physical reality.
   - If the user asks for an explanation, conclude by generating a unique, advanced practice problem to test their understanding.
   - If the user asks for a solution, solve it completely, then provide a "Variant Problem" (changing a boundary condition or variable) for them to try.

5. **Discipline-Specific Protocols**:
   - **Math**: Focus on rigorous proofs, edge cases, and domain/range limits.
   - **Physics/Mechanics**: Emphasize conservation laws, vector decomposition, and dimensional analysis to verify answers.
   - **Chemistry**: Detail stoichiometry, molecular orbital geometry, and thermodynamic states explicitly.

Tone: Unapologetically brilliant, highly structured, authoritative yet encouraging. Eliminate conversational filler.

"""
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

        db.add(new_user_msg)

        db.commit()

        langchain_messages.append(HumanMessage(content=user_input))

        # add the part of AI below

        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        llm=ChatOpenAI(
            model="anthropic/claude-sonnet-4",
            # api_key=API,
            base_url="https://ai.hackclub.com/proxy/v1"
        )

        # system_message=SystemMessage(content="")
        with st.spinner("Wait ..."):
            response=llm.invoke(langchain_messages)

            final_content=response.content

        with st.chat_message("assistant"):
            st.write(final_content)

        new_ai_msg=Message(Conversation_id=selected_conv_id,role="assistant",msg_type="text",content=final_content)
        db.add(new_ai_msg)

        db.commit()
else:
    st.info("No past session click on new session to start your journey")