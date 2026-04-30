from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated, Union

from ....setup.dependencies import get_db, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_A.departmental_activities import (
    DepartmentalActivityCreate,
    DepartmentalActivityUpdateFaculty,
    DepartmentalActivityUpdateHOD,
    DepartmentalActivityUpdateDirector,
    DepartmentalActivityResponse,
)
from ....crud.Part_A import departmental_activities as crud_activities

router = APIRouter()

@router.post("/department-activities", response_model=DepartmentalActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    current_user: CurrentUser,
    activity: Annotated[str, Form()],
    nature_of_activity: Annotated[str, Form()],
    db: Annotated[Session, Depends(get_db)],
    sr_no: Annotated[Optional[int], Form()] = None,
    department: Annotated[Optional[str], Form()] = None,
    file: Annotated[Optional[UploadFile], File()] = None,
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can create entries")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    activity_data = DepartmentalActivityCreate(
        sr_no=sr_no,
        activity=activity,
        nature_of_activity=nature_of_activity,
        department=department,
        document=document_path
    )
    return crud_activities.create_departmental_activity(db, activity_data, current_user.id)

@router.get("/department-activities/faculty/{faculty_id}", response_model=List[DepartmentalActivityResponse])
def read_activities_by_faculty(
    current_user: CurrentUser,
    faculty_id: Annotated[str, Path()],
    db: Annotated[Session, Depends(get_db)]
):
    if not current_user.has_authority_over(faculty_id, "faculty"):
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud_activities.get_departmental_activities_by_faculty(db, faculty_id)

@router.get("/department-activities", response_model=List[DepartmentalActivityResponse])
def read_all_activities(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)]
):
    allowed_roles = {"admin", "dean", "vc"}
    if not any(role in allowed_roles for role in current_user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin, dean, or vc can view all data")
    return db.query(crud_activities.DepartmentalActivity).all()

@router.put("/department-activities/{id}", response_model=DepartmentalActivityResponse)
def update_activity(
    current_user: CurrentUser,
    id: Annotated[str, Path()],
    activity_update: Union[DepartmentalActivityUpdateFaculty, DepartmentalActivityUpdateHOD, DepartmentalActivityUpdateDirector],
    db: Annotated[Session, Depends(get_db)]
):
    db_entry = crud_activities.get_departmental_activity(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if not current_user.has_authority_over(db_entry.faculty_id, "faculty", db_entry.department):
        raise HTTPException(status_code=403, detail="Not authorized")

    if current_user.id == db_entry.faculty_id and "faculty" in current_user.roles:
        return crud_activities.update_departmental_activity_faculty(db, id, activity_update)
    
    if "hod" in current_user.roles or "admin" in current_user.roles:
        return crud_activities.update_departmental_activity_hod(db, id, activity_update)
    elif "director" in current_user.roles:
        return crud_activities.update_departmental_activity_director(db, id, activity_update)
    else:
        # Fallback for higher roles (Dean/VC) who have authority
        return crud_activities.update_departmental_activity_hod(db, id, activity_update)

@router.delete("/department-activities/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    current_user: CurrentUser,
    id: Annotated[str, Path()],
    db: Annotated[Session, Depends(get_db)]
):
    db_entry = crud_activities.get_departmental_activity(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if not current_user.has_authority_over(db_entry.faculty_id, "faculty", db_entry.department):
        raise HTTPException(status_code=403, detail="Not authorized")

    crud_activities.delete_departmental_activity(db, id)
    return None

@router.get("/department-activities/summary/{faculty_id}")
def get_activity_summary(
    current_user: CurrentUser,
    faculty_id: Annotated[str, Path()],
    db: Annotated[Session, Depends(get_db)]
):
    if not current_user.has_authority_over(faculty_id, "faculty"):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    activities = crud_activities.get_departmental_activities_by_faculty(db, faculty_id)
    total_score = sum([a.api_score_faculty for a in activities])
    return {"totalScore": min(total_score, 20)}
