from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.student_feedback import StudentFeedback
from ...schema.Part_A.student_feedback import (
    StudentFeedbackCreate,
    StudentFeedbackUpdateFaculty,
    StudentFeedbackUpdateHOD,
    StudentFeedbackUpdateDirector,
)

def get_student_feedback(db: Session, id: int) -> Optional[StudentFeedback]:
    return db.query(StudentFeedback).filter(StudentFeedback.id == id).first()

def get_student_feedback_by_faculty(db: Session, faculty_id: int) -> List[StudentFeedback]:
    return db.query(StudentFeedback).filter(StudentFeedback.faculty_id == faculty_id).all()

def create_student_feedback(db: Session, feedback: StudentFeedbackCreate, faculty_id: int) -> StudentFeedback:
    db_feedback = StudentFeedback(**feedback.model_dump(), faculty_id=faculty_id)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def update_student_feedback_faculty(
    db: Session, id: int, feedback_update: StudentFeedbackUpdateFaculty
) -> Optional[StudentFeedback]:
    db_feedback = get_student_feedback(db, id)
    if db_feedback:
        update_data = feedback_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_feedback, key, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

def update_student_feedback_hod(
    db: Session, id: int, feedback_update: StudentFeedbackUpdateHOD
) -> Optional[StudentFeedback]:
    db_feedback = get_student_feedback(db, id)
    if db_feedback:
        db_feedback.api_score_hod = feedback_update.api_score_hod
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

def update_student_feedback_director(
    db: Session, id: int, feedback_update: StudentFeedbackUpdateDirector
) -> Optional[StudentFeedback]:
    db_feedback = get_student_feedback(db, id)
    if db_feedback:
        db_feedback.api_score_director = feedback_update.api_score_director
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

def delete_student_feedback(db: Session, id: int) -> bool:
    db_feedback = get_student_feedback(db, id)
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
        return True
    return False

def get_student_feedback_total_score(db: Session, faculty_id: int) -> float:
    entries = get_student_feedback_by_faculty(db, faculty_id)
    return sum([e.api_score_faculty for e in entries])
