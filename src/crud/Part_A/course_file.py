from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.course_file import CourseFile
from ...schema.Part_A.course_file import (
    CourseFileCreate,
    CourseFileUpdateFaculty,
    CourseFileUpdateHOD,
)

def get_course_file(db: Session, id: str) -> Optional[CourseFile]:
    return db.query(CourseFile).filter(CourseFile.id == id).first()

def get_course_files_by_faculty(db: Session, faculty_id: str) -> List[CourseFile]:
    return db.query(CourseFile).filter(CourseFile.faculty_id == faculty_id).all()

def create_course_file(db: Session, course_file: CourseFileCreate, faculty_id: str) -> CourseFile:
    db_course_file = CourseFile(**course_file.model_dump(), faculty_id=faculty_id)
    db.add(db_course_file)
    db.commit()
    db.refresh(db_course_file)
    return db_course_file

def update_course_file_faculty(
    db: Session, id: str, course_file_update: CourseFileUpdateFaculty
) -> Optional[CourseFile]:
    db_course_file = get_course_file(db, id)
    if db_course_file:
        update_data = course_file_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_course_file, key, value)
        db.commit()
        db.refresh(db_course_file)
    return db_course_file

def update_course_file_hod(
    db: Session, id: str, course_file_update: CourseFileUpdateHOD
) -> Optional[CourseFile]:
    db_course_file = get_course_file(db, id)
    if db_course_file:
        update_data = course_file_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_course_file, key, value)
        db.commit()
        db.refresh(db_course_file)
    return db_course_file

def delete_course_file(db: Session, id: str) -> bool:
    db_course_file = get_course_file(db, id)
    if db_course_file:
        db.delete(db_course_file)
        db.commit()
        return True
    return False

def get_course_file_total_score(db: Session, faculty_id: str) -> float:
    entries = get_course_files_by_faculty(db, faculty_id)
    return sum([e.api_score_faculty for e in entries])
