# Get VC Approval (Final)

**URL Path:** `/api/v1/appraisal-remarks/final/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves the final score, grade, and VC's approval remarks for a faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.

## Response Data
- **Success (200 OK):**
    - `final_score` (float): The ultimate score approved for the year.
    - `final_grade` (str): A / B / C grade based on score.
    - `vc_approval` (str): VC's final comment.

## Access Control
- Faculty, VC, and all intermediate authorities can view.
- Administrators have full access.
