# Get IPR Summary

**URL Path:** `/api/v1/ipr/summary/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves the total research score for IPR for a specific faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.

## Response Data
- **Success (200 OK):**
    - `total_score` (float): Sum of points from all published and granted patents/IPR.

## Access Control
- Faculty can view their own summary.
- Higher authorities can view subordinates' summaries.
- Administrators have full access.
