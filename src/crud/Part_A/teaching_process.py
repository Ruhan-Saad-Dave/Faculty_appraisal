from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.teaching_process import TeachingProcess
from ...schema.Part_A.teaching_process import (
    TeachingProcessCreate,
    TeachingProcessUpdateFaculty,
    TeachingProcessUpdateHOD,
)

def get_teaching_process(db: Session, id: str) -> Optional[TeachingProcess]:
    return db.query(TeachingProcess).filter(TeachingProcess.id == id).first()

def get_teaching_process_by_faculty(db: Session, faculty_id: str) -> List[TeachingProcess]:
    return db.query(TeachingProcess).filter(TeachingProcess.faculty_id == faculty_id).all()

def create_teaching_process(db: Session, teaching: TeachingProcessCreate, faculty_id: str) -> TeachingProcess:
    db_teaching = TeachingProcess(**teaching.model_dump(), faculty_id=faculty_id)
    db.add(db_teaching)
    db.commit()
    db.refresh(db_teaching)
    return db_teaching

def update_teaching_process_faculty(
    db: Session, id: str, teaching_update: TeachingProcessUpdateFaculty
) -> Optional[TeachingProcess]:
    db_teaching = get_teaching_process(db, id)
    if db_teaching:
        update_data = teaching_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_teaching, key, value)
        db.commit()
        db.refresh(db_teaching)
    return db_teaching

def update_teaching_process_hod(
    db: Session, id: str, teaching_update: TeachingProcessUpdateHOD
) -> Optional[TeachingProcess]:
    db_teaching = get_teaching_process(db, id)
    if db_teaching:
        update_data = teaching_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_teaching, key, value)
        db.commit()
        db.refresh(db_teaching)
    return db_teaching

def delete_teaching_process(db: Session, id: str) -> bool:
    db_teaching = get_teaching_process(db, id)
    if db_teaching:
        db.delete(db_teaching)
        db.commit()
        return True
    return False

def get_teaching_process_total_score(db: Session, faculty_id: str) -> float:
    entries = get_teaching_process_by_faculty(db, faculty_id)
    return sum([e.api_score_faculty for e in entries])
