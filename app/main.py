from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routes import router as api_router
from app.db import init_db

app = FastAPI(title="AI Trade Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

# Serve static files
if os.path.exists("public"):
    app.mount("/public", StaticFiles(directory="public"), name="public")

@app.on_event("startup")
async def startup_event():
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}. Continuing without DB persistence.")

@app.get("/")
def root():
    if os.path.exists("public/index.html"):
        return FileResponse("public/index.html", media_type="text/html")
    return {"message": "AI Trade Engine backend is running. Use /api/* endpoints."}

@app.get("/dashboard")
def dashboard():
    if os.path.exists("public/index.html"):
        return FileResponse("public/index.html", media_type="text/html")
    return {"message": "Dashboard not available"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
