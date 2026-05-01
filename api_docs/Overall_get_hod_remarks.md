# Get HOD Remarks

**URL Path:** `/api/v1/appraisal-remarks/hod/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves the specific remarks and approved score from the Head of Department (HOD) for a faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.

## Response Data
- **Success (200 OK):**
    - `hod_remark` (str): Feedback from HOD.
    - `hod_approved_score` (float): Total score approved by HOD.
    - `hod_signature` (str): Digital signature path (if any).

## Access Control
- Faculty can view HOD remarks on their own appraisal.
- Higher authorities and HOD can view these remarks.
- Administrators have full access.
