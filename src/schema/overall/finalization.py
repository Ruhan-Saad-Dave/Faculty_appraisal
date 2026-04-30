from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EnclosureBase(BaseModel):
    description: str

class EnclosureCreate(EnclosureBase):
    pass

class EnclosureResponse(EnclosureBase):
    id: str
    faculty_id: str
    document_url: Optional[str] = None

    class Config:
        from_attributes = True

class DeclarationBase(BaseModel):
    is_declared: bool
    place: str
    designation: str

class DeclarationCreate(DeclarationBase):
    pass

class DeclarationResponse(DeclarationBase):
    id: str
    faculty_id: str
    date: datetime

    class Config:
        from_attributes = True
