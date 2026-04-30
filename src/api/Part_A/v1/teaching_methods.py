from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_A.teaching_methods import (
    TeachingMethodsCreate,
    TeachingMethodsUpdateFaculty,
    TeachingMethodsUpdateHOD,
    TeachingMethodsResponse,
)
from ....crud.Part_A import teaching_methods as crud_teaching_methods

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    return User(id=1, roles=["faculty"])

@router.post("/teaching-methods", response_model=TeachingMethodsResponse, status_code=status.HTTP_201_CREATED)
def create_teaching_methods(
    methods: TeachingMethodsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can create entries")
    return crud_teaching_methods.create_teaching_methods(db, methods, current_user.id)

@router.get("/teaching-methods/faculty/{faculty_id}", response_model=List[TeachingMethodsResponse])
def read_teaching_methods_by_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return crud_teaching_methods.get_teaching_methods_by_faculty(db, faculty_id)

@router.get("/teaching-methods", response_model=List[TeachingMethodsResponse])
def read_all_teaching_methods(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all data")
    return db.query(crud_teaching_methods.TeachingMethods).all()

@router.put("/teaching-methods/{id}", response_model=TeachingMethodsResponse)
def update_teaching_methods(
    id: int,
    methods_update: TeachingMethodsUpdateFaculty,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_entry = crud_teaching_methods.get_teaching_methods(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "admin" in current_user.roles or "hod" in current_user.roles:
        return crud_teaching_methods.update_teaching_methods_hod(db, id, methods_update)
    elif "faculty" in current_user.roles and db_entry.faculty_id == current_user.id:
        return crud_teaching_methods.update_teaching_methods_faculty(db, id, methods_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.delete("/teaching-methods/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teaching_methods(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_teaching_methods.delete_teaching_methods(db, id)
    return None
