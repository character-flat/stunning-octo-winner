from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Note, NoteVersion
from app.schemas import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    NoteDetailResponse,
    NoteVersionResponse,
)

router = APIRouter(prefix="/notes", tags=["notes"])


def create_version(db: Session, note: Note, version_number: int):
    """Create a version snapshot of a note"""
    version = NoteVersion(
        note_id=note.id,
        title=note.title,
        content=note.content,
        version_number=version_number,
    )
    db.add(version)
    db.commit()


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note_data: NoteCreate, db: Session = Depends(get_db)):
    """Create a new note"""
    note = Note(title=note_data.title, content=note_data.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    
    # Create initial version (version 1)
    create_version(db, note, version_number=1)
    
    return note


@router.get("/", response_model=List[NoteResponse])
def list_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all notes with pagination"""
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes


@router.get("/{note_id}", response_model=NoteDetailResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """Get a specific note with its version history"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_data: NoteUpdate, db: Session = Depends(get_db)):
    """Update a note and create a new version"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    
    # Update note fields if provided
    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content
    
    db.commit()
    db.refresh(note)
    
    # Get the latest version number and create a new version
    latest_version = db.query(NoteVersion).filter(
        NoteVersion.note_id == note_id
    ).order_by(NoteVersion.version_number.desc()).first()
    
    new_version_number = (latest_version.version_number + 1) if latest_version else 1
    create_version(db, note, version_number=new_version_number)
    
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a note and all its versions"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    
    db.delete(note)
    db.commit()
    return None


@router.get("/{note_id}/versions", response_model=List[NoteVersionResponse])
def get_note_versions(note_id: int, db: Session = Depends(get_db)):
    """Get all versions of a note"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    
    versions = db.query(NoteVersion).filter(
        NoteVersion.note_id == note_id
    ).order_by(NoteVersion.version_number.desc()).all()
    
    return versions


@router.get("/{note_id}/versions/{version_number}", response_model=NoteVersionResponse)
def get_note_version(note_id: int, version_number: int, db: Session = Depends(get_db)):
    """Get a specific version of a note"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    
    version = db.query(NoteVersion).filter(
        NoteVersion.note_id == note_id,
        NoteVersion.version_number == version_number
    ).first()
    
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Version {version_number} not found for note {note_id}"
        )
    
    return version
