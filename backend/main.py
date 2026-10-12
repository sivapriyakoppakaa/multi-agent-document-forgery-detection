from fastapi import FastAPI
from routes.upload import router as upload_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Multi-Agent Document Forgery Detection System",
    description="Backend API for detecting forged documents using AI",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Multi-Agent Document Forgery Detection System"
    }