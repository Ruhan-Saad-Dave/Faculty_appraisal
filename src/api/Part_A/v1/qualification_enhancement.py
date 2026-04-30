from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_A.qualification_enhancement import (
    QualificationEnhancementCreate,
    QualificationEnhancementUpdateFaculty,
    QualificationEnhancementUpdateHOD,
    QualificationEnhancementUpdateDirector,
    QualificationEnhancementResponse,
)
from ....crud.Part_A import qualification_enhancement as crud_qualification

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    return User(id=1, roles=["faculty"])

@router.post("/qualification-enhancement", response_model=QualificationEnhancementResponse, status_code=status.HTTP_201_CREATED)
def create_qualification(
    qualification: QualificationEnhancementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can create entries")
    return crud_qualification.create_qualification_enhancement(db, qualification, current_user.id)

@router.get("/qualification-enhancement/faculty/{faculty_id}", response_model=List[QualificationEnhancementResponse])
def read_qualifications_by_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return crud_qualification.get_qualification_enhancements_by_faculty(db, faculty_id)

@router.get("/qualification-enhancement", response_model=List[QualificationEnhancementResponse])
def read_all_qualifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all data")
    return db.query(crud_qualification.QualificationEnhancement).all()

@router.put("/qualification-enhancement/{id}", response_model=QualificationEnhancementResponse)
def update_qualification(
    id: int,
    qualification_update: QualificationEnhancementUpdateFaculty,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_entry = crud_qualification.get_qualification_enhancement(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "admin" in current_user.roles or "hod" in current_user.roles:
        return crud_qualification.update_qualification_enhancement_hod(db, id, qualification_update)
    elif "director" in current_user.roles:
        return crud_qualification.update_qualification_enhancement_director(db, id, qualification_update)
    elif "faculty" in current_user.roles and db_entry.faculty_id == current_user.id:
        return crud_qualification.update_qualification_enhancement_faculty(db, id, qualification_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.delete("/qualification-enhancement/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_qualification(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_qualification.delete_qualification_enhancement(db, id)
    return None
