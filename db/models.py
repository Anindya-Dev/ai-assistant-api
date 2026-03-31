from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db.database import Base
from datetime import datetime

class JournalEntry(Base):
    __tablename__="journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    content=Column(String,nullable=False)
    user_id= Column(Integer,ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    username= Column(String,unique=True)
    password= Column(String)


class ConversationHistory(Base):
    __tablename__="conversation_history"

    id=Column(Integer,primary_key=True,index=True)

    query= Column(String)
    answer=Column(String)

    user_id=Column(Integer,ForeignKey("users.id"))
    created_at=Column(DateTime,default=datetime.utcnow)


