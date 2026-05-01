# Update IPR Entry

**URL Path:** `/api/v1/ipr/{ipr_id}`

**Method:** `PUT`

**Description:** Updates an existing Intellectual Property Rights (IPR) entry. Supports role-based updates for faculty information and authority scores.

## Request Data
- **Parameters:**
    - `ipr_id` (UUID, path): Unique identifier of the IPR entry.
- **Body (JSON):**
    - **Faculty Update:** `title`, `scope`, `filing_date`, `status`, `patent_file_no`.
    - **HOD Update:** `research_score_hod` (float).
    - **Director Update:** `research_score_director` (float).

## Response Data
- **Success (200 OK):** The updated IPR entry object.
- **Error (404 Not Found):** If the IPR entry does not exist.
- **Error (403 Forbidden):** If the user is not authorized to update this entry or specific fields.

## Access Control
- Faculty can update their own entries (except scores).
- HOD can update `research_score_hod`.
- Director can update `research_score_director`.
- Administrators have full update permissions.
