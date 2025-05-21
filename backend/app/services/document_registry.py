import json
import os
from datetime import datetime
from threading import Lock

_relevance_cache = {}
_relevance_lock = Lock()

REGISTRY_PATH = "data/document_registry.json"
_lock = Lock()


_relevance_cache = {}
def update_relevance_scores(doc_scores: dict):
    global _relevance_cache
    with _relevance_lock:
        _relevance_cache.update(doc_scores)

def get_relevance(doc_id: str):
    with _relevance_lock:
        return _relevance_cache.get(doc_id, 0)

def get_documents_filtered(author=None, date=None, doc_type=None, min_relevance=None):
    docs = _load_registry()
    results = []

    for doc in docs:
        if author and doc.get("author") != author:
            continue
        if date and doc.get("upload_date") != date:
            continue
        if doc_type and doc.get("doc_type") != doc_type:
            continue

        relevance = get_relevance(doc["doc_id"])
        if min_relevance and relevance < min_relevance:
            continue

        doc_with_relevance = doc.copy()
        doc_with_relevance["relevance_score"] = relevance
        results.append(doc_with_relevance)

    return results



def _load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return []
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_registry(data):
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_document(doc_id: str, filename: str, doc_type: str, author: str = None):
    with _lock:
        registry = _load_registry()
        # Check for duplicates (doc_id)
        if any(doc["doc_id"] == doc_id for doc in registry):
            return  # already registered

        entry = {
            "doc_id": doc_id,
            "filename": filename,
            "doc_type": doc_type,
            "author": author or "Unknown",
            "upload_date": datetime.now().strftime("%Y-%m-%d")
        }
        registry.append(entry)
        _save_registry(registry)

def list_documents(author: str = None, date: str = None, doc_type: str = None):
    registry = _load_registry()
    filtered = []

    for doc in registry:
        if author and doc.get("author") != author:
            continue
        if date and doc.get("upload_date") != date:
            continue
        if doc_type and doc.get("doc_type") != doc_type:
            continue
        filtered.append(doc)
    return filtered
