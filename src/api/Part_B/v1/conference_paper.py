from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ....setup.dependencies import get_db, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
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

@router.post("/conferences", response_model=ConferencePaperResponse, status_code=status.HTTP_201_CREATED)
async def create_conference_paper(
    current_user: CurrentUser,
    event_title: str = Form(...),
    event_date: date = Form(...),
    activity_type: str = Form(...),
    hosting_organization: str = Form(...),
    event_level: str = Form(...),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create conference papers")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    paper = ConferencePaperCreate(
        event_title=event_title,
        event_date=event_date,
        activity_type=activity_type,
        hosting_organization=hosting_organization,
        event_level=event_level,
        department=department,
        document=document_path
    )
    
    return crud_conference_paper.create_conference_paper(db=db, paper=paper, faculty_id=current_user.id)

@router.get("/conferences/faculty/{faculty_id}", response_model=List[ConferencePaperResponse])
def read_conference_papers_by_faculty(
    current_user: CurrentUser,
    faculty_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's conference papers")
    
    papers = crud_conference_paper.get_conference_papers_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return papers

@router.get("/conferences", response_model=List[ConferencePaperResponse])
def read_all_conference_papers(
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all conference papers")
    
    papers = crud_conference_paper.get_all_conference_papers(db, skip=skip, limit=limit)
    return papers

@router.put("/conferences/{paper_id}", response_model=ConferencePaperResponse)
def update_conference_paper(
    current_user: CurrentUser,
    paper_id: str,
    paper_update: ConferencePaperUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db)
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

@router.delete("/conferences/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conference_paper(
    current_user: CurrentUser,
    paper_id: str,
    db: Session = Depends(get_db)
):
    db_paper = crud_conference_paper.get_conference_paper(db, paper_id)
    if db_paper is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conference Paper not found")

    if "admin" not in current_user.roles and db_paper.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this conference paper")
    
    crud_conference_paper.delete_conference_paper(db, paper_id)
    return {"message": "Conference Paper deleted successfully"}

@router.get("/conferences/summary/{faculty_id}", response_model=ConferencePaperSummary)
def get_conference_papers_summary(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_conference_paper.get_conference_papers_total_score(db, faculty_id)
    return ConferencePaperSummary(total_score=total_score)
