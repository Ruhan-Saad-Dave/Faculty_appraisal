from pydantic import BaseModel, Field, computed_field
from typing import Optional

class StudentFeedbackBase(BaseModel):
    sr_no: Optional[int] = None
    course_code_name: str = Field(..., max_length=255)
    first_feedback: float = Field(..., ge=0, le=5)
    second_feedback: float = Field(..., ge=0, le=5)

class StudentFeedbackCreate(StudentFeedbackBase):
    pass

class StudentFeedbackUpdateFaculty(BaseModel):
    course_code_name: Optional[str] = Field(None, max_length=255)
    first_feedback: Optional[float] = Field(None, ge=0, le=5)
    second_feedback: Optional[float] = Field(None, ge=0, le=5)

class StudentFeedbackUpdateHOD(BaseModel):
    api_score_hod: float

class StudentFeedbackUpdateDirector(BaseModel):
    api_score_director: float

class StudentFeedbackResponse(StudentFeedbackBase):
    id: int
    faculty_id: int
    api_score_faculty: float
    api_score_hod: float
    api_score_director: float

    class Config:
        from_attributes = True

    @computed_field
    @property
    def average(self) -> float:
        return (self.first_feedback + self.second_feedback) / 2
