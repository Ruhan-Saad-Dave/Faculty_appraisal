from pydantic import BaseModel, Field
from typing import Optional

class QualificationEnhancementBase(BaseModel):
    sr_no: Optional[int] = None
    qualification_type: str = Field(..., max_length=255)
    department: Optional[str] = None
    document: Optional[str] = None

class QualificationEnhancementCreate(QualificationEnhancementBase):
    pass

class QualificationEnhancementUpdateFaculty(QualificationEnhancementBase):
    qualification_type: Optional[str] = Field(None, max_length=255)
    department: Optional[str] = None

class QualificationEnhancementUpdateHOD(BaseModel):
    api_score_hod: float

class QualificationEnhancementUpdateDirector(BaseModel):
    api_score_director: float

class QualificationEnhancementResponse(QualificationEnhancementBase):
    id: str
    faculty_id: str
    api_score_faculty: float
    api_score_hod: float
    api_score_director: float

    class Config:
        from_attributes = True
