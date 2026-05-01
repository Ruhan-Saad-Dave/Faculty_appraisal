# Get Research Guidance Summary

**URL Path:** `/api/v1/research-guidance/summary/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves the total research score and student statistics for Research Guidance for a specific faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.

## Response Data
- **Success (200 OK):**
    - `total_score` (float): Sum of points from all guidance entries.
    - `total_students_me` (int): Total M.E./M.Tech students guided.
    - `total_students_phd` (int): Total Ph.D. students guided.

## Access Control
- Faculty can view their own summary.
- Higher authorities can view subordinates' summaries.
- Administrators have full access.
