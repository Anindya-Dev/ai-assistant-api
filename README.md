# AI Assistant API

A FastAPI backend for a personal AI assistant with journal memory, retrieval-augmented generation, JWT authentication, and conversation history.

## Overview

This project lets a user:

- create an account and log in
- save private journal entries
- ask questions against personal journal memory
- retrieve chat history
- retrieve journal history

The application uses SQLite for relational data, ChromaDB for vector search, Sentence Transformers for embeddings, and Groq-hosted Llama for response generation.

## Features

- FastAPI-based REST API
- JWT authentication with bearer tokens
- Personal journal entry storage
- User-scoped semantic retrieval with ChromaDB metadata filtering
- RAG-style answer generation over stored journal entries
- Query rewrite retry loop for retrieval recovery
- Conversation history persistence
- Journal history endpoint

## Architecture

High-level request flow:

1. Client sends a request to the API.
2. FastAPI validates payloads and authenticates protected routes.
3. The service layer decides whether to use journal retrieval or direct generation.
4. Journal queries are embedded and searched in ChromaDB.
5. Matching journal content is injected into a grounded prompt.
6. Groq generates the final answer.
7. SQL history is stored in SQLite.

Current storage split:

- SQLite: users, journal entries, conversation history
- ChromaDB: journal entry embeddings and vector search metadata

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- ChromaDB
- Sentence Transformers
- Groq API
- python-jose for JWT
- passlib + bcrypt for password hashing

## Project Structure

```text
ai-assistant-api/
|-- agents/
|   |-- agent.py
|   |-- prompts.py
|   `-- tools.py
|-- db/
|   |-- chroma.py
|   |-- database.py
|   `-- models.py
|-- routes/
|   `-- assistant_routes.py
|-- services/
|   |-- auth_service.py
|   |-- history_service.py
|   |-- journal_services.py
|   |-- llm_service.py
|   `-- rag_services.py
|-- architecture.md
|-- main.py
`-- requirements.txt
```

## Prerequisites

- Python 3.11+
- A Groq API key

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_jwt_secret
```

Recommended:

- use a long random `SECRET_KEY`
- do not commit `.env`

## Installation

```bash
git clone https://github.com/Anindya-Dev/ai-assistant-api.git
cd ai-assistant-api
python -m venv .venv
```

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Authentication Flow

1. `POST /signup`
2. `POST /login`
3. Copy the returned JWT token
4. Use `Authorization: Bearer <token>` for protected routes

## API Endpoints

### `GET /`

Health-style root route.

Response:

```json
{
  "message": "AI-ASSISTANT-API is running"
}
```

### `POST /signup`

Create a new user.

Request:

```json
{
  "username": "alice",
  "password": "strong-password"
}
```

### `POST /login`

Authenticate and return a JWT access token.

Request:

```json
{
  "username": "alice",
  "password": "strong-password"
}
```

Response:

```json
{
  "access_token": "..."
}
```

### `POST /add-entry`

Add a journal entry for the authenticated user.

Headers:

```text
Authorization: Bearer <token>
```

Request:

```json
{
  "text": "I paid the electric bills today"
}
```

Response:

```json
{
  "message": "Entry added",
  "id": 1
}
```

### `POST /ask`

Ask the assistant a question. If the query looks personal, the API tries journal retrieval first; otherwise it falls back to direct generation.

Headers:

```text
Authorization: Bearer <token>
```

Request:

```json
{
  "query": "When did I pay the bills?"
}
```

Example response:

```json
{
  "answer": "You paid the electric bills today."
}
```

### `GET /journal-history`

Return the authenticated user's journal entries.

Headers:

```text
Authorization: Bearer <token>
```

Example response:

```json
{
  "history": [
    {
      "id": 1,
      "content": "I paid the electric bills today",
      "time": "2026-03-31T05:55:58.730226"
    }
  ]
}
```

### `GET /history`

Return the authenticated user's question/answer conversation history.

Headers:

```text
Authorization: Bearer <token>
```

Example response:

```json
{
  "history": [
    {
      "query": "When did I pay the bills?",
      "answer": "You paid the electric bills today.",
      "time": "2026-03-31T06:10:00.000000"
    }
  ]
}
```

## Retrieval Behavior

Current retrieval flow:

- route queries through a lightweight rule in `agents/agent.py`
- embed the query with `all-MiniLM-L6-v2`
- search ChromaDB with `user_id` filtering
- retry with rewritten queries when the first attempt is weak
- answer with journal context when the best result passes the similarity threshold

Important implementation note:

- query routing is currently heuristic-based, not a full autonomous tool-calling agent

## Local Data

Running the app creates local persistent data:

- `journal.db` for SQLite
- `chroma_db/` for Chroma persistence

If you need a fresh local reset during development, remove both and restart the server.

## Troubleshooting

### `no such column` in SQLite

`Base.metadata.create_all()` creates missing tables, but it does not migrate existing ones. If you change a model schema locally, either:

- reset the local database during development, or
- add proper migrations

### Chroma directory is not visible

Chroma persistence is directory-based, not a single `chroma.db` file. Look for the `chroma_db/` folder in the project root.

### Journal history exists but `/ask` cannot find it

Possible causes:

- the query wording is too far from the stored entry
- the retrieval threshold is too strict
- Chroma and SQLite were reset at different times

## Production Notes

This project is production-minded, but not fully production-hardened yet.

Before deploying to production, add:

- schema migrations with Alembic
- structured logging
- request validation and rate limiting
- secrets management
- test coverage
- proper error monitoring
- containerization and deployment config
- stronger auth and token management policies

