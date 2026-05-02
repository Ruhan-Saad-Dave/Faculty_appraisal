from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ....setup.dependencies import get_db, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_B.popular_writings import (
    PopularWritingCreate,
    PopularWritingUpdate,
    PopularWritingResponse,
    PopularWritingSummary,
)
from ....crud.Part_B import popular_writings as crud_popular_writings

router = APIRouter()

@router.post("/popular-writings", response_model=PopularWritingResponse, status_code=status.HTTP_201_CREATED)
async def create_popular_writing(
    current_user: CurrentUser,
    title: str = Form(...),
    writing_type: str = Form(...),
    date: str = Form(...),
    publisher_agency: Optional[str] = Form(None),
    sr_no: Optional[int] = Form(None),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create entries")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    writing_data = PopularWritingCreate(
        title=title,
        writing_type=writing_type,
        date=date,
        publisher_agency=publisher_agency,
        sr_no=sr_no,
        department=department,
        document=document_path
    )
    
    return crud_popular_writings.create_popular_writing(db=db, writing=writing_data, faculty_id=current_user.id)

@router.get("/popular-writings/faculty/{faculty_id}", response_model=List[PopularWritingResponse])
def read_popular_writings_by_faculty(
    current_user: CurrentUser,
    faculty_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    # Authority check
    if not current_user.has_authority_over(str(faculty_id), "faculty"):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    return crud_popular_writings.get_popular_writings_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)

@router.get("/popular-writings/{writing_id}", response_model=PopularWritingResponse)
def read_popular_writing(
    current_user: CurrentUser,
    writing_id: UUID,
    db: Session = Depends(get_db)
):
    db_writing = crud_popular_writings.get_popular_writing(db, writing_id)
    if not db_writing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        
    if not current_user.has_authority_over(str(db_writing.faculty_id), "faculty"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        
    return db_writing

@router.put("/popular-writings/{writing_id}", response_model=PopularWritingResponse)
def update_popular_writing(
    current_user: CurrentUser,
    writing_id: UUID,
    writing_update: PopularWritingUpdate,
    db: Session = Depends(get_db)
):
    db_writing = crud_popular_writings.get_popular_writing(db, writing_id)
    if not db_writing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    # Only faculty can update their own details, others can only update scores
    if "faculty" in current_user.roles and str(db_writing.faculty_id) == str(current_user.id):
        # Faculty can update everything except scores
        writing_update.api_score_hod = None
        writing_update.api_score_director = None
    elif "hod" in current_user.roles or "director" in current_user.roles or "admin" in current_user.roles:
        # Check authority
        if not current_user.has_authority_over(str(db_writing.faculty_id), "faculty"):
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return crud_popular_writings.update_popular_writing(db, writing_id, writing_update)

@router.delete("/popular-writings/{writing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_popular_writing(
    current_user: CurrentUser,
    writing_id: UUID,
    db: Session = Depends(get_db)
):
    db_writing = crud_popular_writings.get_popular_writing(db, writing_id)
    if not db_writing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if str(db_writing.faculty_id) != str(current_user.id) and "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    crud_popular_writings.delete_popular_writing(db, writing_id)
    return None

@router.get("/popular-writings/summary/{faculty_id}", response_model=PopularWritingSummary)
def get_popular_writings_summary(
    current_user: CurrentUser,
    faculty_id: UUID,
    db: Session = Depends(get_db)
):
    if not current_user.has_authority_over(str(faculty_id), "faculty"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    total_score = crud_popular_writings.get_popular_writings_total_score(db, faculty_id)
    return PopularWritingSummary(total_score=total_score)
