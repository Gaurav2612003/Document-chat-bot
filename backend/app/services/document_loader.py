from nltk.tokenize import sent_tokenize
from app.config import settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import chromadb
import nltk
nltk.download('punkt_tab')

# Initialize ChromaDB client here if not already initialized
chroma = chromadb.PersistentClient(settings.VECTOR_DB_DIR)

embedding_fn = SentenceTransformerEmbeddingFunction(model_name=settings.MODEL_NAME)

def index_document(doc_id: str, content_blocks: list, metadata: dict = {}):
    collection = chroma.get_or_create_collection(
        name=settings.CHROMA_COLLECTION,
        embedding_function=embedding_fn
    )

    sentences = []
    metadatas = []
    ids = []

    for block_index, block in enumerate(content_blocks):
        block_text = block["text"]
        block_meta = block.get("metadata", {})

        page_number = block_meta.get("page_number")
        paragraph_number = block_meta.get("paragraph_number")

        split_sentences = sent_tokenize(block_text)

        for i, sentence in enumerate(split_sentences):
            sentences.append(sentence)

            # Build metadata and clean None values
            sentence_metadata = {
                **metadata,
                "doc_id": doc_id,
                "block_index": block_index,
                "sentence_index": i,
                "page_number": page_number if page_number is not None else "",
                "paragraph_number": paragraph_number if paragraph_number is not None else ""
            }

            # Optionally convert all values to string (if preferred)
            sentence_metadata = {k: (str(v) if v is not None else "") for k, v in sentence_metadata.items()}

            metadatas.append(sentence_metadata)
            ids.append(f"{doc_id}_b{block_index}_s{i}")

    collection.add(
        documents=sentences,
        metadatas=metadatas,
        ids=ids
    )
