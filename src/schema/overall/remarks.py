from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class AppraisalRemarksBase(BaseModel):
    remarks: Optional[str] = None
    department: Optional[str] = None
    document: Optional[str] = None

class AppraisalRemarksCreate(AppraisalRemarksBase):
    faculty_id: UUID

class AppraisalRemarksResponse(AppraisalRemarksBase):
    id: UUID
    faculty_id: UUID

    class Config:
        from_attributes = True

class HODRemarksBase(BaseModel):
    hod_remark: Optional[str] = None
    hod_approved_score: float = 0.0
    hod_signature: Optional[str] = None
    department: Optional[str] = None
    document: Optional[str] = None

class HODRemarksCreate(HODRemarksBase):
    faculty_id: UUID

class HODRemarksResponse(HODRemarksBase):
    id: UUID
    faculty_id: UUID

    class Config:
        from_attributes = True

class DirectorRemarksBase(BaseModel):
    director_remark: Optional[str] = None
    director_approved_score: float = 0.0
    director_signature: Optional[str] = None
    department: Optional[str] = None
    document: Optional[str] = None

class DirectorRemarksCreate(DirectorRemarksBase):
    faculty_id: UUID

class DirectorRemarksResponse(DirectorRemarksBase):
    id: UUID
    faculty_id: UUID

    class Config:
        from_attributes = True

class DeanRemarksBase(BaseModel):
    dean_remark: Optional[str] = None
    dean_approved_score: float = 0.0
    dean_signature: Optional[str] = None
    department: Optional[str] = None
    document: Optional[str] = None

class DeanRemarksCreate(DeanRemarksBase):
    faculty_id: UUID

class DeanRemarksResponse(DeanRemarksBase):
    id: UUID
    faculty_id: UUID

    class Config:
        from_attributes = True

class FinalApprovalBase(BaseModel):
    final_score: float = 0.0
    final_grade: Optional[str] = None
    vc_approval: Optional[str] = None
    department: Optional[str] = None
    document: Optional[str] = None

class FinalApprovalCreate(FinalApprovalBase):
    faculty_id: UUID

class FinalApprovalResponse(FinalApprovalBase):
    id: UUID
    faculty_id: UUID

    class Config:
        from_attributes = True
