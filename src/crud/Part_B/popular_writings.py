from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from src.models.Part_B.popular_writings import PopularWriting
from src.schema.Part_B.popular_writings import PopularWritingCreate, PopularWritingUpdate

def get_popular_writing(db: Session, writing_id: UUID) -> Optional[PopularWriting]:
    return db.query(PopularWriting).filter(PopularWriting.id == writing_id).first()

def get_popular_writings_by_faculty(db: Session, faculty_id: UUID, skip: int = 0, limit: int = 100) -> List[PopularWriting]:
    return db.query(PopularWriting).filter(PopularWriting.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_popular_writings(db: Session, skip: int = 0, limit: int = 100) -> List[PopularWriting]:
    return db.query(PopularWriting).offset(skip).limit(limit).all()

def create_popular_writing(db: Session, writing: PopularWritingCreate, faculty_id: UUID) -> PopularWriting:
    db_writing = PopularWriting(**writing.model_dump(), faculty_id=faculty_id)
    # Automatic score calculation can be added here if needed
    db.add(db_writing)
    db.commit()
    db.refresh(db_writing)
    return db_writing

def update_popular_writing(db: Session, writing_id: UUID, writing_update: PopularWritingUpdate) -> Optional[PopularWriting]:
    db_writing = db.query(PopularWriting).filter(PopularWriting.id == writing_id).first()
    if db_writing:
        update_data = writing_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_writing, key, value)
        db.commit()
        db.refresh(db_writing)
    return db_writing

def delete_popular_writing(db: Session, writing_id: UUID) -> Optional[PopularWriting]:
    db_writing = db.query(PopularWriting).filter(PopularWriting.id == writing_id).first()
    if db_writing:
        db.delete(db_writing)
        db.commit()
    return db_writing

def get_popular_writings_total_score(db: Session, faculty_id: UUID) -> float:
    writings = db.query(PopularWriting).filter(PopularWriting.faculty_id == faculty_id).all()
    # Assuming each contributes its faculty score to the total summary
    return sum([w.api_score_faculty for w in writings])
