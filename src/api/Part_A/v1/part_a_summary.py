from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_A.part_a_summary import PartASummaryResponse
from ....crud.Part_A import (
    teaching_process,
    student_feedback,
    departmental_activities,
    university_activities,
    social_contributions,
    industry_connect,
    acr,
    course_file,
    teaching_methods,
    project,
    qualification_enhancement
)

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    return User(id=1, roles=["faculty"])

@router.get("/part-a-summary/{faculty_id}", response_model=PartASummaryResponse)
def get_part_a_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Fetch scores from all sections
    # Note: Using faculty scores as primary for summary, 
    # but PDF asks for totalFacultyScore, totalHodScore, totalDirectorScore
    
    tp_entries = teaching_process.get_teaching_process_by_faculty(db, faculty_id)
    sf_entries = student_feedback.get_student_feedback_by_faculty(db, faculty_id)
    da_entries = departmental_activities.get_departmental_activities_by_faculty(db, faculty_id)
    ua_entries = university_activities.get_university_activities_by_faculty(db, faculty_id)
    sc_entries = social_contributions.get_social_contributions_by_faculty(db, faculty_id)
    ic_entries = industry_connect.get_industry_connect_by_faculty(db, faculty_id)
    acr_entries = acr.get_acr_by_faculty(db, faculty_id)
    
    # Simple summation for demo
    teaching_score = sum([e.api_score_faculty for e in tp_entries])
    
    # Feedback average score calculation (simplified)
    feedback_score = 0.0
    if sf_entries:
        feedback_score = sum([(e.first_feedback + e.second_feedback)/2 for e in sf_entries]) / len(sf_entries)
    
    dept_score = sum([e.api_score_faculty for e in da_entries])
    univ_score = sum([e.api_score_faculty for e in ua_entries])
    social_score = sum([e.api_score_faculty for e in sc_entries])
    ind_score = sum([e.api_score_faculty for e in ic_entries])
    acr_val = sum([e.api_score_hod for e in acr_entries])

    # Totals
    total_faculty = teaching_score + feedback_score + dept_score + univ_score + social_score + ind_score
    total_hod = sum([e.api_score_hod for e in tp_entries + sf_entries + da_entries + ua_entries + sc_entries + ic_entries + acr_entries])
    total_dir = sum([getattr(e, 'api_score_director', 0.0) for e in tp_entries + sf_entries + da_entries + ua_entries + sc_entries + ic_entries + acr_entries])

    return PartASummaryResponse(
        teachingScore=teaching_score,
        feedbackScore=feedback_score,
        deptActivityScore=dept_score,
        universityActivityScore=univ_score,
        socialScore=social_score,
        industryScore=ind_score,
        acrScore=acr_val,
        totalFacultyScore=total_faculty,
        totalHodScore=total_hod,
        totalDirectorScore=total_dir
    )
