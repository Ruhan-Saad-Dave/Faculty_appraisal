from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.social_contributions import SocialContribution
from ...schema.Part_A.social_contributions import (
    SocialContributionCreate,
    SocialContributionUpdateFaculty,
    SocialContributionUpdateHOD,
    SocialContributionUpdateDirector,
)

def get_social_contribution(db: Session, id: int) -> Optional[SocialContribution]:
    return db.query(SocialContribution).filter(SocialContribution.id == id).first()

def get_social_contributions_by_faculty(db: Session, faculty_id: int) -> List[SocialContribution]:
    return db.query(SocialContribution).filter(SocialContribution.faculty_id == faculty_id).all()

def create_social_contribution(
    db: Session, contribution: SocialContributionCreate, faculty_id: int
) -> SocialContribution:
    db_contribution = SocialContribution(**contribution.model_dump(), faculty_id=faculty_id)
    db.add(db_contribution)
    db.commit()
    db.refresh(db_contribution)
    return db_contribution

def update_social_contribution_faculty(
    db: Session, id: int, contribution_update: SocialContributionUpdateFaculty
) -> Optional[SocialContribution]:
    db_contribution = get_social_contribution(db, id)
    if db_contribution:
        update_data = contribution_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contribution, key, value)
        db.commit()
        db.refresh(db_contribution)
    return db_contribution

def update_social_contribution_hod(
    db: Session, id: int, contribution_update: SocialContributionUpdateHOD
) -> Optional[SocialContribution]:
    db_contribution = get_social_contribution(db, id)
    if db_contribution:
        db_contribution.api_score_hod = contribution_update.api_score_hod
        db.commit()
        db.refresh(db_contribution)
    return db_contribution

def update_social_contribution_director(
    db: Session, id: int, contribution_update: SocialContributionUpdateDirector
) -> Optional[SocialContribution]:
    db_contribution = get_social_contribution(db, id)
    if db_contribution:
        db_contribution.api_score_director = contribution_update.api_score_director
        db.commit()
        db.refresh(db_contribution)
    return db_contribution

def delete_social_contribution(db: Session, id: int) -> bool:
    db_contribution = get_social_contribution(db, id)
    if db_contribution:
        db.delete(db_contribution)
        db.commit()
        return True
    return False

def get_social_contribution_total_score(db: Session, faculty_id: int) -> float:
    entries = get_social_contributions_by_faculty(db, faculty_id)
    return sum([e.api_score_faculty for e in entries])
