from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.Part_B.conference_paper import ConferencePaper
from src.schema.Part_B.conference_paper import (
    ConferencePaperCreate,
    ConferencePaperUpdateFaculty,
    ConferencePaperUpdateHOD,
    ConferencePaperUpdateDirector,
)

def get_conference_paper(db: Session, paper_id: int) -> Optional[ConferencePaper]:
    return db.query(ConferencePaper).filter(ConferencePaper.id == paper_id).first()

def get_conference_papers_by_faculty(db: Session, faculty_id: int, skip: int = 0, limit: int = 100) -> List[ConferencePaper]:
    return db.query(ConferencePaper).filter(ConferencePaper.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_conference_papers(db: Session, skip: int = 0, limit: int = 100) -> List[ConferencePaper]:
    return db.query(ConferencePaper).offset(skip).limit(limit).all()

def create_conference_paper(db: Session, paper: ConferencePaperCreate, faculty_id: int) -> ConferencePaper:
    db_paper = ConferencePaper(**paper.model_dump(), faculty_id=faculty_id)
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

def update_conference_paper_faculty(
    db: Session, paper_id: int, paper_update: ConferencePaperUpdateFaculty
) -> Optional[ConferencePaper]:
    db_paper = db.query(ConferencePaper).filter(ConferencePaper.id == paper_id).first()
    if db_paper:
        update_data = paper_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_paper, key, value)
        db.commit()
        db.refresh(db_paper)
    return db_paper

def update_conference_paper_hod(
    db: Session, paper_id: int, paper_update: ConferencePaperUpdateHOD
) -> Optional[ConferencePaper]:
    db_paper = db.query(ConferencePaper).filter(ConferencePaper.id == paper_id).first()
    if db_paper:
        db_paper.research_score_hod = paper_update.research_score_hod
        db.commit()
        db.refresh(db_paper)
    return db_paper

def update_conference_paper_director(
    db: Session, paper_id: int, paper_update: ConferencePaperUpdateDirector
) -> Optional[ConferencePaper]:
    db_paper = db.query(ConferencePaper).filter(ConferencePaper.id == paper_id).first()
    if db_paper:
        db_paper.research_score_director = paper_update.research_score_director
        db.commit()
        db.refresh(db_paper)
    return db_paper

def delete_conference_paper(db: Session, paper_id: int) -> Optional[ConferencePaper]:
    db_paper = db.query(ConferencePaper).filter(ConferencePaper.id == paper_id).first()
    if db_paper:
        db.delete(db_paper)
        db.commit()
    return db_paper

def get_conference_papers_total_score(db: Session, faculty_id: int) -> float:
    papers = db.query(ConferencePaper).filter(ConferencePaper.faculty_id == faculty_id).all()
    total_score = sum([paper.research_score_faculty for paper in papers])
    return total_score
