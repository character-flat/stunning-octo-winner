from fastapi import FastAPI
from app.routes import notes_router

app = FastAPI(
    title="Notes API with Version History",
    description="A FastAPI-based backend for a note-taking application with version history",
    version="1.0.0",
)

# Include routers
app.include_router(notes_router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Notes API with Version History",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
