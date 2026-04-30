from pydantic import BaseModel, Field
from typing import Optional

class SocialContributionBase(BaseModel):
    sr_no: Optional[int] = None
    activity_type: str = Field(..., max_length=255)
    details_of_activity: str

class SocialContributionCreate(SocialContributionBase):
    pass

class SocialContributionUpdateFaculty(BaseModel):
    activity_type: Optional[str] = Field(None, max_length=255)
    details_of_activity: Optional[str] = None
    api_score_faculty: Optional[float] = None

class SocialContributionUpdateHOD(BaseModel):
    api_score_hod: float

class SocialContributionUpdateDirector(BaseModel):
    api_score_director: float

class SocialContributionResponse(SocialContributionBase):
    id: int
    faculty_id: int
    api_score_faculty: float
    api_score_hod: float
    api_score_director: float

    class Config:
        from_attributes = True
