from services.llm_service import generate_response

def run_agent(query: str):
    routing_prompt = f"""You are a query router.

Decide whether this query needs personal journal/memory search or a direct answer.

Query: "{query}"

Reply with exactly one word only:
search
direct
"""

    decision = generate_response(routing_prompt).strip().lower()

    if decision == "search":
        return {"tool": "search_documents", "query": query}
    elif decision == "direct":
        return {"tool": "answer_directly", "query": query}
    else:
        return {"tool": "answer_directly", "query": query}
