# Update Research Guidance Entry

**URL Path:** `/api/v1/research-guidance/{guidance_id}`

**Method:** `PUT`

**Description:** Updates an existing Research Guidance entry. Supports role-based updates for faculty information and authority scores.

## Request Data
- **Parameters:**
    - `guidance_id` (UUID, path): Unique identifier of the guidance entry.
- **Body (JSON):**
    - **Faculty Update:** `degree`, `student_name`, `submission_status`, `award_date`.
    - **HOD Update:** `api_score_hod` (float).
    - **Director Update:** `api_score_director` (float).

## Response Data
- **Success (200 OK):** The updated guidance entry object.

## Access Control
- Faculty can update their own entries (except scores).
- HOD can update `api_score_hod`.
- Director can update `api_score_director`.
- Administrators have full update permissions.
