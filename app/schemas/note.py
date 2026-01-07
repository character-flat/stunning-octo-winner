from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base note schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class NoteCreate(NoteBase):
    """Schema for creating a note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating a note."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)


class NoteResponse(NoteBase):
    """Schema for note response."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteVersionBase(BaseModel):
    """Base schema for note version."""
    version_number: int
    title: str
    content: str
    editor_id: int
    created_at: datetime


class NoteVersionResponse(NoteVersionBase):
    """Schema for note version response."""
    id: int
    note_id: int

    class Config:
        from_attributes = True


class NoteVersionListResponse(BaseModel):
    """Schema for listing note versions."""
    note_id: int
    versions: List[NoteVersionResponse]


class RestoreVersionRequest(BaseModel):
    """Schema for restoring a note to a previous version."""
    version_number: int = Field(..., gt=0)
