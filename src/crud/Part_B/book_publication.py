from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.Part_B.book_publication import BookPublication
from src.schema.Part_B.book_publication import (
    BookPublicationCreate,
    BookPublicationUpdateFaculty,
    BookPublicationUpdateHOD,
    BookPublicationUpdateDirector,
)

def get_book_publication(db: Session, publication_id: int) -> Optional[BookPublication]:
    return db.query(BookPublication).filter(BookPublication.id == publication_id).first()

def get_book_publications_by_faculty(db: Session, faculty_id: int, skip: int = 0, limit: int = 100) -> List[BookPublication]:
    return db.query(BookPublication).filter(BookPublication.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_book_publications(db: Session, skip: int = 0, limit: int = 100) -> List[BookPublication]:
    return db.query(BookPublication).offset(skip).limit(limit).all()

def create_book_publication(db: Session, publication: BookPublicationCreate, faculty_id: int) -> BookPublication:
    db_publication = BookPublication(**publication.model_dump(), faculty_id=faculty_id)
    db.add(db_publication)
    db.commit()
    db.refresh(db_publication)
    return db_publication

def update_book_publication_faculty(
    db: Session, publication_id: int, publication_update: BookPublicationUpdateFaculty
) -> Optional[BookPublication]:
    db_publication = db.query(BookPublication).filter(BookPublication.id == publication_id).first()
    if db_publication:
        update_data = publication_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_publication, key, value)
        db.commit()
        db.refresh(db_publication)
    return db_publication

def update_book_publication_hod(
    db: Session, publication_id: int, publication_update: BookPublicationUpdateHOD
) -> Optional[BookPublication]:
    db_publication = db.query(BookPublication).filter(BookPublication.id == publication_id).first()
    if db_publication:
        db_publication.api_score_hod = publication_update.api_score_hod
        db.commit()
        db.refresh(db_publication)
    return db_publication

def update_book_publication_director(
    db: Session, publication_id: int, publication_update: BookPublicationUpdateDirector
) -> Optional[BookPublication]:
    db_publication = db.query(BookPublication).filter(BookPublication.id == publication_id).first()
    if db_publication:
        db_publication.api_score_director = publication_update.api_score_director
        db.commit()
        db.refresh(db_publication)
    return db_publication

def delete_book_publication(db: Session, publication_id: int) -> Optional[BookPublication]:
    db_publication = db.query(BookPublication).filter(BookPublication.id == publication_id).first()
    if db_publication:
        db.delete(db_publication)
        db.commit()
    return db_publication

def get_book_publications_total_score(db: Session, faculty_id: int) -> float:
    publications = db.query(BookPublication).filter(BookPublication.faculty_id == faculty_id).all()
    total_score = sum([pub.api_score_faculty for pub in publications]) # Assuming faculty score contributes to total
    return total_score