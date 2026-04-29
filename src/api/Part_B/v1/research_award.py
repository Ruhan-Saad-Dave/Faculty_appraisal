from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_B.research_award import (
    ResearchAwardCreate,
    ResearchAwardUpdateFaculty,
    ResearchAwardUpdateHOD,
    ResearchAwardUpdateDirector,
    ResearchAwardResponse,
    ResearchAwardSummary,
)
from ....crud.Part_B import research_award as crud_research_award
from ....models.Part_B.research_award import ResearchAward as DBResearchAward

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    # This is a mock user for demonstration. Replace with actual authentication.
    return User(id=1, roles=["faculty"]) # Default to faculty for now

@router.post("/research-awards", response_model=ResearchAwardResponse, status_code=status.HTTP_201_CREATED)
def create_research_award(
    award: ResearchAwardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create research awards")
    
    return crud_research_award.create_research_award(db=db, award=award, faculty_id=current_user.id)

@router.get("/research-awards/faculty/{faculty_id}", response_model=List[ResearchAwardResponse])
def read_research_awards_by_faculty(
    faculty_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's research awards")
    
    awards = crud_research_award.get_research_awards_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return awards

@router.get("/research-awards", response_model=List[ResearchAwardResponse])
def read_all_research_awards(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all research awards")
    
    awards = crud_research_award.get_all_research_awards(db, skip=skip, limit=limit)
    return awards

@router.put("/research-awards/{award_id}", response_model=ResearchAwardResponse)
def update_research_award(
    award_id: int,
    award_update: ResearchAwardUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_award = crud_research_award.get_research_award(db, award_id)
    if db_award is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research Award not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_award = crud_research_award.update_research_award_faculty(db, award_id, award_update)
    elif "hod" in current_user.roles:
        if not isinstance(award_update, ResearchAwardUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update research_score_hod")
        updated_award = crud_research_award.update_research_award_hod(db, award_id, award_update)
    elif "director" in current_user.roles:
        if not isinstance(award_update, ResearchAwardUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update research_score_director")
        updated_award = crud_research_award.update_research_award_director(db, award_id, award_update)
    elif "faculty" in current_user.roles and db_award.faculty_id == current_user.id:
        updated_award = crud_research_award.update_research_award_faculty(db, award_id, award_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this research award")

    if updated_award is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update research award")
    return updated_award

@router.delete("/research-awards/{award_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research_award(
    award_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_award = crud_research_award.get_research_award(db, award_id)
    if db_award is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research Award not found")

    if "admin" not in current_user.roles and db_award.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this research award")
    
    crud_research_award.delete_research_award(db, award_id)
    return {"message": "Research Award deleted successfully"}

@router.get("/research-awards/summary/{faculty_id}", response_model=ResearchAwardSummary)
def get_research_awards_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_research_award.get_research_awards_total_score(db, faculty_id)
    return ResearchAwardSummary(total_score=total_score)
