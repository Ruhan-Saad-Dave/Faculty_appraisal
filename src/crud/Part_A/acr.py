from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.acr import ACR
from ...schema.Part_A.acr import (
    ACRCreate,
    ACRUpdateHOD,
    ACRUpdateDirector,
)

def get_acr(db: Session, id: int) -> Optional[ACR]:
    return db.query(ACR).filter(ACR.id == id).first()

def get_acr_by_faculty(db: Session, faculty_id: int) -> List[ACR]:
    return db.query(ACR).filter(ACR.faculty_id == faculty_id).all()

def create_acr(db: Session, acr: ACRCreate) -> ACR:
    db_acr = ACR(**acr.model_dump())
    db.add(db_acr)
    db.commit()
    db.refresh(db_acr)
    return db_acr

def update_acr_hod(
    db: Session, id: int, acr_update: ACRUpdateHOD
) -> Optional[ACR]:
    db_acr = get_acr(db, id)
    if db_acr:
        db_acr.api_score_hod = acr_update.api_score_hod
        db.commit()
        db.refresh(db_acr)
    return db_acr

def update_acr_director(
    db: Session, id: int, acr_update: ACRUpdateDirector
) -> Optional[ACR]:
    db_acr = get_acr(db, id)
    if db_acr:
        update_data = acr_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_acr, key, value)
        db.commit()
        db.refresh(db_acr)
    return db_acr

def delete_acr(db: Session, id: int) -> bool:
    db_acr = get_acr(db, id)
    if db_acr:
        db.delete(db_acr)
        db.commit()
        return True
    return False

def get_acr_total_score(db: Session, faculty_id: int) -> float:
    entries = get_acr_by_faculty(db, faculty_id)
    # Note: ACR usually has score from HOD/Director. 
    # Summary requirement for ACR might need clarification, but I'll return a sum for now.
    return sum([e.api_score_hod for e in entries])
