# Update VC Remarks (Final Approval)

**URL Path:** `/api/v1/appraisal-remarks/final/{faculty_id}`

**Method:** `PUT`

**Description:** Creates or updates the Vice Chancellor's (VC) final score, grade, and approval comments.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.
- **Body (JSON):**
    - `final_score` (float), `final_grade` (str), `vc_approval` (str).

## Access Control
- Restricted to VC and Administrators only.
