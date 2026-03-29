import chromadb
from chromadb.config import Settings

client=chromadb.Client(
    Settings(
        persist_directory="./chroma_db"
    )
)

collection= client.get_or_create_collection(name="journal_entries")

def add_to_chroma(entry_id:int,text:str,embedding:list):
    collection.add(
        ids=[str(entry_id)],
        documents=[text],
        embeddings=[embedding]
    )


def search_chroma(query_embedding:list,top_k:int=3):
    result= collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return result