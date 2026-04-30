from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.departmental_activities import DepartmentalActivity
from ...schema.Part_A.departmental_activities import (
    DepartmentalActivityCreate,
    DepartmentalActivityUpdateFaculty,
    DepartmentalActivityUpdateHOD,
    DepartmentalActivityUpdateDirector,
)

def get_departmental_activity(db: Session, id: str) -> Optional[DepartmentalActivity]:
    return db.query(DepartmentalActivity).filter(DepartmentalActivity.id == id).first()

def get_departmental_activities_by_faculty(db: Session, faculty_id: str) -> List[DepartmentalActivity]:
    return db.query(DepartmentalActivity).filter(DepartmentalActivity.faculty_id == faculty_id).all()

def create_departmental_activity(
    db: Session, activity: DepartmentalActivityCreate, faculty_id: str
) -> DepartmentalActivity:
    db_activity = DepartmentalActivity(**activity.model_dump(), faculty_id=faculty_id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def update_departmental_activity_faculty(
    db: Session, id: str, activity_update: DepartmentalActivityUpdateFaculty
) -> Optional[DepartmentalActivity]:
    db_activity = get_departmental_activity(db, id)
    if db_activity:
        update_data = activity_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_activity, key, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity

def update_departmental_activity_hod(
    db: Session, id: str, activity_update: DepartmentalActivityUpdateHOD
) -> Optional[DepartmentalActivity]:
    db_activity = get_departmental_activity(db, id)
    if db_activity:
        db_activity.api_score_hod = activity_update.api_score_hod
        db.commit()
        db.refresh(db_activity)
    return db_activity

def update_departmental_activity_director(
    db: Session, id: str, activity_update: DepartmentalActivityUpdateDirector
) -> Optional[DepartmentalActivity]:
    db_activity = get_departmental_activity(db, id)
    if db_activity:
        db_activity.api_score_director = activity_update.api_score_director
        db.commit()
        db.refresh(db_activity)
    return db_activity

def delete_departmental_activity(db: Session, id: str) -> bool:
    db_activity = get_departmental_activity(db, id)
    if db_activity:
        db.delete(db_activity)
        db.commit()
        return True
    return False

def get_departmental_activity_total_score(db: Session, faculty_id: str) -> float:
    entries = get_departmental_activities_by_faculty(db, faculty_id)
    return sum([e.api_score_faculty for e in entries])
