import os
import sys
import pytest
from typing import Generator

# Set test environment variable before any app imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Now import app modules - they will use the test DATABASE_URL
from app.db.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.models.note import Note, NoteVersion
from app.main import app


# Create test engine with in-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client."""
    # Override the database dependency
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user_token(client, test_user) -> str:
    """Get an authentication token for the test user."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "testpassword123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(test_user_token) -> dict:
    """Get authorization headers for authenticated requests."""
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture
def test_note(db, test_user) -> Note:
    """Create a test note."""
    note = Note(
        title="Test Note",
        content="Test content",
        owner_id=test_user.id
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    
    # Create initial version
    version = NoteVersion(
        note_id=note.id,
        version_number=1,
        title=note.title,
        content=note.content,
        editor_id=test_user.id
    )
    db.add(version)
    db.commit()
    
    return note
