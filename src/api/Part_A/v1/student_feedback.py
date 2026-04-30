from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from ....setup.dependencies import get_db, get_current_user, CurrentUser
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_A.student_feedback import (
    StudentFeedbackCreate,
    StudentFeedbackUpdateFaculty,
    StudentFeedbackUpdateHOD,
    StudentFeedbackUpdateDirector,
    StudentFeedbackResponse,
)
from ....crud.Part_A import student_feedback as crud_student_feedback

router = APIRouter()

@router.post("/student-feedback", response_model=StudentFeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    current_user: CurrentUser,
    sr_no: Optional[int] = Form(None),
    course_code_name: str = Form(...),
    first_feedback: float = Form(...),
    second_feedback: float = Form(...),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can create entries")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    feedback_data = StudentFeedbackCreate(
        sr_no=sr_no,
        course_code_name=course_code_name,
        first_feedback=first_feedback,
        second_feedback=second_feedback,
        department=department,
        document=document_path
    )
    return crud_student_feedback.create_student_feedback(db, feedback_data, current_user.id)

@router.get("/student-feedback/faculty/{faculty_id}", response_model=List[StudentFeedbackResponse])
def read_feedback_by_faculty(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return crud_student_feedback.get_student_feedback_by_faculty(db, faculty_id)

@router.get("/student-feedback", response_model=List[StudentFeedbackResponse])
def read_all_feedback(
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all data")
    return db.query(crud_student_feedback.StudentFeedback).all()

@router.put("/student-feedback/{id}", response_model=StudentFeedbackResponse)
def update_feedback(
    current_user: CurrentUser,
    id: str,
    feedback_update: StudentFeedbackUpdateFaculty,
    db: Session = Depends(get_db)
):
    db_entry = crud_student_feedback.get_student_feedback(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "admin" in current_user.roles or "hod" in current_user.roles:
        return crud_student_feedback.update_student_feedback_hod(db, id, feedback_update)
    elif "director" in current_user.roles:
        return crud_student_feedback.update_student_feedback_director(db, id, feedback_update)
    elif "faculty" in current_user.roles and db_entry.faculty_id == current_user.id:
        return crud_student_feedback.update_student_feedback_faculty(db, id, feedback_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.delete("/student-feedback/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(
    current_user: CurrentUser,
    id: str,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_student_feedback.delete_student_feedback(db, id)
    return None

@router.get("/student-feedback/summary/{faculty_id}")
def get_feedback_summary(
    current_user: CurrentUser,
    faculty_id: str,
    db: Session = Depends(get_db)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    feedbacks = crud_student_feedback.get_student_feedback_by_faculty(db, faculty_id)
    if not feedbacks:
        return {"overallAverage": 0.0}
    
    total_avg = sum([(f.first_feedback + f.second_feedback) / 2 for f in feedbacks])
    overall_avg = total_avg / len(feedbacks)
    return {"overallAverage": overall_avg}
