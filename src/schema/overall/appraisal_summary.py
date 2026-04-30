from pydantic import BaseModel
from typing import Optional

class PartASummary(BaseModel):
    teaching_score: float = 0.0
    feedback_score: float = 0.0
    dept_score: float = 0.0
    university_score: float = 0.0
    social_score: float = 0.0
    industry_score: float = 0.0
    acr_score: float = 0.0
    part_a_total: float = 0.0 # out of 200

class PartBSummary(BaseModel):
    journal_score: float = 0.0
    book_score: float = 0.0
    pedagogy_score: float = 0.0
    guidance_score: float = 0.0
    project_score: float = 0.0
    ipr_score: float = 0.0
    award_score: float = 0.0
    conference_score: float = 0.0
    proposal_score: float = 0.0
    product_score: float = 0.0
    self_development_score: float = 0.0
    industrial_training_score: float = 0.0
    part_b_total: float = 0.0 # out of 375

class AppraisalSummaryResponse(BaseModel):
    faculty_id: str
    part_a_summary: PartASummary
    part_b_summary: PartBSummary
    grand_total_score: float = 0.0 # out of 575
