from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.Part_B.ict_pedagogy import ICTPedagogy
from src.schema.Part_B.ict_pedagogy import (
    ICTPedagogyCreate,
    ICTPedagogyUpdateFaculty,
    ICTPedagogyUpdateHOD,
    ICTPedagogyUpdateDirector,
)

def get_ict_pedagogy(db: Session, pedagogy_id: int) -> Optional[ICTPedagogy]:
    return db.query(ICTPedagogy).filter(ICTPedagogy.id == pedagogy_id).first()

def get_ict_pedagogies_by_faculty(db: Session, faculty_id: int, skip: int = 0, limit: int = 100) -> List[ICTPedagogy]:
    return db.query(ICTPedagogy).filter(ICTPedagogy.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_ict_pedagogies(db: Session, skip: int = 0, limit: int = 100) -> List[ICTPedagogy]:
    return db.query(ICTPedagogy).offset(skip).limit(limit).all()

def create_ict_pedagogy(db: Session, pedagogy: ICTPedagogyCreate, faculty_id: int) -> ICTPedagogy:
    db_pedagogy = ICTPedagogy(**pedagogy.model_dump(), faculty_id=faculty_id)
    db.add(db_pedagogy)
    db.commit()
    db.refresh(db_pedagogy)
    return db_pedagogy

def update_ict_pedagogy_faculty(
    db: Session, pedagogy_id: int, pedagogy_update: ICTPedagogyUpdateFaculty
) -> Optional[ICTPedagogy]:
    db_pedagogy = db.query(ICTPedagogy).filter(ICTPedagogy.id == pedagogy_id).first()
    if db_pedagogy:
        update_data = pedagogy_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_pedagogy, key, value)
        db.commit()
        db.refresh(db_pedagogy)
    return db_pedagogy

def update_ict_pedagogy_hod(
    db: Session, pedagogy_id: int, pedagogy_update: ICTPedagogyUpdateHOD
) -> Optional[ICTPedagogy]:
    db_pedagogy = db.query(ICTPedagogy).filter(ICTPedagogy.id == pedagogy_id).first()
    if db_pedagogy:
        db_pedagogy.api_score_hod = pedagogy_update.api_score_hod
        db.commit()
        db.refresh(db_pedagogy)
    return db_pedagogy

def update_ict_pedagogy_director(
    db: Session, pedagogy_id: int, pedagogy_update: ICTPedagogyUpdateDirector
) -> Optional[ICTPedagogy]:
    db_pedagogy = db.query(ICTPedagogy).filter(ICTPedagogy.id == pedagogy_id).first()
    if db_pedagogy:
        db_pedagogy.api_score_director = pedagogy_update.api_score_director
        db.commit()
        db.refresh(db_pedagogy)
    return db_pedagogy

def delete_ict_pedagogy(db: Session, pedagogy_id: int) -> Optional[ICTPedagogy]:
    db_pedagogy = db.query(ICTPedagogy).filter(ICTPedagogy.id == pedagogy_id).first()
    if db_pedagogy:
        db.delete(db_pedagogy)
        db.commit()
    return db_pedagogy

def get_ict_pedagogies_total_score(db: Session, faculty_id: int) -> float:
    pedagogies = db.query(ICTPedagogy).filter(ICTPedagogy.faculty_id == faculty_id).all()
    total_score = sum([p.api_score_faculty for p in pedagogies])
    return total_score
