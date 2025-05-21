from pydantic import BaseModel
from typing import List

class DocumentUpload(BaseModel):
    filename: str
    content: str
    metadata: dict

class QueryRequest(BaseModel):
    query: str
    selected_docs: List[str] = []

class ThemeResponse(BaseModel):
    theme: str
    supporting_docs: List[str]
    citations: List[str]
