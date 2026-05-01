from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

class FacultyBase(BaseModel):
    employee_id: Optional[str] = None
    name: Optional[str] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    department: Optional[str] = None
    experience: Optional[int] = None
    phone: Optional[str] = None
    academic_year: Optional[str] = None

class FacultyUpdate(FacultyBase):
    pass

class FacultyResponse(FacultyBase):
    id: UUID
    email: EmailStr
    role: str
    school_id: Optional[UUID] = None

    class Config:
        from_attributes = True
