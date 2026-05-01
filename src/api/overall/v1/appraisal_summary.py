from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db, CurrentUser
from ....schema.overall.appraisal_summary import AppraisalSummaryResponse, AppraisalSubmitRequest, AppraisalSubmitResponse
from ....crud.overall import appraisal_summary as crud_appraisal_summary
from ....crud.overall import appraisal_tracking
from ....models.overall.appraisal_summary import AppraisalStatus

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

@router.post("/appraisal-summary/submit", response_model=AppraisalSubmitResponse)
def submit_appraisal(
    request: AppraisalSubmitRequest,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Finalizes the appraisal form for the faculty member and updates status to SUBMITTED.
    """
    # 1. Calculate current final score
    summary = crud_appraisal_summary.get_appraisal_summary(db, current_user.id)
    
    # 2. Update tracking status to SUBMITTED
    db_summary = appraisal_tracking.create_or_update_summary_status(
        db, 
        faculty_id=current_user.id,
        status=AppraisalStatus.SUBMITTED,
        academic_year=request.academic_year,
        overall_score=summary.grand_total_score
    )
    
    return AppraisalSubmitResponse(
        faculty_id=db_summary.faculty_id,
        status=db_summary.status,
        overall_score=db_summary.overall_score,
        academic_year=db_summary.academic_year
    )
