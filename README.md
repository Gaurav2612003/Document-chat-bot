# gaurav-joshi-wasserstoff-AiInternTask

Got it! Here’s the updated README.md including both backend and frontend details, plus deployment notes for both (with Vercel for frontend):

Document Research Chatbot
This project is a document research assistant with a chatbot interface.
It consists of:

Backend: FastAPI server for document upload, OCR extraction, semantic indexing, and query handling

Frontend: React-based web app (deployed on Vercel) to interact with the backend and chat with the bot

Features
Upload .pdf, .docx, .pptx, .txt, and image files

OCR and text extraction with Tesseract and EasyOCR

Sentence chunking and embedding using Sentence Transformers

Semantic search over uploaded documents with citation and relevance filtering

Interactive chatbot UI with document-aware responses

Document metadata management (author, date, type, relevance)

Backend Setup
1. Clone the repository
bash
https://github.com/Gaurav2612003/gaurav-joshi-wasserstoff-AiInternTask
cd backend
2. Create and activate a virtual environment
bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Install system dependencies
Tesseract-OCR
Poppler (optional for PDFs)
Example for Ubuntu:

bash
sudo apt install tesseract-ocr
5. Prepare folders and registry file
bash
touch data/document_registry.json
6. Run the backend server
bash
uvicorn app.main:app --reload
local host -
Access at http://localhost:8000
public host -
Access at http://15.206.92.180:8000/docs
Frontend Setup
The frontend is a Html,js eab app designed for interacting with the backend.

4. Run the frontend 
https://gaurav-joshi-wasserstoff-ai-intern-task.vercel.app/

Testing
Use tools like curl, Postman, or your frontend UI to:

Upload documents

Ask queries to the chatbot

List or filter documents

Deployment
Backend
Deploy on cloud VM (AWS Lightsail)

Use uvicorn with process manager (systemd, supervisor)

Frontend
Deploy on Vercel or any static hosting platform

Connect frontend API requests to your backend URL


Project Structure
chat_theme_indentifier
|  backend/
|  │
|  ├── app/
|  │   ├── main.py
|  │   ├── config.py
|  |   |---api/ routes.py
|  │   ├── services/
|  │   |    ├── theme_extraction.py
|  │   |    ├── ocr_service.py
|  │   |    ├── document_registry.py
|  │   |    |-- query_engine.py
|  |   |    |-- documnet_loader.py
|  |   |    |-- file_parser.py
|  |   |    |-- query_service.py
|  │   |---models/documents.py
|  ├── data/
|  |   |--uploaded-files
|  |   |--Documnet_registry
|  ├── export/exported files
|  ├── vectore_db/database
|  |---requirements.txt
|---frontend/
|  |
|  |--index.html  
|  |-- advance.html
|  |-- scripts.js
|  |--advance.js
|  |-- styele.css
├── .gitignore
└── README.md


Requirements
Example backend requirements:

nginx
Copy
Edit
fastapi
uvicorn
chromadb
sentence-transformers
nltk
pdfminer.six
python-docx
python-pptx
pytesseract
easyocr
opencv-python
scikit-learn
Pillow


fail : (The backend server runs public server on http://15.206.92.180:8000/docs)

The frontend runs public server on https://gaurav-joshi-wasserstoff-ai-intern-task.vercel.app

Note: Currently, the frontend and backend connection fails reason:
vercel runs on https and AWS lightsail runs on http only

Tried many solution free backend depolyment but due to large in size .
