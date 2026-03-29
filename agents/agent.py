def run_agent(query: str):
    query_lower=query.lower()

    if "my" in query_lower or "did i" in query_lower:
        return{
            "tool":"search_documents",
            "query":query
        }
    else:
        return{
            "tool":"answer_directly",
            "query":query
        }