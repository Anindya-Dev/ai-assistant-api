def build_rag_prompt(context: str, query:str):
    return f"""
You are an assistant.

Use ONLY the context below to answer the question.
If answer is not present, say "I couldn't find this in your data."

Context:
{context}

Question:
{query}
"""


def build_rewrite_prompt(query: str):
    return f"""
Rewrite this into one short search query for a personal journal entry.

Return only the rewritten query.
Do not explain.
Do not use bullets.
Do not use quotes.

Query:
{query}
"""
