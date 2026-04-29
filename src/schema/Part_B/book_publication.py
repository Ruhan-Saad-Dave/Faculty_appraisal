from pydantic import BaseModel, Field
from typing import Optional

# Base schema for common attributes
class BookPublicationBase(BaseModel):
    chapter_title: str = Field(..., max_length=255)
    book_details: str = Field(..., max_length=500)
    isbn: str = Field(..., max_length=50)
    publisher_type: str = Field(..., max_length=50)
    co_author_count: int
    is_first_author: bool

# Schema for creating a new book publication (Faculty input)
class BookPublicationCreate(BookPublicationBase):
    pass

# Schema for faculty to update their own book publication
class BookPublicationUpdateFaculty(BookPublicationBase):
    chapter_title: Optional[str] = Field(None, max_length=255)
    book_details: Optional[str] = Field(None, max_length=500)
    isbn: Optional[str] = Field(None, max_length=50)
    publisher_type: Optional[str] = Field(None, max_length=50)
    co_author_count: Optional[int] = None
    is_first_author: Optional[bool] = None

# Schema for HOD to update API score
class BookPublicationUpdateHOD(BaseModel):
    api_score_hod: float

# Schema for Director to update API score
class BookPublicationUpdateDirector(BaseModel):
    api_score_director: float

# Schema for API response
class BookPublicationResponse(BookPublicationBase):
    id: int
    faculty_id: int
    api_score_faculty: float
    api_score_hod: float
    api_score_director: float

    class Config:
        from_attributes = True

# Schema for total score summary
class BookPublicationSummary(BaseModel):
    total_score: float
