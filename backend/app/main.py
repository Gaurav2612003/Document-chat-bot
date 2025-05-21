from fastapi import FastAPI
from app.api.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Document Theme Chatbot")
app.include_router(api_router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["gaurav-joshi-wasserstoff-ai-intern-task.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


