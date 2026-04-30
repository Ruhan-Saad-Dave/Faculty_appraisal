from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.Part_B.ipr import IPR
from src.schema.Part_B.ipr import (
    IPRCreate,
    IPRUpdateFaculty,
    IPRUpdateHOD,
    IPRUpdateDirector,
)

def get_ipr(db: Session, ipr_id: str) -> Optional[IPR]:
    return db.query(IPR).filter(IPR.id == ipr_id).first()

def get_ipr_by_faculty(db: Session, faculty_id: str, skip: int = 0, limit: int = 100) -> List[IPR]:
    return db.query(IPR).filter(IPR.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_ipr(db: Session, skip: int = 0, limit: int = 100) -> List[IPR]:
    return db.query(IPR).offset(skip).limit(limit).all()

def create_ipr(db: Session, ipr: IPRCreate, faculty_id: str) -> IPR:
    db_ipr = IPR(**ipr.model_dump(), faculty_id=faculty_id)
    db.add(db_ipr)
    db.commit()
    db.refresh(db_ipr)
    return db_ipr

def update_ipr_faculty(
    db: Session, ipr_id: str, ipr_update: IPRUpdateFaculty
) -> Optional[IPR]:
    db_ipr = db.query(IPR).filter(IPR.id == ipr_id).first()
    if db_ipr:
        update_data = ipr_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ipr, key, value)
        db.commit()
        db.refresh(db_ipr)
    return db_ipr

def update_ipr_hod(
    db: Session, ipr_id: str, ipr_update: IPRUpdateHOD
) -> Optional[IPR]:
    db_ipr = db.query(IPR).filter(IPR.id == ipr_id).first()
    if db_ipr:
        db_ipr.api_score_hod = ipr_update.api_score_hod
        db.commit()
        db.refresh(db_ipr)
    return db_ipr

def update_ipr_director(
    db: Session, ipr_id: str, ipr_update: IPRUpdateDirector
) -> Optional[IPR]:
    db_ipr = db.query(IPR).filter(IPR.id == ipr_id).first()
    if db_ipr:
        db_ipr.api_score_director = ipr_update.api_score_director
        db.commit()
        db.refresh(db_ipr)
    return db_ipr

def delete_ipr(db: Session, ipr_id: str) -> Optional[IPR]:
    db_ipr = db.query(IPR).filter(IPR.id == ipr_id).first()
    if db_ipr:
        db.delete(db_ipr)
        db.commit()
    return db_ipr

def get_ipr_total_score(db: Session, faculty_id: str) -> float:
    iprs = db.query(IPR).filter(IPR.faculty_id == faculty_id).all()
    total_score = sum([entry.research_score_faculty for entry in ipr_entries])
    return total_score
