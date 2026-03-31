from services.llm_service import generate_response
from db.chroma import search_chroma
from services.embedding_service import generate_embedding

def search_documents(query: str,user_id: int):
    query_embedding=generate_embedding(query)
    results=search_chroma(query_embedding,user_id)

    documents= results["documents"][0] if results ["documents"] else []
    distances= results["distances"][0] if results["distances"] else []
    return{
        "documents":documents,
        "distances":distances
    }

def answer_directly(query: str):
    return generate_response(query)