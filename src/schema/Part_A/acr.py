from pydantic import BaseModel, Field
from typing import Optional

class ACRBase(BaseModel):
    sr_no: Optional[int] = None
    subject: str = Field(..., max_length=255)

class ACRCreate(ACRBase):
    faculty_id: int

class ACRUpdateHOD(BaseModel):
    api_score_hod: float

class ACRUpdateDirector(BaseModel):
    api_score_director: float
    signature: Optional[bool] = None

class ACRResponse(ACRBase):
    id: int
    faculty_id: int
    api_score_hod: float
    api_score_director: float
    signature: bool

    class Config:
        from_attributes = True
