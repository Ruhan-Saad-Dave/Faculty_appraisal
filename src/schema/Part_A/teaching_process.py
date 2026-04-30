from pydantic import BaseModel, Field
from typing import Optional

class TeachingProcessBase(BaseModel):
    sr_no: Optional[int] = None
    semester: str = Field(..., max_length=50)
    course_code_name: str = Field(..., max_length=255)
    planned_classes: int
    conducted_classes: int

class TeachingProcessCreate(TeachingProcessBase):
    pass

class TeachingProcessUpdateFaculty(BaseModel):
    semester: Optional[str] = Field(None, max_length=50)
    course_code_name: Optional[str] = Field(None, max_length=255)
    planned_classes: Optional[int] = None
    conducted_classes: Optional[int] = None

class TeachingProcessUpdateHOD(BaseModel):
    api_score_hod: float
    signature: Optional[bool] = None

class TeachingProcessResponse(TeachingProcessBase):
    id: int
    faculty_id: int
    api_score_faculty: float
    api_score_hod: float
    signature: bool

    class Config:
        from_attributes = True
