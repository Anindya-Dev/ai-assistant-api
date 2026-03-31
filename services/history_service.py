from db.database import SessionLocal
from db.models import ConversationHistory

def get_user_history(user_id:int):
    db= SessionLocal()

    entries= db.query(ConversationHistory)\
    .filter(ConversationHistory.user_id==user_id)\
    .order_by(ConversationHistory.id.desc())\
    .all()

    result=[]

    for entry in entries:
        result.append({
            "query":entry.query,
            "answer":entry.answer,
            "time":entry.created_at
        })

    db.close()

    return result

def save_user_history(user_id: int, query: str, answer: str):
    db = SessionLocal()

    entry = ConversationHistory(
        query=query,
        answer=answer,
        user_id=user_id
    )

    db.add(entry)
    db.commit()
    db.close()
