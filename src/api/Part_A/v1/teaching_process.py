from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated

from ....setup.dependencies import get_db, get_current_user, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_A.teaching_process import (
    TeachingProcessCreate,
    TeachingProcessUpdateFaculty,
    TeachingProcessUpdateHOD,
    TeachingProcessResponse,
)
from ....crud.Part_A import teaching_process as crud_teaching_process

router = APIRouter()

@router.post("/teaching-process", response_model=TeachingProcessResponse, status_code=status.HTTP_201_CREATED)
async def create_teaching_process(
    current_user: CurrentUser,
    sr_no: Optional[int] = Form(None),
    semester: str = Form(...),
    course_code_name: str = Form(...),
    planned_classes: int = Form(...),
    conducted_classes: int = Form(...),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can fill their own teaching data")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    teaching_data = TeachingProcessCreate(
        sr_no=sr_no,
        semester=semester,
        course_code_name=course_code_name,
        planned_classes=planned_classes,
        conducted_classes=conducted_classes,
        department=department,
        document=document_path
    )
    return crud_teaching_process.create_teaching_process(db, teaching_data, current_user.id)

@router.get("/teaching-process/faculty/{faculty_id}", response_model=List[TeachingProcessResponse])
def read_teaching_process_by_faculty(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this data")
    return crud_teaching_process.get_teaching_process_by_faculty(db, faculty_id)

@router.get("/teaching-process", response_model=List[TeachingProcessResponse])
def read_all_teaching_process(
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all teaching data")
    # This would need a get_all_teaching_process in CRUD, or we just filter by nothing
    return db.query(crud_teaching_process.TeachingProcess).all()

@router.put("/teaching-process/{id}", response_model=TeachingProcessResponse)
def update_teaching_process(
    current_user: CurrentUser,
    id: str,
    teaching_update: TeachingProcessUpdateFaculty, # Usually we'd use a Union or handle it inside
    db: Session = Depends(get_db)
):
    db_teaching = crud_teaching_process.get_teaching_process(db, id)
    if not db_teaching:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "admin" in current_user.roles:
        return crud_teaching_process.update_teaching_process_hod(db, id, teaching_update) # Admin can update everything
    elif "hod" in current_user.roles:
        return crud_teaching_process.update_teaching_process_hod(db, id, teaching_update)
    elif "faculty" in current_user.roles and db_teaching.faculty_id == current_user.id:
        return crud_teaching_process.update_teaching_process_faculty(db, id, teaching_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.delete("/teaching-process/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teaching_process(
    current_user: CurrentUser,
    id: str,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_teaching_process.delete_teaching_process(db, id)
    return None

@router.get("/teaching-process/summary/{faculty_id}")
def read_teaching_process_summary(
    current_user: CurrentUser,
    faculty_id: Annotated[str, Path()],
    db: Session = Depends(get_db)
):
    if not current_user.has_authority_over(faculty_id, "faculty"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    total_score = crud_teaching_process.get_teaching_process_total_score(db, faculty_id)
    return {
        "totalMarksOutOf100": total_score,
        "scaledMarksOutOf25": total_score * 0.25
    }
