from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated

from ....setup.dependencies import get_db, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_A.qualification_enhancement import (
    QualificationEnhancementCreate,
    QualificationEnhancementUpdateFaculty,
    QualificationEnhancementUpdateHOD,
    QualificationEnhancementUpdateDirector,
    QualificationEnhancementResponse,
)
from ....crud.Part_A import qualification_enhancement as crud_qualification

router = APIRouter()

@router.post("/qualification-enhancement", response_model=QualificationEnhancementResponse, status_code=status.HTTP_201_CREATED)
async def create_qualification(
    current_user: CurrentUser,
    sr_no: Optional[int] = Form(None),
    qualification_type: str = Form(...),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can create entries")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    qualification_data = QualificationEnhancementCreate(
        sr_no=sr_no,
        qualification_type=qualification_type,
        department=department,
        document=document_path
    )
    return crud_qualification.create_qualification_enhancement(db, qualification_data, current_user.id)

@router.get("/qualification-enhancement/faculty/{faculty_id}", response_model=List[QualificationEnhancementResponse])
def read_qualifications_by_faculty(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return crud_qualification.get_qualification_enhancements_by_faculty(db, faculty_id)

@router.get("/qualification-enhancement", response_model=List[QualificationEnhancementResponse])
def read_all_qualifications(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all data")
    return db.query(crud_qualification.QualificationEnhancement).all()

@router.put("/qualification-enhancement/{id}", response_model=QualificationEnhancementResponse)
def update_qualification(
    current_user: CurrentUser,
    id: str,
    qualification_update: QualificationEnhancementUpdateFaculty,
    db: Session = Depends(get_db),
):
    db_entry = crud_qualification.get_qualification_enhancement(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "admin" in current_user.roles or "hod" in current_user.roles:
        return crud_qualification.update_qualification_enhancement_hod(db, id, qualification_update)
    elif "director" in current_user.roles:
        return crud_qualification.update_qualification_enhancement_director(db, id, qualification_update)
    elif "faculty" in current_user.roles and db_entry.faculty_id == current_user.id:
        return crud_qualification.update_qualification_enhancement_faculty(db, id, qualification_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.delete("/qualification-enhancement/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_qualification(
    current_user: CurrentUser,
    id: str,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_qualification.delete_qualification_enhancement(db, id)
    return None

@router.get("/qualification-enhancement/summary/{faculty_id}")
def read_qualification_summary(
    current_user: CurrentUser,
    faculty_id: Annotated[str, Path()],
    db: Session = Depends(get_db)
):
    if not current_user.has_authority_over(faculty_id, "faculty"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    total_score = crud_qualification.get_qualification_enhancement_total_score(db, faculty_id)
    return {"totalScore": total_score}
