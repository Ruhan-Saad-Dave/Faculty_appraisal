# Get IPR Entries by Faculty

**URL Path:** `/api/v1/ipr/faculty/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves all Intellectual Property Rights (IPR) entries for a specific faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.
    - `skip` (int, query): Number of records to skip (default: 0).
    - `limit` (int, query): Maximum number of records to return (default: 100).

## Response Data
- **Success (200 OK):** A list of IPR entries.
    - `id` (UUID): Unique identifier of the entry.
    - `title` (str): Title of the patent/IPR.
    - `scope` (str): National or International.
    - `filing_date` (date): Date of filing.
    - `status` (str): Published or Granted.
    - `patent_file_no` (str): Official file number.
    - `research_score_faculty` (float): Points claimed by faculty.
    - `research_score_hod` (float): Points approved by HOD.
    - `research_score_director` (float): Points approved by Director.
    - `document` (str): Link to the uploaded proof.

## Access Control
- Faculty can view their own entries.
- Administrators can view any faculty's entries.
- Higher authorities (HOD, Director, etc.) can view entries of their subordinates.
