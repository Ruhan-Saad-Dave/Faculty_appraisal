# Add Appraisal Remarks

**URL Path:** `/api/v1/appraisal-remarks/{faculty_id}`

**Method:** `POST`

**Description:** Adds a general appraisal remark for a faculty member. Used by authorities during the review process.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.
- **Body (JSON):**
    - `remarks` (str): Content of the remark.

## Response Data
- **Success (200 OK):** The created remark object.

## Access Control
- Restricted to HOD, Director, Dean, VC, and Administrators.
- User must have authority over the specified faculty member.
