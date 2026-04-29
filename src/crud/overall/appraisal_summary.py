from sqlalchemy.orm import Session
from typing import Dict

from ...crud.Part_B import (
    journal_publication as crud_journal_publication,
    book_publication as crud_book_publication,
    ict_pedagogy as crud_ict_pedagogy,
    research_guidance as crud_research_guidance,
    research_project as crud_research_project,
    ipr as crud_ipr,
    research_award as crud_research_award,
    conference_paper as crud_conference_paper,
    research_proposal as crud_research_proposal,
    product_development as crud_product_development,
    self_development_fdp as crud_self_development_fdp,
    industrial_training as crud_industrial_training,
)
from ...schema.overall.appraisal_summary import PartBSummary, AppraisalSummaryResponse, PartASummary

def get_appraisal_summary(db: Session, faculty_id: int) -> AppraisalSummaryResponse:
    # Part B Scores
    journal_score = crud_journal_publication.get_journal_publications_total_score(db, faculty_id)
    book_score = crud_book_publication.get_book_publications_total_score(db, faculty_id)
    pedagogy_score = crud_ict_pedagogy.get_ict_pedagogies_total_score(db, faculty_id)
    
    # Research Guidance returns a dict, extract total_score
    guidance_summary = crud_research_guidance.get_research_guidance_total_score(db, faculty_id)
    guidance_score = guidance_summary.get("total_score", 0.0)

    project_score = crud_research_project.get_research_projects_total_score(db, faculty_id)
    ipr_score = crud_ipr.get_ipr_total_score(db, faculty_id)
    award_score = crud_research_award.get_research_awards_total_score(db, faculty_id)
    conference_score = crud_conference_paper.get_conference_papers_total_score(db, faculty_id)
    proposal_score = crud_research_proposal.get_research_proposals_total_score(db, faculty_id)
    product_score = crud_product_development.get_product_developments_total_score(db, faculty_id)
    self_development_score = crud_self_development_fdp.get_self_development_fdp_total_score(db, faculty_id)


    part_b_total = (
        journal_score + book_score + pedagogy_score + guidance_score + project_score +
        ipr_score + award_score + conference_score + proposal_score + product_score +
        self_development_score
    )

    part_b_summary = PartBSummary(
        journal_score=journal_score,
        book_score=book_score,
        pedagogy_score=pedagogy_score,
        guidance_score=guidance_score,
        project_score=project_score,
        ipr_score=ipr_score,
        award_score=award_score,
        conference_score=conference_score,
        proposal_score=proposal_score,
        product_score=product_score,
        self_development_score=self_development_score,
        part_b_total=part_b_total,
    )

    # Part A Scores (placeholders for now)
    part_a_summary = PartASummary(
        teaching_score=0.0,
        feedback_score=0.0,
        dept_score=0.0,
        university_score=0.0,
        social_score=0.0,
        industry_score=0.0,
        acr_score=0.0,
        part_a_total=0.0,
    )

    grand_total_score = part_a_summary.part_a_total + part_b_total

    return AppraisalSummaryResponse(
        faculty_id=faculty_id,
        part_a_summary=part_a_summary,
        part_b_summary=part_b_summary,
        grand_total_score=grand_total_score,
    )
