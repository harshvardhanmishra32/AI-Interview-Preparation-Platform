"""ChromaDB persistent client integration for storing and querying resume embeddings."""
from pathlib import Path
from app.core.config import settings

try:
    import chromadb
except ImportError:  # ChromaDB is optional for lightweight serverless deployments.
    chromadb = None

# Global client cache
_chroma_client = None

def get_chroma_client():
    """Initialize or return the persistent ChromaDB client."""
    if chromadb is None:
        raise RuntimeError("ChromaDB is not installed in this deployment.")
    global _chroma_client
    if _chroma_client is None:
        # Create persistent path directory
        Path(settings.CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
    return _chroma_client

def get_or_create_collection(name: str):
    """Retrieve or create a ChromaDB collection by name."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )

def add_resume_embeddings(user_id: int, resume_text: str, metadata: dict) -> None:
    """Add or update a candidate's resume embeddings in ChromaDB."""
    if chromadb is None:
        return
    collection = get_or_create_collection("resumes")
    # Cast user_id to string for ChromaDB ID requirements
    doc_id = str(user_id)
    
    collection.upsert(
        ids=[doc_id],
        documents=[resume_text],
        metadatas=[metadata]
    )

def query_similar_resumes(query_text: str, n_results: int = 5) -> list[dict]:
    """Query ChromaDB for resumes similar to query_text."""
    if chromadb is None:
        return []
    collection = get_or_create_collection("resumes")
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    formatted_results = []
    if results and results.get("documents"):
        docs = results["documents"][0]
        ids = results["ids"][0]
        metadatas = results["metadatas"][0]
        distances = results.get("distances", [[]])[0]
        
        for i in range(len(docs)):
            formatted_results.append({
                "user_id": int(ids[i]),
                "resume_text": docs[i],
                "metadata": metadatas[i],
                "score": 1 - distances[i] if i < len(distances) else None
            })
            
    return formatted_results
