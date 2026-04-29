from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_B.conference_paper import (
    ConferencePaperCreate,
    ConferencePaperUpdateFaculty,
    ConferencePaperUpdateHOD,
    ConferencePaperUpdateDirector,
    ConferencePaperResponse,
    ConferencePaperSummary,
)
from ....crud.Part_B import conference_paper as crud_conference_paper
from ....models.Part_B.conference_paper import ConferencePaper as DBConferencePaper

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    # This is a mock user for demonstration. Replace with actual authentication.
    return User(id=1, roles=["faculty"]) # Default to faculty for now

@router.post("/conference-papers", response_model=ConferencePaperResponse, status_code=status.HTTP_201_CREATED)
def create_conference_paper(
    paper: ConferencePaperCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create conference papers")
    
    return crud_conference_paper.create_conference_paper(db=db, paper=paper, faculty_id=current_user.id)

@router.get("/conference-papers/faculty/{faculty_id}", response_model=List[ConferencePaperResponse])
def read_conference_papers_by_faculty(
    faculty_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's conference papers")
    
    papers = crud_conference_paper.get_conference_papers_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return papers

@router.get("/conference-papers", response_model=List[ConferencePaperResponse])
def read_all_conference_papers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all conference papers")
    
    papers = crud_conference_paper.get_all_conference_papers(db, skip=skip, limit=limit)
    return papers

@router.put("/conference-papers/{paper_id}", response_model=ConferencePaperResponse)
def update_conference_paper(
    paper_id: int,
    paper_update: ConferencePaperUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_paper = crud_conference_paper.get_conference_paper(db, paper_id)
    if db_paper is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conference Paper not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_paper = crud_conference_paper.update_conference_paper_faculty(db, paper_id, paper_update)
    elif "hod" in current_user.roles:
        if not isinstance(paper_update, ConferencePaperUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update research_score_hod")
        updated_paper = crud_conference_paper.update_conference_paper_hod(db, paper_id, paper_update)
    elif "director" in current_user.roles:
        if not isinstance(paper_update, ConferencePaperUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update research_score_director")
        updated_paper = crud_conference_paper.update_conference_paper_director(db, paper_id, paper_update)
    elif "faculty" in current_user.roles and db_paper.faculty_id == current_user.id:
        updated_paper = crud_conference_paper.update_conference_paper_faculty(db, paper_id, paper_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this conference paper")

    if updated_paper is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update conference paper")
    return updated_paper

@router.delete("/conference-papers/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conference_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_paper = crud_conference_paper.get_conference_paper(db, paper_id)
    if db_paper is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conference Paper not found")

    if "admin" not in current_user.roles and db_paper.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this conference paper")
    
    crud_conference_paper.delete_conference_paper(db, paper_id)
    return {"message": "Conference Paper deleted successfully"}

@router.get("/conference-papers/summary/{faculty_id}", response_model=ConferencePaperSummary)
def get_conference_papers_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_conference_paper.get_conference_papers_total_score(db, faculty_id)
    return ConferencePaperSummary(total_score=total_score)
