from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.Part_B.self_development_fdp import SelfDevelopmentFDP
from src.schema.Part_B.self_development_fdp import (
    SelfDevelopmentFDPCreate,
    SelfDevelopmentFDPUpdateFaculty,
    SelfDevelopmentFDPUpdateHOD,
    SelfDevelopmentFDPUpdateDirector,
)

def get_self_development_fdp(db: Session, fdp_id: str) -> Optional[SelfDevelopmentFDP]:
    return db.query(SelfDevelopmentFDP).filter(SelfDevelopmentFDP.id == fdp_id).first()

def get_self_development_fdp_by_faculty(db: Session, faculty_id: str, skip: int = 0, limit: int = 100) -> List[SelfDevelopmentFDP]:
    return db.query(SelfDevelopmentFDP).filter(SelfDevelopmentFDP.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_self_development_fdp(db: Session, skip: int = 0, limit: int = 100) -> List[SelfDevelopmentFDP]:
    return db.query(SelfDevelopmentFDP).offset(skip).limit(limit).all()

def create_self_development_fdp(db: Session, fdp: SelfDevelopmentFDPCreate, faculty_id: str) -> SelfDevelopmentFDP:
    db_fdp = SelfDevelopmentFDP(**fdp.model_dump(), faculty_id=faculty_id)
    db.add(db_fdp)
    db.commit()
    db.refresh(db_fdp)
    return db_fdp

def update_self_development_fdp_faculty(
    db: Session, fdp_id: str, fdp_update: SelfDevelopmentFDPUpdateFaculty
) -> Optional[SelfDevelopmentFDP]:
    db_fdp = db.query(SelfDevelopmentFDP).filter(SelfDevelopmentFDP.id == fdp_id).first()
    if db_fdp:
        update_data = fdp_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_fdp, key, value)
        db.commit()
        db.refresh(db_fdp)
    return db_fdp

def update_self_development_fdp_hod(
    db: Session, fdp_id: str, fdp_update: SelfDevelopmentFDPUpdateHOD
) -> Optional[SelfDevelopmentFDP]:
    db_fdp = db.query(SelfDevelopmentFDP).filter(SelfDevelopmentFDP.id == fdp_id).first()
    if db_fdp:
        db_fdp.api_score_hod = fdp_update.api_score_hod
        db.commit()
        db.refresh(db_fdp)
    return db_fdp

def update_self_development_fdp_director(
    db: Session, fdp_id: str, fdp_update: SelfDevelopmentFDPUpdateDirector
) -> Optional[SelfDevelopmentFDP]:
    db_fdp = db.query(SelfDevelopmentFDP).filter(SelfDevelopmentFDP.id == fdp_id).first()
    if db_fdp:
        db_fdp.api_score_director = fdp_update.api_score_director
        db.commit()
        db.refresh(db_fdp)
    return db_fdp

def delete_self_development_fdp(db: Session, fdp_id: str) -> Optional[SelfDevelopmentFDP]:
    db_fdp = db.query(SelfDevelopmentFDP).filter(SelfDevelopmentFDP.id == fdp_id).first()
    if db_fdp:
        db.delete(db_fdp)
        db.commit()
    return db_fdp

def get_self_development_fdp_total_score(db: Session, faculty_id: str) -> float:
    fdp_entries = db.query(SelfDevelopmentFDP).filter(SelfDevelopmentFDP.faculty_id == faculty_id).all()
    total_score = sum([fdp.api_score_faculty for fdp in fdp_entries])
    return total_score
