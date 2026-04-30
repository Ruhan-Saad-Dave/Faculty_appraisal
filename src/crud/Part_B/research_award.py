from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.Part_B.research_award import ResearchAward
from src.schema.Part_B.research_award import (
    ResearchAwardCreate,
    ResearchAwardUpdateFaculty,
    ResearchAwardUpdateHOD,
    ResearchAwardUpdateDirector,
)

def get_research_award(db: Session, award_id: int) -> Optional[ResearchAward]:
    return db.query(ResearchAward).filter(ResearchAward.id == award_id).first()

def get_research_awards_by_faculty(db: Session, faculty_id: int, skip: int = 0, limit: int = 100) -> List[ResearchAward]:
    return db.query(ResearchAward).filter(ResearchAward.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_research_awards(db: Session, skip: int = 0, limit: int = 100) -> List[ResearchAward]:
    return db.query(ResearchAward).offset(skip).limit(limit).all()

def create_research_award(db: Session, award: ResearchAwardCreate, faculty_id: int) -> ResearchAward:
    db_award = ResearchAward(**award.model_dump(), faculty_id=faculty_id)
    db.add(db_award)
    db.commit()
    db.refresh(db_award)
    return db_award

def update_research_award_faculty(
    db: Session, award_id: int, award_update: ResearchAwardUpdateFaculty
) -> Optional[ResearchAward]:
    db_award = db.query(ResearchAward).filter(ResearchAward.id == award_id).first()
    if db_award:
        update_data = award_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_award, key, value)
        db.commit()
        db.refresh(db_award)
    return db_award

def update_research_award_hod(
    db: Session, award_id: int, award_update: ResearchAwardUpdateHOD
) -> Optional[ResearchAward]:
    db_award = db.query(ResearchAward).filter(ResearchAward.id == award_id).first()
    if db_award:
        db_award.research_score_hod = award_update.research_score_hod
        db.commit()
        db.refresh(db_award)
    return db_award

def update_research_award_director(
    db: Session, award_id: int, award_update: ResearchAwardUpdateDirector
) -> Optional[ResearchAward]:
    db_award = db.query(ResearchAward).filter(ResearchAward.id == award_id).first()
    if db_award:
        db_award.research_score_director = award_update.research_score_director
        db.commit()
        db.refresh(db_award)
    return db_award

def delete_research_award(db: Session, award_id: int) -> Optional[ResearchAward]:
    db_award = db.query(ResearchAward).filter(ResearchAward.id == award_id).first()
    if db_award:
        db.delete(db_award)
        db.commit()
    return db_award

def get_research_awards_total_score(db: Session, faculty_id: int) -> float:
    awards = db.query(ResearchAward).filter(ResearchAward.faculty_id == faculty_id).all()
    total_score = sum([award.research_score_faculty for award in awards])
    return total_score
