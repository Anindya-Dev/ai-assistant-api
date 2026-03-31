from fastapi import APIRouter
from pydantic import BaseModel
from services.rag_services import handle_query
from services.auth_service import get_current_user
from services.history_service import get_user_history
from db.database import SessionLocal
from db.models import User
from services.auth_service import hash_password
from services.auth_service import verify_password,create_access_token
from fastapi import Depends
from fastapi import HTTPException
from services.journal_services import add_journal_entry, get_user_journal_history


router=APIRouter()

class UserSignup(BaseModel):
    username:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

class JournalRequest(BaseModel):
    text:str

class QueryRequest(BaseModel):
    query:str

@router.get("/")
def root():
    return{
        "message":"AI-ASSISTANT-API is running"
    }

@router.post("/ask")
def ask_question(request:QueryRequest,user=Depends(get_current_user)):
    user_id= user["user_id"]
    response=handle_query(request.query,user_id)
    save_user_history(user_id,request.query,response)
    return{"answer":response}

@router.post("/add-entry")
def add_entry(request:JournalRequest,user=Depends(get_current_user)):
    user_id=user["user_id"]
    entry_id= add_journal_entry(request.text,user_id)
    return{"message":"Entry added","id":entry_id}

@router.get("/history")
def history(user=Depends(get_current_user)):
    user_id=user["user_id"]
    history= get_user_history(user_id)

    return {"history":history}

@router.post("/signup")

def signup(request:UserSignup):
    db=SessionLocal()

    existing=db.query(User).filter(User.username==request.username).first()

    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pw=hash_password(request.password)

    new_user=User(username=request.username,password=hashed_pw)

    db.add(new_user)
    db.commit()

    db.close()

    return {"message":"User created successfully"}

@router.post("/login")
def login(request:UserLogin):
    db=SessionLocal()
    
    user=db.query(User).filter(User.username==request.username).first()

    if not user:
        db.close()
        raise HTTPException(status_code=400, detail="Invalid username")
    
    if not verify_password(request.password,user.password):
        db.close()
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token= create_access_token({"user_id":user.id})

    db.close()

    return{"access_token": token}


@router.get("/journal-history")
def journal_history(user=Depends(get_current_user)):
    user_id = user["user_id"]
    history = get_user_journal_history(user_id)
    return {"history": history}


