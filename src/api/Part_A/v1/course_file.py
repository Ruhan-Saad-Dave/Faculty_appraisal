from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_A.course_file import (
    CourseFileCreate,
    CourseFileUpdateFaculty,
    CourseFileUpdateHOD,
    CourseFileResponse,
)
from ....crud.Part_A import course_file as crud_course_file

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    return User(id=1, roles=["faculty"])

@router.post("/course-files", response_model=CourseFileResponse, status_code=status.HTTP_201_CREATED)
def create_course_file(
    course_file: CourseFileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can create entries")
    return crud_course_file.create_course_file(db, course_file, current_user.id)

@router.get("/course-files/faculty/{faculty_id}", response_model=List[CourseFileResponse])
def read_course_files_by_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return crud_course_file.get_course_files_by_faculty(db, faculty_id)

@router.get("/course-files", response_model=List[CourseFileResponse])
def read_all_course_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all data")
    return db.query(crud_course_file.CourseFile).all()

@router.put("/course-files/{id}", response_model=CourseFileResponse)
def update_course_file(
    id: int,
    course_file_update: CourseFileUpdateFaculty,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_entry = crud_course_file.get_course_file(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "admin" in current_user.roles or "hod" in current_user.roles:
        # For simplicity in this demo, HOD update logic
        return crud_course_file.update_course_file_hod(db, id, course_file_update)
    elif "faculty" in current_user.roles and db_entry.faculty_id == current_user.id:
        return crud_course_file.update_course_file_faculty(db, id, course_file_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.delete("/course-files/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_file(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_course_file.delete_course_file(db, id)
    return None
