# Update Director Remarks

**URL Path:** `/api/v1/appraisal-remarks/director/{faculty_id}`

**Method:** `PUT`

**Description:** Creates or updates the Director's remarks and approved score for a faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.
- **Body (JSON):**
    - `director_remark` (str), `director_approved_score` (float), `director_signature` (str).

## Access Control
- Restricted to Director and Administrators.
- Director must have authority over the faculty member.
