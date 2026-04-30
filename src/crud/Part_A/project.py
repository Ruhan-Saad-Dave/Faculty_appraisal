from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.project import ProjectPartA
from ...schema.Part_A.project import (
    ProjectPartACreate,
    ProjectPartAUpdateFaculty,
    ProjectPartAUpdateHOD,
    ProjectPartAUpdateDirector,
)

def get_project(db: Session, id: int) -> Optional[ProjectPartA]:
    return db.query(ProjectPartA).filter(ProjectPartA.id == id).first()

def get_projects_by_faculty(db: Session, faculty_id: int) -> List[ProjectPartA]:
    return db.query(ProjectPartA).filter(ProjectPartA.faculty_id == faculty_id).all()

def create_project(db: Session, project: ProjectPartACreate, faculty_id: int) -> ProjectPartA:
    db_project = ProjectPartA(**project.model_dump(), faculty_id=faculty_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project_faculty(
    db: Session, id: int, project_update: ProjectPartAUpdateFaculty
) -> Optional[ProjectPartA]:
    db_project = get_project(db, id)
    if db_project:
        update_data = project_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project

def update_project_hod(
    db: Session, id: int, project_update: ProjectPartAUpdateHOD
) -> Optional[ProjectPartA]:
    db_project = get_project(db, id)
    if db_project:
        db_project.api_score_hod = project_update.api_score_hod
        db.commit()
        db.refresh(db_project)
    return db_project

def update_project_director(
    db: Session, id: int, project_update: ProjectPartAUpdateDirector
) -> Optional[ProjectPartA]:
    db_project = get_project(db, id)
    if db_project:
        db_project.api_score_director = project_update.api_score_director
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, id: int) -> bool:
    db_project = get_project(db, id)
    if db_project:
        db.delete(db_project)
        db.commit()
        return True
    return False

def get_project_total_score(db: Session, faculty_id: int) -> float:
    entries = get_projects_by_faculty(db, faculty_id)
    return sum([e.api_score_faculty for e in entries])
