# Get Dean Remarks

**URL Path:** `/api/v1/appraisal-remarks/dean/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves the specific remarks and approved score from the Dean for a faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.

## Response Data
- **Success (200 OK):**
    - `dean_remark` (str), `dean_approved_score` (float), `dean_signature` (str).

## Access Control
- Faculty, Higher authorities, and Dean can view.
- Administrators have full access.
