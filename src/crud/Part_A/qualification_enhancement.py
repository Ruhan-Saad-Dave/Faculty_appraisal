from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.qualification_enhancement import QualificationEnhancement
from ...schema.Part_A.qualification_enhancement import (
    QualificationEnhancementCreate,
    QualificationEnhancementUpdateFaculty,
    QualificationEnhancementUpdateHOD,
    QualificationEnhancementUpdateDirector,
)

def get_qualification_enhancement(db: Session, id: str) -> Optional[QualificationEnhancement]:
    return db.query(QualificationEnhancement).filter(QualificationEnhancement.id == id).first()

def get_qualification_enhancements_by_faculty(db: Session, faculty_id: str) -> List[QualificationEnhancement]:
    return db.query(QualificationEnhancement).filter(QualificationEnhancement.faculty_id == faculty_id).all()

def create_qualification_enhancement(
    db: Session, qualification: QualificationEnhancementCreate, faculty_id: str
) -> QualificationEnhancement:
    db_qualification = QualificationEnhancement(**qualification.model_dump(), faculty_id=faculty_id)
    db.add(db_qualification)
    db.commit()
    db.refresh(db_qualification)
    return db_qualification

def update_qualification_enhancement_faculty(
    db: Session, id: str, qualification_update: QualificationEnhancementUpdateFaculty
) -> Optional[QualificationEnhancement]:
    db_qualification = get_qualification_enhancement(db, id)
    if db_qualification:
        update_data = qualification_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_qualification, key, value)
        db.commit()
        db.refresh(db_qualification)
    return db_qualification

def update_qualification_enhancement_hod(
    db: Session, id: str, qualification_update: QualificationEnhancementUpdateHOD
) -> Optional[QualificationEnhancement]:
    db_qualification = get_qualification_enhancement(db, id)
    if db_qualification:
        db_qualification.api_score_hod = qualification_update.api_score_hod
        db.commit()
        db.refresh(db_qualification)
    return db_qualification

def update_qualification_enhancement_director(
    db: Session, id: str, qualification_update: QualificationEnhancementUpdateDirector
) -> Optional[QualificationEnhancement]:
    db_qualification = get_qualification_enhancement(db, id)
    if db_qualification:
        db_qualification.api_score_director = qualification_update.api_score_director
        db.commit()
        db.refresh(db_qualification)
    return db_qualification

def delete_qualification_enhancement(db: Session, id: str) -> bool:
    db_qualification = get_qualification_enhancement(db, id)
    if db_qualification:
        db.delete(db_qualification)
        db.commit()
        return True
    return False

def get_qualification_enhancement_total_score(db: Session, faculty_id: str) -> float:
    entries = get_qualification_enhancements_by_faculty(db, faculty_id)
    return sum([e.api_score_faculty for e in entries])
