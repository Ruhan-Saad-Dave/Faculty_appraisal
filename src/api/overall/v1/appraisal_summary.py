from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.overall.appraisal_summary import AppraisalSummaryResponse
from ....crud.overall import appraisal_summary as crud_appraisal_summary

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    # This is a mock user for demonstration. Replace with actual authentication.
    return User(id=1, roles=["faculty"]) # Default to faculty for now

@router.get("/appraisal-summary/{faculty_id}", response_model=AppraisalSummaryResponse)
def get_appraisal_summary_endpoint(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's appraisal summary")
    
    summary = crud_appraisal_summary.get_appraisal_summary(db, faculty_id)
    return summary
