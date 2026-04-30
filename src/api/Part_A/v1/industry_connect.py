from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from ....setup.dependencies import get_db, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_A.industry_connect import (
    IndustryConnectCreate,
    IndustryConnectUpdateFaculty,
    IndustryConnectUpdateHOD,
    IndustryConnectUpdateDirector,
    IndustryConnectResponse,
)
from ....crud.Part_A import industry_connect as crud_activities

router = APIRouter()

@router.post("/industry-connect", response_model=IndustryConnectResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    current_user: CurrentUser,
    sr_no: Optional[int] = Form(None),
    industry_name: str = Form(...),
    details_of_activity: str = Form(...),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can create entries")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    connect_data = IndustryConnectCreate(
        sr_no=sr_no,
        industry_name=industry_name,
        details_of_activity=details_of_activity,
        department=department,
        document=document_path
    )
    return crud_activities.create_industry_connect(db, connect_data, current_user.id)

@router.get("/industry-connect/faculty/{faculty_id}", response_model=List[IndustryConnectResponse])
def read_activities_by_faculty(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return crud_activities.get_industry_connect_by_faculty(db, faculty_id)

@router.get("/industry-connect", response_model=List[IndustryConnectResponse])
def read_all_activities(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all data")
    return db.query(crud_activities.IndustryConnect).all()

@router.put("/industry-connect/{id}", response_model=IndustryConnectResponse)
def update_activity(
    current_user: CurrentUser,
    id: str,
    connect_update: IndustryConnectUpdateFaculty,
    db: Session = Depends(get_db),
):
    db_entry = crud_activities.get_industry_connect(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "admin" in current_user.roles or "hod" in current_user.roles:
        return crud_activities.update_industry_connect_hod(db, id, connect_update)
    elif "director" in current_user.roles:
        return crud_activities.update_industry_connect_director(db, id, connect_update)
    elif "faculty" in current_user.roles and db_entry.faculty_id == current_user.id:
        return crud_activities.update_industry_connect_faculty(db, id, connect_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.delete("/industry-connect/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    current_user: CurrentUser,
    id: str,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_activities.delete_industry_connect(db, id)
    return None

@router.get("/industry-connect/summary/{faculty_id}")
def get_activity_summary(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db),
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    activities = crud_activities.get_industry_connect_by_faculty(db, faculty_id)
    total_score = sum([a.api_score_faculty for a in activities])
    return {"totalScore": min(total_score, 5)} # Max 5 as per PDF
