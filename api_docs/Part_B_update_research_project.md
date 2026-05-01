# Update Research Project

**URL Path:** `/api/v1/research-projects/{project_id}`

**Method:** `PUT`

**Description:** Updates an existing Research Project entry. Supports role-based updates for project details and authority scores.

## Request Data
- **Parameters:**
    - `project_id` (UUID, path): Unique identifier of the project.
- **Body (JSON):**
    - **Faculty Update:** `project_name`, `funding_agency`, `date_of_sanction`, `funding_amount`, `role`, `project_status`.
    - **HOD Update:** `api_score_hod` (float).
    - **Director Update:** `api_score_director` (float).

## Response Data
- **Success (200 OK):** The updated project object.

## Access Control
- Faculty can update their own entries (except scores).
- HOD can update `api_score_hod`.
- Director can update `api_score_director`.
- Administrators have full update permissions.
