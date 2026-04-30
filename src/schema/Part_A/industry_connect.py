from pydantic import BaseModel, Field
from typing import Optional

class IndustryConnectBase(BaseModel):
    sr_no: Optional[int] = None
    industry_name: str = Field(..., max_length=255)
    details_of_activity: str

class IndustryConnectCreate(IndustryConnectBase):
    pass

class IndustryConnectUpdateFaculty(BaseModel):
    industry_name: Optional[str] = Field(None, max_length=255)
    details_of_activity: Optional[str] = None
    api_score_faculty: Optional[float] = None

class IndustryConnectUpdateHOD(BaseModel):
    api_score_hod: float

class IndustryConnectUpdateDirector(BaseModel):
    api_score_director: float

class IndustryConnectResponse(IndustryConnectBase):
    id: int
    faculty_id: int
    api_score_faculty: float
    api_score_hod: float
    api_score_director: float

    class Config:
        from_attributes = True
