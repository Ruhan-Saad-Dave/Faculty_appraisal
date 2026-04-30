from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.Part_B.research_project import ResearchProject
from src.schema.Part_B.research_project import (
    ResearchProjectCreate,
    ResearchProjectUpdateFaculty,
    ResearchProjectUpdateHOD,
    ResearchProjectUpdateDirector,
)

def get_research_project(db: Session, project_id: str) -> Optional[ResearchProject]:
    return db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

def get_research_projects_by_faculty(db: Session, faculty_id: str, skip: int = 0, limit: int = 100) -> List[ResearchProject]:
    return db.query(ResearchProject).filter(ResearchProject.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_research_projects(db: Session, skip: int = 0, limit: int = 100) -> List[ResearchProject]:
    return db.query(ResearchProject).offset(skip).limit(limit).all()

def create_research_project(db: Session, project: ResearchProjectCreate, faculty_id: str) -> ResearchProject:
    db_project = ResearchProject(**project.model_dump(), faculty_id=faculty_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_research_project_faculty(
    db: Session, project_id: str, project_update: ResearchProjectUpdateFaculty
) -> Optional[ResearchProject]:
    db_project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if db_project:
        update_data = project_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project

def update_research_project_hod(
    db: Session, project_id: str, project_update: ResearchProjectUpdateHOD
) -> Optional[ResearchProject]:
    db_project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if db_project:
        db_project.api_score_hod = project_update.api_score_hod
        db.commit()
        db.refresh(db_project)
    return db_project

def update_research_project_director(
    db: Session, project_id: str, project_update: ResearchProjectUpdateDirector
) -> Optional[ResearchProject]:
    db_project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if db_project:
        db_project.api_score_director = project_update.api_score_director
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_research_project(db: Session, project_id: str) -> Optional[ResearchProject]:
    db_project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

def get_research_projects_total_score(db: Session, faculty_id: str) -> float:
    projects = db.query(ResearchProject).filter(ResearchProject.faculty_id == faculty_id).all()
    total_score = sum([p.api_score_faculty for p in projects])
    return total_score
