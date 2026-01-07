from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.router import api_router

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="""
## Notes API with Version History

A FastAPI-based backend for a note-taking application with version history.

### Features:
- **User Authentication**: Register and login with JWT tokens
- **Notes Management**: CRUD operations for notes
- **Version History**: Track changes to notes with version control
- **Restore Versions**: Restore notes to previous versions

### Authentication:
Protected endpoints require a Bearer token in the Authorization header.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    from app.db.database import engine, Base
    from app.models.user import User
    from app.models.note import Note, NoteVersion
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint returning API information."""
    return {
        "message": "Welcome to Notes API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred",
            "type": type(exc).__name__
        }
    )
