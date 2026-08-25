import streamlit as st
from models import Conversation,SessionLocal,Message
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

if "user_id" not in st.session_state or st.session_state["user_id"] is None:
    st.warning("You must go to signIn/SignUp")

db=SessionLocal()

current_user_id=st.session_state["user_id"]
st.title("Study Sessions")


user_conversations=db.query(Conversation).filter(Conversation.user_id==current_user_id).all()

# if st.button("Add new icon ✚"):
#     new_conv=Conversation(user_id=current_user_id,title="new study session")
#     db.add(new_conv)
#     db.commit()
#     st.rerun()

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
    user_input=HumanMessage(content=user_input)

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
        # API=""
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        llm=ChatOpenAI(
            model="google/gemini-3.6-flash",
            base_url="https://ai.hackclub.com/proxy/v1",
            # api_key=API
        )
        system_message=SystemMessage(content="""
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

""")
        invoking=llm.invoke([user_input,system_message])
        ai_response=invoking.content

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
    st.info("Click on new page to start a session (There is no history)")