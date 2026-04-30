from pydantic import BaseModel, Field
from typing import Optional

class UniversityActivityBase(BaseModel):
    sr_no: Optional[int] = None
    activity: str = Field(..., max_length=255)
    nature_of_activity: str
    department: Optional[str] = None
    document: Optional[str] = None

class UniversityActivityCreate(UniversityActivityBase):
    pass

class UniversityActivityUpdateFaculty(BaseModel):
    activity: Optional[str] = Field(None, max_length=255)
    nature_of_activity: Optional[str] = None
    department: Optional[str] = None

class UniversityActivityUpdateHOD(BaseModel):
    api_score_hod: float

class UniversityActivityUpdateDirector(BaseModel):
    api_score_director: float

class UniversityActivityResponse(UniversityActivityBase):
    id: str
    faculty_id: str
    api_score_faculty: float
    api_score_hod: float
    api_score_director: float

    class Config:
        from_attributes = True
