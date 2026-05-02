from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import date

class PopularWritingBase(BaseModel):
    title: str
    writing_type: str
    publisher_agency: Optional[str] = None
    date: date
    sr_no: Optional[int] = None
    department: Optional[str] = None

class PopularWritingCreate(PopularWritingBase):
    document: Optional[str] = None

class PopularWritingUpdate(BaseModel):
    title: Optional[str] = None
    writing_type: Optional[str] = None
    publisher_agency: Optional[str] = None
    date: Optional[date] = None
    api_score_faculty: Optional[float] = None
    api_score_hod: Optional[float] = None
    api_score_director: Optional[float] = None
    sr_no: Optional[int] = None
    department: Optional[str] = None
    document: Optional[str] = None

class PopularWritingResponse(PopularWritingBase):
    id: UUID
    faculty_id: UUID
    api_score_faculty: float
    api_score_hod: float
    api_score_director: float
    document: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class PopularWritingSummary(BaseModel):
    total_score: float
