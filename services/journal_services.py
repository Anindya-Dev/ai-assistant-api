from db.database import SessionLocal
from db.models import JournalEntry
from embedding_service import generate_embedding
from db.chroma import add_to_chroma
def add_journal_entry(text: str):
    db=SessionLocal()
    new_entry=JournalEntry(content=text)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    embedding=generate_embedding(text)

    add_to_chroma(new_entry.id,text,embedding)
    
    db.close()

    return new_entry.id