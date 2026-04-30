from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from ....setup.dependencies import get_db, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_B.self_development_fdp import (
    SelfDevelopmentFDPCreate,
    SelfDevelopmentFDPUpdateFaculty,
    SelfDevelopmentFDPUpdateHOD,
    SelfDevelopmentFDPUpdateDirector,
    SelfDevelopmentFDPResponse,
    SelfDevelopmentFDPSummary,
)
from ....crud.Part_B import self_development_fdp as crud_self_development_fdp

router = APIRouter()

@router.post("/self-development", response_model=SelfDevelopmentFDPResponse, status_code=status.HTTP_201_CREATED)
async def create_self_development_fdp(
    current_user: CurrentUser,
    program_name: str = Form(...),
    duration_days: int = Form(...),
    organizer: str = Form(...),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create self-development FDP entries")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    fdp = SelfDevelopmentFDPCreate(
        program_name=program_name,
        duration_days=duration_days,
        organizer=organizer,
        department=department,
        document=document_path
    )
    
    return crud_self_development_fdp.create_self_development_fdp(db=db, fdp=fdp, faculty_id=current_user.id)

@router.get("/self-development/faculty/{faculty_id}", response_model=List[SelfDevelopmentFDPResponse])
def read_self_development_fdp_by_faculty(
    current_user: CurrentUser,
    faculty_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's self-development FDP entries")
    
    fdp_entries = crud_self_development_fdp.get_self_development_fdp_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return fdp_entries

@router.get("/self-development", response_model=List[SelfDevelopmentFDPResponse])
def read_all_self_development_fdp(
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all self-development FDP entries")
    
    fdp_entries = crud_self_development_fdp.get_all_self_development_fdp(db, skip=skip, limit=limit)
    return fdp_entries

@router.put("/self-development/{fdp_id}", response_model=SelfDevelopmentFDPResponse)
def update_self_development_fdp(
    current_user: CurrentUser,
    fdp_id: str,
    fdp_update: SelfDevelopmentFDPUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db),
):
    db_fdp = crud_self_development_fdp.get_self_development_fdp(db, fdp_id)
    if db_fdp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Self-Development FDP entry not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_fdp = crud_self_development_fdp.update_self_development_fdp_faculty(db, fdp_id, fdp_update)
    elif "hod" in current_user.roles:
        if not isinstance(fdp_update, ResearchProjectUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update api_score_hod")
        updated_fdp = crud_self_development_fdp.update_self_development_fdp_hod(db, fdp_id, fdp_update)
    elif "director" in current_user.roles:
        if not isinstance(fdp_update, ResearchProjectUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update api_score_director")
        updated_fdp = crud_self_development_fdp.update_self_development_fdp_director(db, fdp_id, fdp_update)
    elif "faculty" in current_user.roles and db_fdp.faculty_id == current_user.id:
        updated_fdp = crud_self_development_fdp.update_self_development_fdp_faculty(db, fdp_id, fdp_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this self-development FDP entry")

    if updated_fdp is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update self-development FDP entry")
    return updated_fdp

@router.delete("/self-development/{fdp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_self_development_fdp(
    current_user: CurrentUser,
    fdp_id: str,
    db: Session = Depends(get_db),
):
    db_fdp = crud_self_development_fdp.get_self_development_fdp(db, fdp_id)
    if db_fdp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Self-Development FDP entry not found")

    if "admin" not in current_user.roles and db_fdp.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this self-development FDP entry")
    
    crud_self_development_fdp.delete_self_development_fdp(db, fdp_id)
    return {"message": "Self-Development FDP entry deleted successfully"}

@router.get("/self-development/summary/{faculty_id}", response_model=SelfDevelopmentFDPSummary)
def get_self_development_fdp_summary(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_self_development_fdp.get_self_development_fdp_total_score(db, faculty_id)
    return SelfDevelopmentFDPSummary(total_score=total_score)
