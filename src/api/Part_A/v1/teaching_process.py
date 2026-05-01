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
    sr_no: Optional[int] = Form(None, description="Serial number of the record"),
    semester: str = Form(..., description="Academic semester (e.g., Autumn 2025)"),
    course_code_name: str = Form(..., description="Code and name of the course"),
    planned_classes: int = Form(..., description="Number of classes planned"),
    conducted_classes: int = Form(..., description="Number of classes actually conducted"),
    department: Optional[str] = Form(None, description="Faculty department"),
    file: Optional[UploadFile] = File(None, description="PDF proof of teaching activities"),
    db: Session = Depends(get_db)
):
    """
    **Create a new Teaching Process entry (Lectures/Practicals).**

    - **URL Path:** `/api/v1/part-a/teaching-process`
    - **Role Required:** `faculty`
    - **Request Body (Form-Data):**
        - `sr_no` (int): Serial number.
        - `semester` (str): Semester name.
        - `course_code_name` (str): Course identifier.
        - `planned_classes` (int): Target number of classes.
        - `conducted_classes` (int): Actual classes held.
        - `department` (str): Department name.
        - `file` (file): PDF document proof.
    - **Response:**
        - Returns the created `TeachingProcessResponse` including `id`, `faculty_id`, and `api_score_faculty`.
    """
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
    faculty_id: Annotated[str, Path(description="UUID of the faculty member")],
    db: Session = Depends(get_db)
):
    """
    **Retrieve all teaching process entries for a specific faculty.**

    - **URL Path:** `/api/v1/part-a/teaching-process/faculty/{faculty_id}`
    - **Access Control:** User can see their own data; Higher authorities can see subordinates.
    - **Response:** List of teaching process objects.
    """
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this data")
    return crud_teaching_process.get_teaching_process_by_faculty(db, faculty_id)

@router.get("/teaching-process", response_model=List[TeachingProcessResponse])
def read_all_teaching_process(
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    **Retrieve all teaching process entries (Admin only).**

    - **URL Path:** `/api/v1/part-a/teaching-process`
    - **Response:** List of all teaching process objects.
    """
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all teaching data")
    # This would need a get_all_teaching_process in CRUD, or we just filter by nothing
    return db.query(crud_teaching_process.TeachingProcess).all()

@router.put("/teaching-process/{id}", response_model=TeachingProcessResponse)
def update_teaching_process(
    current_user: CurrentUser,
    id: Annotated[str, Path(description="UUID of the teaching process record")],
    teaching_update: TeachingProcessUpdateFaculty,
    db: Session = Depends(get_db)
):
    """
    **Update an existing teaching process record.**

    - **URL Path:** `/api/v1/part-a/teaching-process/{id}`
    - **Update Logic:**
        - **Faculty:** Can update basic teaching info.
        - **HOD/Admin:** Can update scores and verification status.
    - **Response:** The updated teaching process object.
    """
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
    id: Annotated[str, Path(description="UUID of the teaching process record")],
    db: Session = Depends(get_db)
):
    """
    **Delete a teaching process record (Admin only).**

    - **URL Path:** `/api/v1/part-a/teaching-process/{id}`
    - **Response:** 204 No Content.
    """
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_teaching_process.delete_teaching_process(db, id)
    return None

@router.get("/teaching-process/summary/{faculty_id}")
def read_teaching_process_summary(
    current_user: CurrentUser,
    faculty_id: Annotated[str, Path(description="UUID of the faculty member")],
    db: Session = Depends(get_db)
):
    """
    **Get the API score summary for teaching process.**

    - **URL Path:** `/api/v1/part-a/teaching-process/summary/{faculty_id}`
    - **Response:**
        - `totalMarksOutOf100`: Aggregated percentage of classes held.
        - `scaledMarksOutOf25`: Scaled score for final appraisal.
    """
    if not current_user.has_authority_over(faculty_id, "faculty"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    total_score = crud_teaching_process.get_teaching_process_total_score(db, faculty_id)
    return {
        "totalMarksOutOf100": total_score,
        "scaledMarksOutOf25": total_score * 0.25
    }
