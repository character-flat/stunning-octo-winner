from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the note")
    content: str = Field(..., min_length=1, description="Content of the note")


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Title of the note")
    content: Optional[str] = Field(None, min_length=1, description="Content of the note")


class NoteVersionResponse(BaseModel):
    id: int
    note_id: int
    title: str
    content: str
    version_number: int
    created_at: datetime

    class Config:
        from_attributes = True


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteDetailResponse(NoteResponse):
    versions: List[NoteVersionResponse] = []

    class Config:
        from_attributes = True
