from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_A.acr import (
    ACRCreate,
    ACRUpdateHOD,
    ACRUpdateDirector,
    ACRResponse,
)
from ....crud.Part_A import acr as crud_acr

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    return User(id=1, roles=["faculty"])

@router.post("/acr", response_model=ACRResponse, status_code=status.HTTP_201_CREATED)
def create_acr(
    acr_data: ACRCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can pre-create ACR rows")
    return crud_acr.create_acr(db, acr_data)

@router.get("/acr/faculty/{faculty_id}", response_model=List[ACRResponse])
def read_acr_by_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return crud_acr.get_acr_by_faculty(db, faculty_id)

@router.get("/acr", response_model=List[ACRResponse])
def read_all_acr(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all data")
    return db.query(crud_acr.ACR).all()

@router.put("/acr/{id}", response_model=ACRResponse)
def update_acr(
    id: int,
    acr_update: ACRUpdateHOD,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_entry = crud_acr.get_acr(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "hod" in current_user.roles:
        return crud_acr.update_acr_hod(db, id, acr_update)
    elif "director" in current_user.roles:
        return crud_acr.update_acr_director(db, id, acr_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access for faculty")

@router.get("/acr/summary/{faculty_id}")
def get_acr_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    entries = crud_acr.get_acr_by_faculty(db, faculty_id)
    total_score = sum([e.api_score_hod for e in entries])
    return {"totalScore": min(total_score, 25)} # Max 25 as per PDF
