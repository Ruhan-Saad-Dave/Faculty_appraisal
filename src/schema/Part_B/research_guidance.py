from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Base schema for common attributes
class ResearchGuidanceBase(BaseModel):
    degree: str = Field(..., max_length=20)
    student_name: str = Field(..., max_length=255)
    submission_status: str
    award_date: Optional[date] = None
    department: Optional[str] = Field(None, description="Department of the faculty") # Added as per user request
    document: Optional[str] = Field(None, description="Google Drive link to the document") # Added as per user request

# Schema for creating a new Research Guidance entry (Faculty input)
class ResearchGuidanceCreate(ResearchGuidanceBase):
    pass

# Schema for faculty to update their own Research Guidance entry
class ResearchGuidanceUpdateFaculty(ResearchGuidanceBase):
    degree: Optional[str] = Field(None, max_length=20)
    student_name: Optional[str] = Field(None, max_length=255)
    submission_status: Optional[str] = None
    award_date: Optional[date] = None

# Schema for HOD to update API score
class ResearchGuidanceUpdateHOD(BaseModel):
    api_score_hod: float

# Schema for Director to update API score
class ResearchGuidanceUpdateDirector(BaseModel):
    api_score_director: float

# Schema for API response
class ResearchGuidanceResponse(ResearchGuidanceBase):
    id: int
    faculty_id: int
    api_score_faculty: float
    api_score_hod: float
    api_score_director: float

    class Config:
        from_attributes = True

# Schema for total score summary
class ResearchGuidanceSummary(BaseModel):
    total_score: float
    total_students_me: Optional[int] = None
    total_students_phd: Optional[int] = None
