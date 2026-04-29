from pydantic import BaseModel, Field
from typing import Optional

# Base schema for common attributes
class SelfDevelopmentFDPBase(BaseModel):
    program_name: str = Field(..., max_length=255)
    duration_days: int
    organizer: str = Field(..., max_length=255)

# Schema for creating a new Self Development FDP entry (Faculty input)
class SelfDevelopmentFDPCreate(SelfDevelopmentFDPBase):
    pass

# Schema for faculty to update their own Self Development FDP entry
class SelfDevelopmentFDPUpdateFaculty(SelfDevelopmentFDPBase):
    program_name: Optional[str] = Field(None, max_length=255)
    duration_days: Optional[int] = None
    organizer: Optional[str] = Field(None, max_length=255)

# Schema for HOD to update API score
class SelfDevelopmentFDPUpdateHOD(BaseModel):
    api_score_hod: float

# Schema for Director to update API score
class SelfDevelopmentFDPUpdateDirector(BaseModel):
    api_score_director: float

# Schema for API response
class SelfDevelopmentFDPResponse(SelfDevelopmentFDPBase):
    id: int
    faculty_id: int
    api_score_faculty: float
    api_score_hod: float
    api_score_director: float

    class Config:
        from_attributes = True

# Schema for total score summary
class SelfDevelopmentFDPSummary(BaseModel):
    total_score: float
