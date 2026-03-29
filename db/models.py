from sqlalchemy import Column, Integer, String
from db.database import Base

class JournalEntry(Base):
    __tablename__="journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    content=Column(String,nullable=False)
