# Update Dean Remarks

**URL Path:** `/api/v1/appraisal-remarks/dean/{faculty_id}`

**Method:** `PUT`

**Description:** Creates or updates the Dean's remarks and approved score for a faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.
- **Body (JSON):**
    - `dean_remark` (str), `dean_approved_score` (float), `dean_signature` (str).

## Access Control
- Restricted to Dean and Administrators.
- Dean must have authority over the faculty member.
