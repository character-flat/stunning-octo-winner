from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.note import Note, NoteVersion
from app.schemas.note import (
    NoteCreate, NoteUpdate, NoteResponse, 
    NoteVersionResponse, NoteVersionListResponse, RestoreVersionRequest
)
from app.api.deps import get_current_user

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new note.
    
    - **title**: Note title (1-255 characters)
    - **content**: Note content
    """
    db_note = Note(
        title=note_data.title,
        content=note_data.content,
        owner_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    # Create initial version (version 1)
    version = NoteVersion(
        note_id=db_note.id,
        version_number=1,
        title=db_note.title,
        content=db_note.content,
        editor_id=current_user.id
    )
    db.add(version)
    db.commit()
    
    return db_note


@router.get("/", response_model=List[NoteResponse])
def get_all_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all notes belonging to the current user.
    
    - **skip**: Number of notes to skip (pagination)
    - **limit**: Maximum number of notes to return
    """
    notes = db.query(Note).filter(
        Note.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific note by ID.
    
    - **note_id**: The ID of the note to retrieve
    """
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a note and create a new version.
    
    - **note_id**: The ID of the note to update
    - **title**: New title (optional)
    - **content**: New content (optional)
    """
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    # Track if changes were made
    changes_made = False
    
    if note_data.title is not None and note_data.title != note.title:
        note.title = note_data.title
        changes_made = True
    
    if note_data.content is not None and note_data.content != note.content:
        note.content = note_data.content
        changes_made = True
    
    if changes_made:
        # Get the current highest version number
        max_version = db.query(NoteVersion).filter(
            NoteVersion.note_id == note_id
        ).order_by(NoteVersion.version_number.desc()).first()
        
        new_version_number = (max_version.version_number + 1) if max_version else 1
        
        # Create new version
        version = NoteVersion(
            note_id=note.id,
            version_number=new_version_number,
            title=note.title,
            content=note.content,
            editor_id=current_user.id
        )
        db.add(version)
        db.commit()
        db.refresh(note)
    
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a note and all its versions.
    
    - **note_id**: The ID of the note to delete
    """
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    db.delete(note)
    db.commit()
    return None


# Version History Endpoints

@router.get("/{note_id}/versions", response_model=List[NoteVersionResponse])
def get_note_versions(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all versions of a note.
    
    - **note_id**: The ID of the note
    """
    # Check if note exists and belongs to user
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    versions = db.query(NoteVersion).filter(
        NoteVersion.note_id == note_id
    ).order_by(NoteVersion.version_number.desc()).all()
    
    return versions


@router.get("/{note_id}/versions/{version_number}", response_model=NoteVersionResponse)
def get_note_version(
    note_id: int,
    version_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific version of a note.
    
    - **note_id**: The ID of the note
    - **version_number**: The version number to retrieve
    """
    # Check if note exists and belongs to user
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    version = db.query(NoteVersion).filter(
        NoteVersion.note_id == note_id,
        NoteVersion.version_number == version_number
    ).first()
    
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Version {version_number} not found"
        )
    
    return version


@router.post("/{note_id}/restore", response_model=NoteResponse)
def restore_note_version(
    note_id: int,
    restore_data: RestoreVersionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Restore a note to a previous version.
    
    This creates a new version with the content from the specified version.
    
    - **note_id**: The ID of the note
    - **version_number**: The version number to restore to
    """
    # Check if note exists and belongs to user
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    # Get the version to restore
    version_to_restore = db.query(NoteVersion).filter(
        NoteVersion.note_id == note_id,
        NoteVersion.version_number == restore_data.version_number
    ).first()
    
    if not version_to_restore:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Version {restore_data.version_number} not found"
        )
    
    # Update the note with the old version's content
    note.title = version_to_restore.title
    note.content = version_to_restore.content
    
    # Get the current highest version number
    max_version = db.query(NoteVersion).filter(
        NoteVersion.note_id == note_id
    ).order_by(NoteVersion.version_number.desc()).first()
    
    new_version_number = max_version.version_number + 1
    
    # Create a new version (restore creates a new version)
    new_version = NoteVersion(
        note_id=note.id,
        version_number=new_version_number,
        title=note.title,
        content=note.content,
        editor_id=current_user.id
    )
    db.add(new_version)
    db.commit()
    db.refresh(note)
    
    return note
