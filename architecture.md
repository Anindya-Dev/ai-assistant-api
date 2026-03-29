1. Client:
User sends query via frontend / API call

2. FastAPI Layer:
Receives request
Authenticates user (JWT)
Passes query to service layer

3. Service Layer (Core Logic):
- Decides whether to use RAG or direct LLM
- Handles retry logic
- Handles query rewriting
- Applies similarity threshold check
- Controls full workflow

4. Agent Layer:
- Uses tools:
   → search_documents (RAG)
   → answer_directly (LLM)
- LLM decides tool usage based on descriptions

5. Retrieval Layer:
- Converts query to embedding (sentence-transformers)
- Searches ChromaDB
- Returns top-k chunks + similarity scores

6. LLM Layer:
- (Groq + Llama 3.3 70B)
- Generates:
   → query rewrite (if needed)
   → final grounded answer
- Uses strict prompt + context injection

7. Database Layer:
- SQLite:
   → user data
   → conversation history
- ChromaDB:
   → embeddings + documents

8. Observability (logs/debug):
- Log:
   → query
   → similarity score
   → retry count
   → success/failure