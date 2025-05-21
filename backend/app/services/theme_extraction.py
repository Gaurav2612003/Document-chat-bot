from collections import defaultdict
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def identify_themes(responses):
    if not responses:
        return {}  # Or an empty theme struc
    # responses is a list of dicts with keys: sentence, citation, score, doc_id
    sentences = [r["sentence"] for r in responses]
    embeddings = model.encode(sentences)

    # Cluster the sentence embeddings
    num_clusters = min(3, len(sentences))  # Prevent crash with <3 items
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(embeddings)

    # Group by cluster label
    theme_groups = defaultdict(list)
    for i, label in enumerate(kmeans.labels_):
        theme_groups[label].append(responses[i])

    # Create a summary theme per group (e.g. top representative sentence)
    themes_output = {}
    for cluster_id, group in theme_groups.items():
        representative_sentence = group[0]["sentence"]  # Simple heuristic
        citations = []

        for item in group:
            citation = {
                "doc_id": item.get("doc_id", "UNKNOWN"),
                "sentence_index": int(item["citation"].split("Sentence")[-1].strip()) if "Sentence" in item["citation"] else -1
            }
            citations.append(citation)

        themes_output[f"Theme {cluster_id + 1}"] = {
            "theme": representative_sentence,
            "citations": citations
        }

    return themes_output
