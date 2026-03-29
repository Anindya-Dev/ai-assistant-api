from sentence_transformers import SentenceTransformer

model= SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text:str):
    embedding=model.encode(text)
    return embedding.tolist() #numpy array → not JSON serializable but list → storable / transferable
