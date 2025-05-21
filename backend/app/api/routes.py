from fastapi import APIRouter, File, UploadFile, Form, Query
from fastapi import UploadFile, HTTPException
from app.services import file_parser, ocr_service, document_loader, query_service, theme_extraction
from app.models.document import QueryRequest
from fastapi import Query
from fastapi.responses import FileResponse
from app.services.export_service import export_to_csv, export_to_pdf
from typing import Optional 
import os
import uuid
from fastapi.responses import FileResponse
from typing import Optional 
from app.services import document_registry
from pydantic import BaseModel
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

"""
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".ppt", ".txt", ".png", ".jpg", ".jpeg"}

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Supported types are: {', '.join(SUPPORTED_EXTENSIONS)}")

    file_path = f"data/{file.filename}"
    os.makedirs("data", exist_ok=True)

    try:
        # Save the file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract content based on file type
        if ext == ".pdf":
            parsed = file_parser.extract_text_from_pdf(file_path)
        elif ext in (".docx", ".pptx", ".ppt", ".txt"):
            if ext == ".docx":
                raw_text = file_parser.extract_text_from_docx(file_path)
            elif ext in (".pptx", ".ppt"):
                raw_text = file_parser.extract_text_from_pptx(file_path)
            else:  # .txt
                raw_text = file_parser.extract_text_from_txt(file_path)

            parsed = file_parser.extract_paragraphs_with_metadata(
                raw_text,
                source_type=ext.lstrip("."),
                filename=file.filename
            )
        else:  # image types: .png, .jpg, .jpeg
            content = ocr_service.extract_text_from_image(file_path)
            parsed = file_parser.extract_paragraphs_with_metadata(
                content,
                source_type="image",
                filename=file.filename
            )

        doc_id = str(uuid.uuid4())
        document_loader.index_document(doc_id, parsed, metadata={"filename": file.filename})

        # Determine doc_type for registry
        if ext == ".pdf":
            doc_type = "pdf"
        elif ext == ".docx":
            doc_type = "docx"
        elif ext in (".pptx", ".ppt"):
            doc_type = "pptx"
        elif ext == ".txt":
            doc_type = "txt"
        else:
            doc_type = "image"

        document_registry.add_document(doc_id, file.filename, doc_type)
        return {"doc_id": doc_id, "filename": file.filename, "doc_type": doc_type}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
"""

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    logger.info(f"Received file with extension: {ext}")

    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    file_path = f"data/{file.filename}"
    os.makedirs("data", exist_ok=True)

    try:
        with open(file_path, "wb") as f:
            logger.info("Saving file...")
            f.write(await file.read())

        logger.info(f"File saved at: {file_path}")

        if ext == ".pdf":
            parsed = file_parser.extract_text_from_pdf(file_path)
        elif ext in (".docx", ".pptx", ".ppt", ".txt"):
            ...
        else:
            ...

        logger.info("Text extracted, indexing document...")
        doc_id = str(uuid.uuid4())
        document_loader.index_document(doc_id, parsed, metadata={"filename": file.filename})
        ...

        logger.info("Upload complete.")
        return {"doc_id": doc_id, "filename": file.filename, "doc_type": doc_type}

    except Exception as e:
        logger.exception("File processing failed:")
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")


@router.post("/query/")
async def query_docs(request: QueryRequest):
    results = query_service.process_query(request.query, request.selected_docs)
    themes = theme_extraction.identify_themes(results["results"])
    return {
        "matches": results,
        "themes": themes
    }

@router.get("/documents/")
def list_documents(
    author: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    doc_type: Optional[str] = Query(None),
    min_relevance: Optional[float] = Query(None)
):
    docs = document_registry.get_documents_filtered(
        author=author,
        date=date,
        doc_type=doc_type,
        min_relevance=min_relevance
    )
    return {"documents": docs}


@router.post("/export/")
def export_results(data: list[dict], file_type: str = "csv"):
    if file_type == "pdf":
        path = export_to_pdf(data)
    else:
        path = export_to_csv(data)
    return FileResponse(path, filename=os.path.basename(path), media_type="application/octet-stream")
