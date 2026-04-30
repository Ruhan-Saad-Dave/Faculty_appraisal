from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppraisalRemarksBase(BaseModel):
    remarks: Optional[str] = None
    department: Optional[str] = None
    document: Optional[str] = None

class AppraisalRemarksCreate(AppraisalRemarksBase):
    faculty_id: str

class AppraisalRemarksResponse(AppraisalRemarksBase):
    id: str
    faculty_id: str

    class Config:
        from_attributes = True

class HODRemarksBase(BaseModel):
    hod_remark: Optional[str] = None
    hod_approved_score: float = 0.0
    hod_signature: Optional[str] = None
    department: Optional[str] = None
    document: Optional[str] = None

class HODRemarksCreate(HODRemarksBase):
    faculty_id: str

class HODRemarksResponse(HODRemarksBase):
    id: str
    faculty_id: str

    class Config:
        from_attributes = True

class DirectorRemarksBase(BaseModel):
    director_remark: Optional[str] = None
    director_approved_score: float = 0.0
    director_signature: Optional[str] = None
    department: Optional[str] = None
    document: Optional[str] = None

class DirectorRemarksCreate(DirectorRemarksBase):
    faculty_id: str

class DirectorRemarksResponse(DirectorRemarksBase):
    id: str
    faculty_id: str

    class Config:
        from_attributes = True

class DeanRemarksBase(BaseModel):
    dean_remark: Optional[str] = None
    dean_approved_score: float = 0.0
    dean_signature: Optional[str] = None
    department: Optional[str] = None
    document: Optional[str] = None

class DeanRemarksCreate(DeanRemarksBase):
    faculty_id: str

class DeanRemarksResponse(DeanRemarksBase):
    id: str
    faculty_id: str

    class Config:
        from_attributes = True

class FinalApprovalBase(BaseModel):
    final_score: float = 0.0
    final_grade: Optional[str] = None
    vc_approval: Optional[str] = None
    department: Optional[str] = None
    document: Optional[str] = None

class FinalApprovalCreate(FinalApprovalBase):
    faculty_id: str

class FinalApprovalResponse(FinalApprovalBase):
    id: str
    faculty_id: str

    class Config:
        from_attributes = True
