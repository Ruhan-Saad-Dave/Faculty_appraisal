from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.Part_B.research_guidance import ResearchGuidance
from src.schema.Part_B.research_guidance import (
    ResearchGuidanceCreate,
    ResearchGuidanceUpdateFaculty,
    ResearchGuidanceUpdateHOD,
    ResearchGuidanceUpdateDirector,
)

def get_research_guidance(db: Session, guidance_id: int) -> Optional[ResearchGuidance]:
    return db.query(ResearchGuidance).filter(ResearchGuidance.id == guidance_id).first()

def get_research_guidance_by_faculty(db: Session, faculty_id: int, skip: int = 0, limit: int = 100) -> List[ResearchGuidance]:
    return db.query(ResearchGuidance).filter(ResearchGuidance.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_research_guidance(db: Session, skip: int = 0, limit: int = 100) -> List[ResearchGuidance]:
    return db.query(ResearchGuidance).offset(skip).limit(limit).all()

def create_research_guidance(db: Session, guidance: ResearchGuidanceCreate, faculty_id: int) -> ResearchGuidance:
    db_guidance = ResearchGuidance(**guidance.model_dump(), faculty_id=faculty_id)
    db.add(db_guidance)
    db.commit()
    db.refresh(db_guidance)
    return db_guidance

def update_research_guidance_faculty(
    db: Session, guidance_id: int, guidance_update: ResearchGuidanceUpdateFaculty
) -> Optional[ResearchGuidance]:
    db_guidance = db.query(ResearchGuidance).filter(ResearchGuidance.id == guidance_id).first()
    if db_guidance:
        update_data = guidance_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_guidance, key, value)
        db.commit()
        db.refresh(db_guidance)
    return db_guidance

def update_research_guidance_hod(
    db: Session, guidance_id: int, guidance_update: ResearchGuidanceUpdateHOD
) -> Optional[ResearchGuidance]:
    db_guidance = db.query(ResearchGuidance).filter(ResearchGuidance.id == guidance_id).first()
    if db_guidance:
        db_guidance.api_score_hod = guidance_update.api_score_hod
        db.commit()
        db.refresh(db_guidance)
    return db_guidance

def update_research_guidance_director(
    db: Session, guidance_id: int, guidance_update: ResearchGuidanceUpdateDirector
) -> Optional[ResearchGuidance]:
    db_guidance = db.query(ResearchGuidance).filter(ResearchGuidance.id == guidance_id).first()
    if db_guidance:
        db_guidance.api_score_director = guidance_update.api_score_director
        db.commit()
        db.refresh(db_guidance)
    return db_guidance

def delete_research_guidance(db: Session, guidance_id: int) -> Optional[ResearchGuidance]:
    db_guidance = db.query(ResearchGuidance).filter(ResearchGuidance.id == guidance_id).first()
    if db_guidance:
        db.delete(db_guidance)
        db.commit()
    return db_guidance

def get_research_guidance_total_score(db: Session, faculty_id: int) -> dict:
    guidance_entries = db.query(ResearchGuidance).filter(ResearchGuidance.faculty_id == faculty_id).all()
    total_score = sum([entry.api_score_faculty for entry in guidance_entries])
    
    total_students_me = sum(1 for entry in guidance_entries if entry.degree.lower() == "me")
    total_students_phd = sum(1 for entry in guidance_entries if entry.degree.lower() == "phd")

    return {
        "total_score": total_score,
        "total_students_me": total_students_me,
        "total_students_phd": total_students_phd,
    }
