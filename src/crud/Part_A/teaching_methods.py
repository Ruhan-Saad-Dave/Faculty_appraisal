from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.teaching_methods import TeachingMethods
from ...schema.Part_A.teaching_methods import (
    TeachingMethodsCreate,
    TeachingMethodsUpdateFaculty,
    TeachingMethodsUpdateHOD,
)

def get_teaching_methods(db: Session, id: int) -> Optional[TeachingMethods]:
    return db.query(TeachingMethods).filter(TeachingMethods.id == id).first()

def get_teaching_methods_by_faculty(db: Session, faculty_id: int) -> List[TeachingMethods]:
    return db.query(TeachingMethods).filter(TeachingMethods.faculty_id == faculty_id).all()

def create_teaching_methods(db: Session, teaching_methods: TeachingMethodsCreate, faculty_id: int) -> TeachingMethods:
    db_teaching_methods = TeachingMethods(**teaching_methods.model_dump(), faculty_id=faculty_id)
    db.add(db_teaching_methods)
    db.commit()
    db.refresh(db_teaching_methods)
    return db_teaching_methods

def update_teaching_methods_faculty(
    db: Session, id: int, teaching_methods_update: TeachingMethodsUpdateFaculty
) -> Optional[TeachingMethods]:
    db_teaching_methods = get_teaching_methods(db, id)
    if db_teaching_methods:
        update_data = teaching_methods_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_teaching_methods, key, value)
        db.commit()
        db.refresh(db_teaching_methods)
    return db_teaching_methods

def update_teaching_methods_hod(
    db: Session, id: int, teaching_methods_update: TeachingMethodsUpdateHOD
) -> Optional[TeachingMethods]:
    db_teaching_methods = get_teaching_methods(db, id)
    if db_teaching_methods:
        update_data = teaching_methods_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_teaching_methods, key, value)
        db.commit()
        db.refresh(db_teaching_methods)
    return db_teaching_methods

def delete_teaching_methods(db: Session, id: int) -> bool:
    db_teaching_methods = get_teaching_methods(db, id)
    if db_teaching_methods:
        db.delete(db_teaching_methods)
        db.commit()
        return True
    return False

def get_teaching_methods_total_score(db: Session, faculty_id: int) -> float:
    entries = get_teaching_methods_by_faculty(db, faculty_id)
    return sum([e.api_score_faculty for e in entries])
