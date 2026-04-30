from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from ....setup.dependencies import get_db, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_B.ict_pedagogy import (
    ICTPedagogyCreate,
    ICTPedagogyUpdateFaculty,
    ICTPedagogyUpdateHOD,
    ICTPedagogyUpdateDirector,
    ICTPedagogyResponse,
    ICTPedagogySummary,
)
from ....crud.Part_B import ict_pedagogy as crud_ict_pedagogy
from ....models.Part_B.ict_pedagogy import ICTPedagogy as DBICTPedagogy

router = APIRouter()

@router.post("/pedagogy", response_model=ICTPedagogyResponse, status_code=status.HTTP_201_CREATED)
async def create_ict_pedagogy(
    current_user: CurrentUser,
    title: str = Form(...),
    description: str = Form(...),
    pedagogy_type: str = Form(...),
    quadrants: int = Form(...),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create ICT pedagogies")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    pedagogy = ICTPedagogyCreate(
        title=title,
        description=description,
        pedagogy_type=pedagogy_type,
        quadrants=quadrants,
        department=department,
        document=document_path
    )
    
    return crud_ict_pedagogy.create_ict_pedagogy(db=db, pedagogy=pedagogy, faculty_id=current_user.id)

@router.get("/pedagogy/faculty/{faculty_id}", response_model=List[ICTPedagogyResponse])
def read_ict_pedagogies_by_faculty(
    current_user: CurrentUser,
    faculty_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's ICT pedagogies")
    
    pedagogies = crud_ict_pedagogy.get_ict_pedagogies_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return pedagogies

@router.get("/pedagogy", response_model=List[ICTPedagogyResponse])
def read_all_ict_pedagogies(
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all ICT pedagogies")
    
    pedagogies = crud_ict_pedagogy.get_all_ict_pedagogies(db, skip=skip, limit=limit)
    return pedagogies

@router.put("/pedagogy/{pedagogy_id}", response_model=ICTPedagogyResponse)
def update_ict_pedagogy(
    current_user: CurrentUser,
    pedagogy_id: str,
    pedagogy_update: ICTPedagogyUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db)
):
    db_pedagogy = crud_ict_pedagogy.get_ict_pedagogy(db, pedagogy_id)
    if db_pedagogy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ICT Pedagogy entry not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_pedagogy = crud_ict_pedagogy.update_ict_pedagogy_faculty(db, pedagogy_id, pedagogy_update)
    elif "hod" in current_user.roles:
        if not isinstance(pedagogy_update, ICTPedagogyUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update api_score_hod")
        updated_pedagogy = crud_ict_pedagogy.update_ict_pedagogy_hod(db, pedagogy_id, pedagogy_update)
    elif "director" in current_user.roles:
        if not isinstance(pedagogy_update, ICTPedagogyUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update api_score_director")
        updated_pedagogy = crud_ict_pedagogy.update_ict_pedagogy_director(db, pedagogy_id, pedagogy_update)
    elif "faculty" in current_user.roles and db_pedagogy.faculty_id == current_user.id:
        updated_pedagogy = crud_ict_pedagogy.update_ict_pedagogy_faculty(db, pedagogy_id, pedagogy_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this ICT pedagogy entry")

    if updated_pedagogy is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update ICT pedagogy entry")
    return updated_pedagogy

@router.delete("/pedagogy/{pedagogy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ict_pedagogy(
    current_user: CurrentUser,
    pedagogy_id: str,
    db: Session = Depends(get_db)
):
    db_pedagogy = crud_ict_pedagogy.get_ict_pedagogy(db, pedagogy_id)
    if db_pedagogy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ICT Pedagogy entry not found")

    if "admin" not in current_user.roles and db_pedagogy.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this ICT pedagogy entry")
    
    crud_ict_pedagogy.delete_ict_pedagogy(db, pedagogy_id)
    return {"message": "ICT Pedagogy entry deleted successfully"}

@router.get("/pedagogy/summary/{faculty_id}", response_model=ICTPedagogySummary)
def get_ict_pedagogies_summary(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_ict_pedagogy.get_ict_pedagogies_total_score(db, faculty_id)
    return ICTPedagogySummary(total_score=total_score)
