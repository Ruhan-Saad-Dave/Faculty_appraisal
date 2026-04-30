from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_A.project import (
    ProjectPartACreate,
    ProjectPartAUpdateFaculty,
    ProjectPartAUpdateHOD,
    ProjectPartAUpdateDirector,
    ProjectPartAResponse,
)
from ....crud.Part_A import project as crud_project

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    return User(id=1, roles=["faculty"])

@router.post("/projects", response_model=ProjectPartAResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectPartACreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can create entries")
    return crud_project.create_project(db, project, current_user.id)

@router.get("/projects/faculty/{faculty_id}", response_model=List[ProjectPartAResponse])
def read_projects_by_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return crud_project.get_projects_by_faculty(db, faculty_id)

@router.get("/projects", response_model=List[ProjectPartAResponse])
def read_all_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all data")
    return db.query(crud_project.ProjectPartA).all()

@router.put("/projects/{id}", response_model=ProjectPartAResponse)
def update_project(
    id: int,
    project_update: ProjectPartAUpdateFaculty,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_entry = crud_project.get_project(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "admin" in current_user.roles or "hod" in current_user.roles:
        return crud_project.update_project_hod(db, id, project_update)
    elif "director" in current_user.roles:
        return crud_project.update_project_director(db, id, project_update)
    elif "faculty" in current_user.roles and db_entry.faculty_id == current_user.id:
        return crud_project.update_project_faculty(db, id, project_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.delete("/projects/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_project.delete_project(db, id)
    return None
