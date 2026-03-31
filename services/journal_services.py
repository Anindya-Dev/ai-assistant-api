from db.database import SessionLocal
from db.models import JournalEntry
from services.embedding_service import generate_embedding
from db.chroma import add_to_chroma

def add_journal_entry(text: str,user_id:int):
    db=SessionLocal()
    new_entry=JournalEntry(content=text,user_id=user_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    embedding=generate_embedding(text)

    add_to_chroma(new_entry.id,text,embedding,user_id)
    
    db.close()

    return new_entry.id

def get_user_journal_history(user_id: int):
    db = SessionLocal()

    entries = (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == user_id)
        .order_by(JournalEntry.id.desc())
        .all()
    )

    result = []
    for entry in entries:
        result.append({
            "id": entry.id,
            "content": entry.content,
            "time": entry.created_at
        })

    db.close()
    return result
