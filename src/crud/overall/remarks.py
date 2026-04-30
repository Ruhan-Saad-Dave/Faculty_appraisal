from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from ...models.overall.remarks import AppraisalRemarks, HODRemarks, DirectorRemarks, DeanRemarks, FinalApproval
from ...schema.overall.remarks import (
    AppraisalRemarksCreate, HODRemarksCreate, DirectorRemarksCreate, 
    DeanRemarksCreate, FinalApprovalCreate
)

# Appraisal Remarks (General)
def get_appraisal_remarks_by_faculty(db: Session, faculty_id: str) -> List[AppraisalRemarks]:
    return db.query(AppraisalRemarks).filter(AppraisalRemarks.faculty_id == faculty_id).all()

def create_appraisal_remarks(db: Session, faculty_id: str, data: AppraisalRemarksCreate) -> AppraisalRemarks:
    db_remarks = AppraisalRemarks(**data.model_dump(), faculty_id=faculty_id)
    db.add(db_remarks)
    db.commit()
    db.refresh(db_remarks)
    return db_remarks

# HOD Remarks
def get_hod_remarks_by_faculty(db: Session, faculty_id: str) -> Optional[HODRemarks]:
    return db.query(HODRemarks).filter(HODRemarks.faculty_id == faculty_id).first()

def create_or_update_hod_remarks(db: Session, faculty_id: str, data: HODRemarksCreate) -> HODRemarks:
    db_remarks = get_hod_remarks_by_faculty(db, faculty_id)
    if db_remarks:
        for key, value in data.model_dump().items():
            setattr(db_remarks, key, value)
    else:
        db_remarks = HODRemarks(**data.model_dump(), faculty_id=faculty_id)
        db.add(db_remarks)
    db.commit()
    db.refresh(db_remarks)
    return db_remarks

# Director Remarks
def get_director_remarks_by_faculty(db: Session, faculty_id: str) -> Optional[DirectorRemarks]:
    return db.query(DirectorRemarks).filter(DirectorRemarks.faculty_id == faculty_id).first()

def create_or_update_director_remarks(db: Session, faculty_id: str, data: DirectorRemarksCreate) -> DirectorRemarks:
    db_remarks = get_director_remarks_by_faculty(db, faculty_id)
    if db_remarks:
        for key, value in data.model_dump().items():
            setattr(db_remarks, key, value)
    else:
        db_remarks = DirectorRemarks(**data.model_dump(), faculty_id=faculty_id)
        db.add(db_remarks)
    db.commit()
    db.refresh(db_remarks)
    return db_remarks

# Dean Remarks
def get_dean_remarks_by_faculty(db: Session, faculty_id: str) -> Optional[DeanRemarks]:
    return db.query(DeanRemarks).filter(DeanRemarks.faculty_id == faculty_id).first()

def create_or_update_dean_remarks(db: Session, faculty_id: str, data: DeanRemarksCreate) -> DeanRemarks:
    db_remarks = get_dean_remarks_by_faculty(db, faculty_id)
    if db_remarks:
        for key, value in data.model_dump().items():
            setattr(db_remarks, key, value)
    else:
        db_remarks = DeanRemarks(**data.model_dump(), faculty_id=faculty_id)
        db.add(db_remarks)
    db.commit()
    db.refresh(db_remarks)
    return db_remarks

# Final Approval (VC)
def get_final_approval_by_faculty(db: Session, faculty_id: str) -> Optional[FinalApproval]:
    return db.query(FinalApproval).filter(FinalApproval.faculty_id == faculty_id).first()

def create_or_update_final_approval(db: Session, faculty_id: str, data: FinalApprovalCreate) -> FinalApproval:
    db_approval = get_final_approval_by_faculty(db, faculty_id)
    if db_approval:
        for key, value in data.model_dump().items():
            setattr(db_approval, key, value)
    else:
        db_approval = FinalApproval(**data.model_dump(), faculty_id=faculty_id)
        db.add(db_approval)
    db.commit()
    db.refresh(db_approval)
    return db_approval
