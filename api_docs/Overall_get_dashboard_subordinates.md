# Get Subordinates Status (Dashboard)

**URL Path:** `/api/v1/dashboard/subordinates`

**Method:** `GET`

**Description:** Returns a list of all faculties reporting to the current user along with their appraisal submission status. Used for authority dashboards.

## Response Data
- **Success (200 OK):** A list of subordinate status objects.
    - `faculty_id` (UUID): ID of the subordinate.
    - `name` (str): Name of the subordinate.
    - `status` (str): DRAFT / SUBMITTED / APPROVED / etc.
    - `overall_score` (float): Current aggregated score.

## Access Control
- Restricted to HOD, Director, Dean, VC, and Administrators.
- Returns only subordinates within the user's jurisdiction (School/Department).
