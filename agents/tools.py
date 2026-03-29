from services.llm_service import generate_response
from db.chroma import search_chroma
from services.embedding_service import generate_embedding

def search_documents(query: str):
    query_embedding=generate_embedding(query)
    results=search_chroma(query_embedding)
    documents= results["documents"][0] if results ["documents"] else []
    if not documents:
        return "I couldn't find this in your data."

    context="\n".join(documents)
    prompt= f"""
You are an assistant.

Use ONLY the context below to answer the question.
If answer is not present, say "I couldn't find this in your data."

Context:
{context}

Question:
{query}
"""
    answer= generate_response(prompt)
    
    return answer


def answer_directly(query: str):
    return generate_response(query)