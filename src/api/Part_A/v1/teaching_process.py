from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_A.teaching_process import (
    TeachingProcessCreate,
    TeachingProcessUpdateFaculty,
    TeachingProcessUpdateHOD,
    TeachingProcessResponse,
)
from ....crud.Part_A import teaching_process as crud_teaching_process

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    # Mock user. In production, this would use a JWT token.
    return User(id=1, roles=["faculty"])

@router.post("/teaching-process", response_model=TeachingProcessResponse, status_code=status.HTTP_201_CREATED)
def create_teaching_process(
    teaching: TeachingProcessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can fill their own teaching data")
    return crud_teaching_process.create_teaching_process(db, teaching, current_user.id)

@router.get("/teaching-process/faculty/{faculty_id}", response_model=List[TeachingProcessResponse])
def read_teaching_process_by_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this data")
    return crud_teaching_process.get_teaching_process_by_faculty(db, faculty_id)

@router.get("/teaching-process", response_model=List[TeachingProcessResponse])
def read_all_teaching_process(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all teaching data")
    # This would need a get_all_teaching_process in CRUD, or we just filter by nothing
    return db.query(crud_teaching_process.TeachingProcess).all()

@router.put("/teaching-process/{id}", response_model=TeachingProcessResponse)
def update_teaching_process(
    id: int,
    teaching_update: TeachingProcessUpdateFaculty, # Usually we'd use a Union or handle it inside
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_teaching = crud_teaching_process.get_teaching_process(db, id)
    if not db_teaching:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "admin" in current_user.roles:
        return crud_teaching_process.update_teaching_process_hod(db, id, teaching_update) # Admin can update everything
    elif "hod" in current_user.roles:
        return crud_teaching_process.update_teaching_process_hod(db, id, teaching_update)
    elif "faculty" in current_user.roles and db_teaching.faculty_id == current_user.id:
        return crud_teaching_process.update_teaching_process_faculty(db, id, teaching_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.delete("/teaching-process/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teaching_process(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_teaching_process.delete_teaching_process(db, id)
    return None
