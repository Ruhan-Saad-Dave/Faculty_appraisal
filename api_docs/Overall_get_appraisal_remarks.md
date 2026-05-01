# Get Appraisal Remarks

**URL Path:** `/api/v1/appraisal-remarks/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves all general appraisal remarks for a faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.

## Response Data
- **Success (200 OK):** A list of remarks objects.
    - `id` (UUID): Unique identifier of the remark.
    - `faculty_id` (UUID): ID of the faculty.
    - `remarks` (str): Content of the remark.

## Access Control
- Higher authorities (HOD, Director, Dean, VC) can view remarks of their subordinates.
- Administrators have full access.
