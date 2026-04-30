from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.university_activities import UniversityActivity
from ...schema.Part_A.university_activities import (
    UniversityActivityCreate,
    UniversityActivityUpdateFaculty,
    UniversityActivityUpdateHOD,
    UniversityActivityUpdateDirector,
)

def get_university_activity(db: Session, id: int) -> Optional[UniversityActivity]:
    return db.query(UniversityActivity).filter(UniversityActivity.id == id).first()

def get_university_activities_by_faculty(db: Session, faculty_id: int) -> List[UniversityActivity]:
    return db.query(UniversityActivity).filter(UniversityActivity.faculty_id == faculty_id).all()

def create_university_activity(
    db: Session, activity: UniversityActivityCreate, faculty_id: int
) -> UniversityActivity:
    db_activity = UniversityActivity(**activity.model_dump(), faculty_id=faculty_id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def update_university_activity_faculty(
    db: Session, id: int, activity_update: UniversityActivityUpdateFaculty
) -> Optional[UniversityActivity]:
    db_activity = get_university_activity(db, id)
    if db_activity:
        update_data = activity_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_activity, key, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity

def update_university_activity_hod(
    db: Session, id: int, activity_update: UniversityActivityUpdateHOD
) -> Optional[UniversityActivity]:
    db_activity = get_university_activity(db, id)
    if db_activity:
        db_activity.api_score_hod = activity_update.api_score_hod
        db.commit()
        db.refresh(db_activity)
    return db_activity

def update_university_activity_director(
    db: Session, id: int, activity_update: UniversityActivityUpdateDirector
) -> Optional[UniversityActivity]:
    db_activity = get_university_activity(db, id)
    if db_activity:
        db_activity.api_score_director = activity_update.api_score_director
        db.commit()
        db.refresh(db_activity)
    return db_activity

def delete_university_activity(db: Session, id: int) -> bool:
    db_activity = get_university_activity(db, id)
    if db_activity:
        db.delete(db_activity)
        db.commit()
        return True
    return False

def get_university_activity_total_score(db: Session, faculty_id: int) -> float:
    entries = get_university_activities_by_faculty(db, faculty_id)
    return sum([e.api_score_faculty for e in entries])
