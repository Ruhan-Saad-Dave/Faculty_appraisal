from pydantic import BaseModel, Field
from typing import Optional

class CourseFileBase(BaseModel):
    sr_no: Optional[int] = None
    course_paper: str = Field(..., max_length=255)
    title: str = Field(..., max_length=255)
    details_proof: bool = False

class CourseFileCreate(CourseFileBase):
    pass

class CourseFileUpdateFaculty(BaseModel):
    course_paper: Optional[str] = Field(None, max_length=255)
    title: Optional[str] = Field(None, max_length=255)
    details_proof: Optional[bool] = None

class CourseFileUpdateHOD(BaseModel):
    api_score_hod: float
    signature: Optional[bool] = None

class CourseFileResponse(CourseFileBase):
    id: int
    faculty_id: int
    api_score_faculty: float
    api_score_hod: float
    signature: bool

    class Config:
        from_attributes = True
