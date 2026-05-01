# Update HOD Remarks

**URL Path:** `/api/v1/appraisal-remarks/hod/{faculty_id}`

**Method:** `PUT`

**Description:** Creates or updates the HOD's remarks and approved score for a faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.
- **Body (JSON):**
    - `hod_remark` (str), `hod_approved_score` (float), `hod_signature` (str).

## Response Data
- **Success (200 OK):** The updated HOD remarks object.

## Access Control
- Restricted to HOD and Administrators.
- HOD must have authority over the faculty member.
