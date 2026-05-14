from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

# Read dashboard HTML
DASHBOARD_HTML = None
def load_dashboard():
    global DASHBOARD_HTML
    try:
        if os.path.exists("public/index.html"):
            with open("public/index.html", "r") as f:
                DASHBOARD_HTML = f.read()
    except:
        pass

@app.on_event("startup")
async def startup_event():
    load_dashboard()
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}. Continuing without DB persistence.")

@app.get("/", response_class=HTMLResponse)
def root():
    if DASHBOARD_HTML:
        return DASHBOARD_HTML
    return """
    <html>
        <head><title>AI Trade Engine</title></head>
        <body><h1>AI Trade Engine Backend</h1><p>Use /api/* endpoints</p></body>
    </html>
    """

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    if DASHBOARD_HTML:
        return DASHBOARD_HTML
    return {"message": "Dashboard not available"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
