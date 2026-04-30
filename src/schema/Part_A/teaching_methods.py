from pydantic import BaseModel, Field
from typing import Optional

class TeachingMethodsBase(BaseModel):
    sr_no: Optional[int] = None
    short_description: str = Field(..., max_length=255)
    details_proof: bool = False

class TeachingMethodsCreate(TeachingMethodsBase):
    pass

class TeachingMethodsUpdateFaculty(BaseModel):
    short_description: Optional[str] = Field(None, max_length=255)
    details_proof: Optional[bool] = None

class TeachingMethodsUpdateHOD(BaseModel):
    api_score_hod: float
    signature: Optional[bool] = None

class TeachingMethodsResponse(TeachingMethodsBase):
    id: int
    faculty_id: int
    api_score_faculty: float
    api_score_hod: float
    signature: bool

    class Config:
        from_attributes = True
