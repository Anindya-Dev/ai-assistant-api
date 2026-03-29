from fastapi import APIRouter
from pydantic import BaseModel
from services.rag_services import handle_query

router=APIRouter()

class QueryRequest(BaseModel):
    query:str

@router.post("/ask")
def ask_question(request:QueryRequest):
    response=handle_query(request.query)
    return{"answer":response}