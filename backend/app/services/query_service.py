from app.config import settings
import chromadb
from chromadb import Client
from sentence_transformers import SentenceTransformer
from typing import Optional, List
from fastapi import Query
from app.services import document_registry

model = SentenceTransformer(settings.MODEL_NAME)
chroma = chromadb.PersistentClient(settings.VECTOR_DB_DIR)


def format_citation(meta: dict) -> str:
    doc_id = meta.get("doc_id", "UNKNOWN")
    sent_idx = meta.get("sentence_index", "?")
    return f"{doc_id}, Sentence {sent_idx}"


def process_query(query: str, selected_docs: Optional[List[str]] = None, top_k: int = 10) -> dict:
    embedding = model.encode([query])
    collection = chroma.get_or_create_collection(name=settings.CHROMA_COLLECTION)

    # Apply document filtering if provided
    where_clause = {"doc_id": {"$in": selected_docs}} if selected_docs else {}

    results = collection.query(
        query_embeddings=embedding,
        n_results=top_k,
        where=where_clause if selected_docs else None
    )

    response_data = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, meta, score in zip(documents, metadatas, distances):
        citation = format_citation(meta)
        response_data.append({
            "sentence": doc,
            "citation": citation,
            "score": score,
            "doc_id": meta.get("doc_id")
        })

    # Cache top relevance scores for filtering
    doc_scores = {}
    for meta, score in zip(metadatas, distances):
        doc_id = meta.get("doc_id")
        if doc_id and (doc_id not in doc_scores or score > doc_scores[doc_id]):
            doc_scores[doc_id] = score
    document_registry.update_relevance_scores(doc_scores)

    return {
        "query": query,
        "results": response_data
    }

def query_documents(query: str, top_k: int = 10):
    results = vector_store.search(query, top_k=top_k)  # pseudo code, your actual call may differ

    # Update _relevance_cache here:
    for doc, score in results:
        _relevance_cache[doc.id] = score

    return results


def list_documents(author: Optional[str] = Query(None), date: Optional[str] = Query(None)) -> List[dict]:
    # Returns the full list from registry with optional filtering logic
    docs = document_registry.list_documents()
    if author:
        docs = [d for d in docs if d.get("author") == author]
    if date:
        docs = [d for d in docs if d.get("upload_date") == date]

    return docs
