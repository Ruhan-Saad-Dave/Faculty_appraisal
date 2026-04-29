from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Base schema for common attributes
class ResearchAwardBase(BaseModel):
    award_name: str = Field(..., max_length=500)
    award_date: date
    awarding_agency: str = Field(..., max_length=255)
    level: str = Field(..., max_length=50) # International / National

# Schema for creating a new Research Award entry (Faculty input)
class ResearchAwardCreate(ResearchAwardBase):
    pass

# Schema for faculty to update their own Research Award entry
class ResearchAwardUpdateFaculty(ResearchAwardBase):
    award_name: Optional[str] = Field(None, max_length=500)
    award_date: Optional[date] = None
    awarding_agency: Optional[str] = Field(None, max_length=255)
    level: Optional[str] = Field(None, max_length=50)

# Schema for HOD to update API score
class ResearchAwardUpdateHOD(BaseModel):
    research_score_hod: float

# Schema for Director to update API score
class ResearchAwardUpdateDirector(BaseModel):
    research_score_director: float

# Schema for API response
class ResearchAwardResponse(ResearchAwardBase):
    id: int
    faculty_id: int
    research_score_faculty: float
    research_score_hod: float
    research_score_director: float

    class Config:
        from_attributes = True

# Schema for total score summary
class ResearchAwardSummary(BaseModel):
    total_score: float
