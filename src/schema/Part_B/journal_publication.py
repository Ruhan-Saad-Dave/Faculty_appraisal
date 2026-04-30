from pydantic import BaseModel, Field
from typing import Optional
from ...models.Part_B.journal_publication import IndexingEnum # Corrected import path

class JournalPublicationBase(BaseModel):
    sr_no: Optional[int] = None
    title_with_page_nos: Optional[str] = Field(None, max_length=65535) # TEXT in DB
    journal_details: Optional[str] = Field(None, max_length=65535) # TEXT in DB
    issn_isbn_no: Optional[str] = Field(None, max_length=50)
    indexing: Optional[IndexingEnum] = None
    department: Optional[str] = None # Added as per user request
    document: Optional[str] = None # Added as per user request (Google Drive link)

class JournalPublicationCreate(JournalPublicationBase):
    pass

class JournalPublicationUpdateFaculty(JournalPublicationBase):
    pass

class JournalPublicationUpdateHOD(BaseModel):
    api_score_hod: Optional[float] = None

class JournalPublicationUpdateDirector(BaseModel):
    api_score_director: Optional[float] = None

class JournalPublicationResponse(JournalPublicationBase):
    id: str
    faculty_id: str
    api_score_faculty: int
    api_score_hod: float
    api_score_director: float

    class Config:
        from_attributes = True

class JournalPublicationSummary(BaseModel):
    total_score: float = Field(..., description="Total score for published papers in journals (max 120)")