from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

class EnclosureBase(BaseModel):
    enclosure_text: str

class EnclosureCreate(EnclosureBase):
    pass

class EnclosureResponse(EnclosureBase):
    id: UUID
    faculty_id: UUID
    document: Optional[str] = None

    class Config:
        from_attributes = True

class DeclarationBase(BaseModel):
    place: str
    designation: str

class DeclarationCreate(DeclarationBase):
    pass

class DeclarationResponse(DeclarationBase):
    id: UUID
    faculty_id: UUID
    submission_date: date

    class Config:
        from_attributes = True
