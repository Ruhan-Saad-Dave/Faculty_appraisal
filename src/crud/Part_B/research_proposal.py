from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.Part_B.research_proposal import ResearchProposal
from ..schema.Part_B.research_proposal import (
    ResearchProposalCreate,
    ResearchProposalUpdateFaculty,
    ResearchProposalUpdateHOD,
    ResearchProposalUpdateDirector,
)

def get_research_proposal(db: Session, proposal_id: int) -> Optional[ResearchProposal]:
    return db.query(ResearchProposal).filter(ResearchProposal.id == proposal_id).first()

def get_research_proposals_by_faculty(db: Session, faculty_id: int, skip: int = 0, limit: int = 100) -> List[ResearchProposal]:
    return db.query(ResearchProposal).filter(ResearchProposal.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_research_proposals(db: Session, skip: int = 0, limit: int = 100) -> List[ResearchProposal]:
    return db.query(ResearchProposal).offset(skip).limit(limit).all()

def create_research_proposal(db: Session, proposal: ResearchProposalCreate, faculty_id: int) -> ResearchProposal:
    db_proposal = ResearchProposal(**proposal.model_dump(), faculty_id=faculty_id)
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

def update_research_proposal_faculty(
    db: Session, proposal_id: int, proposal_update: ResearchProposalUpdateFaculty
) -> Optional[ResearchProposal]:
    db_proposal = db.query(ResearchProposal).filter(ResearchProposal.id == proposal_id).first()
    if db_proposal:
        update_data = proposal_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_proposal, key, value)
        db.commit()
        db.refresh(db_proposal)
    return db_proposal

def update_research_proposal_hod(
    db: Session, proposal_id: int, proposal_update: ResearchProposalUpdateHOD
) -> Optional[ResearchProposal]:
    db_proposal = db.query(ResearchProposal).filter(ResearchProposal.id == proposal_id).first()
    if db_proposal:
        db_proposal.api_score_hod = proposal_update.api_score_hod
        db.commit()
        db.refresh(db_proposal)
    return db_proposal

def update_research_proposal_director(
    db: Session, proposal_id: int, proposal_update: ResearchProposalUpdateDirector
) -> Optional[ResearchProposal]:
    db_proposal = db.query(ResearchProposal).filter(ResearchProposal.id == proposal_id).first()
    if db_proposal:
        db_proposal.api_score_director = proposal_update.api_score_director
        db.commit()
        db.refresh(db_proposal)
    return db_proposal

def delete_research_proposal(db: Session, proposal_id: int) -> Optional[ResearchProposal]:
    db_proposal = db.query(ResearchProposal).filter(ResearchProposal.id == proposal_id).first()
    if db_proposal:
        db.delete(db_proposal)
        db.commit()
    return db_proposal

def get_research_proposals_total_score(db: Session, faculty_id: int) -> float:
    proposals = db.query(ResearchProposal).filter(ResearchProposal.faculty_id == faculty_id).all()
    total_score = sum([p.api_score_faculty for p in proposals])
    return total_score
