# imports

from sqlalchemy import Column, Integer,String, ForeignKey, DateTime, Text,create_engine

from sqlalchemy.orm import declarative_base, relationship,sessionmaker

import datetime

# inherit class will pass for all classes
Base=declarative_base()

class User(Base):

    __tablename__="users"

    id=Column(Integer,primary_key=True)

    username=Column(String(50),unique=True,nullable=False)

    password_hash=Column(String(255),nullable=False)

    conversations=relationship("Conversation",back_populates="user")


class Conversation(Base):
    __tablename__="conversations"

    id=Column(Integer,primary_key=True)
    # we called the user id from id of users to save all conservations by that id to get all conservations of this user easily
    user_id=Column(Integer,ForeignKey("users.id"))
    title=Column(String,default="new study session")
    created_at=Column(DateTime,default=datetime.datetime.now)


    user=relationship("User",back_populates="conversations")

    messages=relationship("Message",back_populates="conversation")

class Message(Base):
    __tablename__="messages"
    id=Column(Integer,primary_key=True)
    Conversation_id=Column(Integer,ForeignKey("conversations.id"))

    role=Column(String(20))

    msg_type=Column(String)

    content=Column(Text)

    file_path=Column(String,nullable=True)
    timestamp=Column(DateTime,default=datetime.datetime.now)

    conversation=relationship("Conversation",back_populates="messages")

engine=create_engine("sqlite:///study_app.db")

Base.metadata.create_all(engine)

SessionLocal=sessionmaker(bind=engine)