from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_B.ipr import (
    IPRCreate,
    IPRUpdateFaculty,
    IPRUpdateHOD,
    IPRUpdateDirector,
    IPRResponse,
    IPRSummary,
)
from ....crud.Part_B import ipr as crud_ipr
from ....models.Part_B.ipr import IPR as DBIPR

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    # This is a mock user for demonstration. Replace with actual authentication.
    return User(id=1, roles=["faculty"]) # Default to faculty for now

@router.post("/ipr", response_model=IPRResponse, status_code=status.HTTP_201_CREATED)
def create_ipr(
    ipr: IPRCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create IPR entries")
    
    return crud_ipr.create_ipr(db=db, ipr=ipr, faculty_id=current_user.id)

@router.get("/ipr/faculty/{faculty_id}", response_model=List[IPRResponse])
def read_ipr_by_faculty(
    faculty_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's IPR entries")
    
    ipr_entries = crud_ipr.get_ipr_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return ipr_entries

@router.get("/ipr", response_model=List[IPRResponse])
def read_all_ipr(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all IPR entries")
    
    ipr_entries = crud_ipr.get_all_ipr(db, skip=skip, limit=limit)
    return ipr_entries

@router.put("/ipr/{ipr_id}", response_model=IPRResponse)
def update_ipr(
    ipr_id: int,
    ipr_update: IPRUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ipr = crud_ipr.get_ipr(db, ipr_id)
    if db_ipr is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IPR entry not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_ipr = crud_ipr.update_ipr_faculty(db, ipr_id, ipr_update)
    elif "hod" in current_user.roles:
        if not isinstance(ipr_update, IPRUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update research_score_hod")
        updated_ipr = crud_ipr.update_ipr_hod(db, ipr_id, ipr_update)
    elif "director" in current_user.roles:
        if not isinstance(ipr_update, IPRUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update research_score_director")
        updated_ipr = crud_ipr.update_ipr_director(db, ipr_id, ipr_update)
    elif "faculty" in current_user.roles and db_ipr.faculty_id == current_user.id:
        updated_ipr = crud_ipr.update_ipr_faculty(db, ipr_id, ipr_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this IPR entry")

    if updated_ipr is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update IPR entry")
    return updated_ipr

@router.delete("/ipr/{ipr_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ipr(
    ipr_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ipr = crud_ipr.get_ipr(db, ipr_id)
    if db_ipr is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IPR entry not found")

    if "admin" not in current_user.roles and db_ipr.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this IPR entry")
    
    crud_ipr.delete_ipr(db, ipr_id)
    return {"message": "IPR entry deleted successfully"}

@router.get("/ipr/summary/{faculty_id}", response_model=IPRSummary)
def get_ipr_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_ipr.get_ipr_total_score(db, faculty_id)
    return IPRSummary(total_score=total_score)
