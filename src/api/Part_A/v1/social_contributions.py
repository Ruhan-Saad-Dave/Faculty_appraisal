from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_A.social_contributions import (
    SocialContributionCreate,
    SocialContributionUpdateFaculty,
    SocialContributionUpdateHOD,
    SocialContributionUpdateDirector,
    SocialContributionResponse,
)
from ....crud.Part_A import social_contributions as crud_activities

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    return User(id=1, roles=["faculty"])

@router.post("/social-contributions", response_model=SocialContributionResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    contribution: SocialContributionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only faculty can create entries")
    return crud_activities.create_social_contribution(db, contribution, current_user.id)

@router.get("/social-contributions/faculty/{faculty_id}", response_model=List[SocialContributionResponse])
def read_activities_by_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return crud_activities.get_social_contributions_by_faculty(db, faculty_id)

@router.get("/social-contributions", response_model=List[SocialContributionResponse])
def read_all_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all data")
    return db.query(crud_activities.SocialContribution).all()

@router.put("/social-contributions/{id}", response_model=SocialContributionResponse)
def update_activity(
    id: int,
    contribution_update: SocialContributionUpdateFaculty,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_entry = crud_activities.get_social_contribution(db, id)
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if "admin" in current_user.roles or "hod" in current_user.roles:
        return crud_activities.update_social_contribution_hod(db, id, contribution_update)
    elif "director" in current_user.roles:
        return crud_activities.update_social_contribution_director(db, id, contribution_update)
    elif "faculty" in current_user.roles and db_entry.faculty_id == current_user.id:
        return crud_activities.update_social_contribution_faculty(db, id, contribution_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.delete("/social-contributions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete entries")
    crud_activities.delete_social_contribution(db, id)
    return None

@router.get("/social-contributions/summary/{faculty_id}")
def get_activity_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    activities = crud_activities.get_social_contributions_by_faculty(db, faculty_id)
    total_score = sum([a.api_score_faculty for a in activities])
    return {"totalScore": min(total_score, 10)} # Max 10 as per PDF
