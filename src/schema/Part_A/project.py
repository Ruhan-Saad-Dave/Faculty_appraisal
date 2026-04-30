from pydantic import BaseModel, Field
from typing import Optional

class ProjectPartABase(BaseModel):
    sr_no: Optional[int] = None
    project_type: str = Field(..., max_length=255)
    department: Optional[str] = None
    document: Optional[str] = None

class ProjectPartACreate(ProjectPartABase):
    pass

class ProjectPartAUpdateFaculty(ProjectPartABase):
    project_type: Optional[str] = Field(None, max_length=255)
    department: Optional[str] = None

class ProjectPartAUpdateHOD(BaseModel):
    api_score_hod: float

class ProjectPartAUpdateDirector(BaseModel):
    api_score_director: float

class ProjectPartAResponse(ProjectPartABase):
    id: str
    faculty_id: str
    api_score_faculty: float
    api_score_hod: float
    api_score_director: float

    class Config:
        from_attributes = True
