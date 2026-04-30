from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ....setup.dependencies import get_db, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_B.research_guidance import (
    ResearchGuidanceCreate,
    ResearchGuidanceUpdateFaculty,
    ResearchGuidanceUpdateHOD,
    ResearchGuidanceUpdateDirector,
    ResearchGuidanceResponse,
    ResearchGuidanceSummary,
)
from ....crud.Part_B import research_guidance as crud_research_guidance

router = APIRouter()

@router.post("/research-guidance", response_model=ResearchGuidanceResponse, status_code=status.HTTP_201_CREATED)
async def create_research_guidance(
    current_user: CurrentUser,
    degree: str = Form(...),
    student_name: str = Form(...),
    submission_status: str = Form(...),
    award_date: Optional[date] = Form(None),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create research guidance entries")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    guidance = ResearchGuidanceCreate(
        degree=degree,
        student_name=student_name,
        submission_status=submission_status,
        award_date=award_date,
        department=department,
        document=document_path
    )
    
    return crud_research_guidance.create_research_guidance(db=db, guidance=guidance, faculty_id=current_user.id)

@router.get("/research-guidance/faculty/{faculty_id}", response_model=List[ResearchGuidanceResponse])
def read_research_guidance_by_faculty(
    current_user: CurrentUser,
    faculty_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's research guidance entries")
    
    guidance_entries = crud_research_guidance.get_research_guidance_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return guidance_entries

@router.get("/research-guidance", response_model=List[ResearchGuidanceResponse])
def read_all_research_guidance(
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all research guidance entries")
    
    guidance_entries = crud_research_guidance.get_all_research_guidance(db, skip=skip, limit=limit)
    return guidance_entries

@router.put("/research-guidance/{guidance_id}", response_model=ResearchGuidanceResponse)
def update_research_guidance(
    current_user: CurrentUser,
    guidance_id: str,
    guidance_update: ResearchGuidanceUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db)
):
    db_guidance = crud_research_guidance.get_research_guidance(db, guidance_id)
    if db_guidance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research Guidance entry not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_guidance = crud_research_guidance.update_research_guidance_faculty(db, guidance_id, guidance_update)
    elif "hod" in current_user.roles:
        if not isinstance(guidance_update, ResearchGuidanceUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update api_score_hod")
        updated_guidance = crud_research_guidance.update_research_guidance_hod(db, guidance_id, guidance_update)
    elif "director" in current_user.roles:
        if not isinstance(guidance_update, ResearchGuidanceUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update api_score_director")
        updated_guidance = crud_research_guidance.update_research_guidance_director(db, guidance_id, guidance_update)
    elif "faculty" in current_user.roles and db_guidance.faculty_id == current_user.id:
        updated_guidance = crud_research_guidance.update_research_guidance_faculty(db, guidance_id, guidance_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this research guidance entry")

    if updated_guidance is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update research guidance entry")
    return updated_guidance

@router.delete("/research-guidance/{guidance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research_guidance(
    current_user: CurrentUser,
    guidance_id: str,
    db: Session = Depends(get_db)
):
    db_guidance = crud_research_guidance.get_research_guidance(db, guidance_id)
    if db_guidance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research Guidance entry not found")

    if "admin" not in current_user.roles and db_guidance.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this research guidance entry")
    
    crud_research_guidance.delete_research_guidance(db, guidance_id)
    return {"message": "Research Guidance entry deleted successfully"}

@router.get("/research-guidance/summary/{faculty_id}", response_model=ResearchGuidanceSummary)
def get_research_guidance_summary(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    summary_data = crud_research_guidance.get_research_guidance_total_score(db, faculty_id)
    return ResearchGuidanceSummary(**summary_data)
