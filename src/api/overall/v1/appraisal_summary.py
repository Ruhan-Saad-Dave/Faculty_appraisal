from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db, CurrentUser
from ....schema.overall.appraisal_summary import AppraisalSummaryResponse
from ....crud.overall import appraisal_summary as crud_appraisal_summary

router = APIRouter()

@router.get("/appraisal-summary/{faculty_id}", response_model=AppraisalSummaryResponse)
def get_appraisal_summary_endpoint(
    faculty_id: str,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    # Hierarchy check
    if not current_user.has_authority_over(faculty_id, "faculty"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's appraisal summary")
    
    summary = crud_appraisal_summary.get_appraisal_summary(db, faculty_id)
    return summary
