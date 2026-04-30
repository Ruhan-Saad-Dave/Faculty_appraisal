from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from ....setup.dependencies import get_db, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_B.research_proposal import (
    ResearchProposalCreate,
    ResearchProposalUpdateFaculty,
    ResearchProposalUpdateHOD,
    ResearchProposalUpdateDirector,
    ResearchProposalResponse,
    ResearchProposalSummary,
)
from ....crud.Part_B import research_proposal as crud_research_proposal

router = APIRouter()

@router.post("/research-proposals", response_model=ResearchProposalResponse, status_code=status.HTTP_201_CREATED)
async def create_research_proposal(
    current_user: CurrentUser,
    proposal_title: str = Form(...),
    duration: str = Form(...),
    funding_agency: str = Form(...),
    grant_amount: float = Form(...),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create research proposals")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    proposal = ResearchProposalCreate(
        proposal_title=proposal_title,
        duration=duration,
        funding_agency=funding_agency,
        grant_amount=grant_amount,
        department=department,
        document=document_path
    )
    
    return crud_research_proposal.create_research_proposal(db=db, proposal=proposal, faculty_id=current_user.id)

@router.get("/research-proposals/faculty/{faculty_id}", response_model=List[ResearchProposalResponse])
def read_research_proposals_by_faculty(
    current_user: CurrentUser,
    faculty_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's research proposals")
    
    proposals = crud_research_proposal.get_research_proposals_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return proposals

@router.get("/research-proposals", response_model=List[ResearchProposalResponse])
def read_all_research_proposals(
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all research proposals")
    
    proposals = crud_research_proposal.get_all_research_proposals(db, skip=skip, limit=limit)
    return proposals

@router.put("/research-proposals/{proposal_id}", response_model=ResearchProposalResponse)
def update_research_proposal(
    current_user: CurrentUser,
    proposal_id: str,
    proposal_update: ResearchProposalUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db),
):
    db_proposal = crud_research_proposal.get_research_proposal(db, proposal_id)
    if db_proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research Proposal not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_proposal = crud_research_proposal.update_research_proposal_faculty(db, proposal_id, proposal_update)
    elif "hod" in current_user.roles:
        if not isinstance(proposal_update, ResearchProposalUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update api_score_hod")
        updated_proposal = crud_research_proposal.update_research_proposal_hod(db, proposal_id, proposal_update)
    elif "director" in current_user.roles:
        if not isinstance(proposal_update, ResearchProposalUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update api_score_director")
        updated_proposal = crud_research_proposal.update_research_proposal_director(db, proposal_id, proposal_update)
    elif "faculty" in current_user.roles and db_proposal.faculty_id == current_user.id:
        updated_proposal = crud_research_proposal.update_research_proposal_faculty(db, proposal_id, proposal_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this research proposal")

    if updated_proposal is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update research proposal")
    return updated_proposal

@router.delete("/research-proposals/{proposal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research_proposal(
    current_user: CurrentUser,
    proposal_id: str,
    db: Session = Depends(get_db),
):
    db_proposal = crud_research_proposal.get_research_proposal(db, proposal_id)
    if db_proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research Proposal not found")

    if "admin" not in current_user.roles and db_proposal.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this research proposal")
    
    crud_research_proposal.delete_research_proposal(db, proposal_id)
    return {"message": "Research Proposal deleted successfully"}

@router.get("/research-proposals/summary/{faculty_id}", response_model=ResearchProposalSummary)
def get_research_proposals_summary(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_research_proposal.get_research_proposals_total_score(db, faculty_id)
    return ResearchProposalSummary(total_score=total_score)
