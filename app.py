import streamlit as st
import bcrypt

from models import SessionLocal,User

st.set_page_config(page_title="Power Study AI",page_icon="📝",layout="wide")

if "user_id" not in st.session_state:
    st.session_state["user_id"]=None

db=SessionLocal()

# area of login or sign up or logout

if st.session_state["user_id"] is None:
    st.title("Welcome Power Study AI")

    tab1,tab2=st.tabs(["Sign In","Sign Up"])

    with tab1:

        st.subheader("Welcome let's Sign In")

        login_user=st.text_input("User Name",key="login user")

        login_pass=st.text_input("Password",type="password",key="login pass")

        if st.button("Sign in",type="primary"):
            user=db.query(User).filter(User.username==login_user).first()

            if user and bcrypt.checkpw(login_pass.encode("utf-8"),user.password_hash.encode("utf-8")):
                st.session_state["user_id"]=user.id

                st.success("Successfully login")
                st.rerun()
            else:
                st.error("Wrong Username or Password")

    with tab2:
        st.subheader("Create new account")

        new_user=st.text_input("User name",key="new user")
        new_pass=st.text_input("Password",key="new pass",type="password")

        if st.button("Create",type="primary"):
            hash_pw=bcrypt.hashpw(new_pass.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")

            new_account=User(username=new_user,password_hash=hash_pw)
            db.add(new_account)
            db.commit()

            st.success("Successfully Created")
            # st.rerun()

        else:
            st.warning("Please Enter the Pass , Username ")

else:

    
    st.title("Welcome your account")
    st.write("Use side bar to start study")
    if st.button("Logout",type="primary"):
        st.session_state["user_id"]=None
        st.rerun()            
