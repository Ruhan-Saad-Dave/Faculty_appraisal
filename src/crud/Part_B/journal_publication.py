from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.Part_B.journal_publication import JournalPublication
from src.schema.Part_B.journal_publication import (
    JournalPublicationCreate,
    JournalPublicationUpdateFaculty,
    JournalPublicationUpdateHOD,
    JournalPublicationUpdateDirector,
)

def get_journal_publication(db: Session, publication_id: str) -> Optional[JournalPublication]:
    return db.query(JournalPublication).filter(JournalPublication.id == publication_id).first()

def get_journal_publications_by_faculty(db: Session, faculty_id: str, skip: int = 0, limit: int = 100) -> List[JournalPublication]:
    return db.query(JournalPublication).filter(JournalPublication.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_journal_publications(db: Session, skip: int = 0, limit: int = 100) -> List[JournalPublication]:
    return db.query(JournalPublication).offset(skip).limit(limit).all()

def create_journal_publication(db: Session, publication: JournalPublicationCreate, faculty_id: str) -> JournalPublication:
    db_publication = JournalPublication(**publication.model_dump(), faculty_id=faculty_id)
    db.add(db_publication)
    db.commit()
    db.refresh(db_publication)
    return db_publication

def update_journal_publication_faculty(
    db: Session, publication_id: str, publication_update: JournalPublicationUpdateFaculty
) -> Optional[JournalPublication]:
    db_publication = db.query(JournalPublication).filter(JournalPublication.id == publication_id).first()
    if db_publication:
        update_data = publication_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_publication, key, value)
        db.commit()
        db.refresh(db_publication)
    return db_publication

def update_journal_publication_hod(
    db: Session, publication_id: str, publication_update: JournalPublicationUpdateHOD
) -> Optional[JournalPublication]:
    db_publication = db.query(JournalPublication).filter(JournalPublication.id == publication_id).first()
    if db_publication:
        db_publication.api_score_hod = publication_update.api_score_hod
        db.commit()
        db.refresh(db_publication)
    return db_publication

def update_journal_publication_director(
    db: Session, publication_id: str, publication_update: JournalPublicationUpdateDirector
) -> Optional[JournalPublication]:
    db_publication = db.query(JournalPublication).filter(JournalPublication.id == publication_id).first()
    if db_publication:
        db_publication.api_score_director = publication_update.api_score_director
        db.commit()
        db.refresh(db_publication)
    return db_publication

def delete_journal_publication(db: Session, publication_id: str) -> Optional[JournalPublication]:
    db_publication = db.query(JournalPublication).filter(JournalPublication.id == publication_id).first()
    if db_publication:
        db.delete(db_publication)
        db.commit()
    return db_publication

def get_journal_publications_total_score(db: Session, faculty_id: str) -> float:
    publications = db.query(JournalPublication).filter(JournalPublication.faculty_id == faculty_id).all()
    total_score = sum([pub.api_score_faculty for pub in publications]) # Assuming faculty score contributes to total
    return total_score
