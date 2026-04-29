from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_B.research_project import (
    ResearchProjectCreate,
    ResearchProjectUpdateFaculty,
    ResearchProjectUpdateHOD,
    ResearchProjectUpdateDirector,
    ResearchProjectResponse,
    ResearchProjectSummary,
)
from ....crud.Part_B import research_project as crud_research_project
from ....models.Part_B.research_project import ResearchProject as DBResearchProject

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    # This is a mock user for demonstration. Replace with actual authentication.
    return User(id=1, roles=["faculty"]) # Default to faculty for now

@router.post("/research-projects", response_model=ResearchProjectResponse, status_code=status.HTTP_201_CREATED)
def create_research_project(
    project: ResearchProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create research projects")
    
    return crud_research_project.create_research_project(db=db, project=project, faculty_id=current_user.id)

@router.get("/research-projects/faculty/{faculty_id}", response_model=List[ResearchProjectResponse])
def read_research_projects_by_faculty(
    faculty_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's research projects")
    
    projects = crud_research_project.get_research_projects_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return projects

@router.get("/research-projects", response_model=List[ResearchProjectResponse])
def read_all_research_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all research projects")
    
    projects = crud_research_project.get_all_research_projects(db, skip=skip, limit=limit)
    return projects

@router.put("/research-projects/{project_id}", response_model=ResearchProjectResponse)
def update_research_project(
    project_id: int,
    project_update: ResearchProjectUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_project = crud_research_project.get_research_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research Project not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_project = crud_research_project.update_research_project_faculty(db, project_id, project_update)
    elif "hod" in current_user.roles:
        if not isinstance(project_update, ResearchProjectUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update api_score_hod")
        updated_project = crud_research_project.update_research_project_hod(db, project_id, project_update)
    elif "director" in current_user.roles:
        if not isinstance(project_update, ResearchProjectUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update api_score_director")
        updated_project = crud_research_project.update_research_project_director(db, project_id, project_update)
    elif "faculty" in current_user.roles and db_project.faculty_id == current_user.id:
        updated_project = crud_research_project.update_research_project_faculty(db, project_id, project_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this research project")

    if updated_project is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update research project")
    return updated_project

@router.delete("/research-projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_project = crud_research_project.get_research_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research Project not found")

    if "admin" not in current_user.roles and db_project.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this research project")
    
    crud_research_project.delete_research_project(db, project_id)
    return {"message": "Research Project deleted successfully"}

@router.get("/research-projects/summary/{faculty_id}", response_model=ResearchProjectSummary)
def get_research_projects_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_research_project.get_research_projects_total_score(db, faculty_id)
    return ResearchProjectSummary(total_score=total_score)
