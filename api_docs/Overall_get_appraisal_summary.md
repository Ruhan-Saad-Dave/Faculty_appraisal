# Get Appraisal Summary

**URL Path:** `/api/v1/appraisal-summary/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves the aggregated appraisal summary for a faculty member, combining scores from Part A and Part B.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.

## Response Data
- **Success (200 OK):**
    - `faculty_id` (UUID): ID of the faculty.
    - `part_a_summary` (object):
        - `teaching_score`, `feedback_score`, `dept_score`, `university_score`, `social_score`, `industry_score`, `acr_score`, `part_a_total`.
    - `part_b_summary` (object):
        - `journal_score`, `book_score`, `pedagogy_score`, `guidance_score`, `project_score`, `ipr_score`, `award_score`, `conference_score`, `proposal_score`, `product_score`, `self_development_score`, `industrial_training_score`, `part_b_total`.
    - `grand_total_score` (float): Sum of Part A and Part B totals (Max 575).

## Access Control
- Faculty can view their own summary.
- Higher authorities (HOD, Director, Dean, VC) can view summaries of their subordinates.
- Administrators have full access.
