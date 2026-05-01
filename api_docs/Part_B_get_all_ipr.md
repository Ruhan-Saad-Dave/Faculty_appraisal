# Get All IPR Entries

**URL Path:** `/api/v1/ipr`

**Method:** `GET`

**Description:** Retrieves all Intellectual Property Rights (IPR) entries across the institution.

## Request Data
- **Parameters:**
    - `skip` (int, query): Number of records to skip (default: 0).
    - `limit` (int, query): Maximum number of records to return (default: 100).

## Response Data
- **Success (200 OK):** A list of all IPR entries.
    - `id` (UUID): Unique identifier of the entry.
    - `faculty_id` (UUID): ID of the faculty owner.
    - `title` (str): Title of the patent/IPR.
    - `scope` (str): National or International.
    - `filing_date` (date): Date of filing.
    - `status` (str): Published or Granted.
    - `patent_file_no` (str): Official file number.
    - `research_score_faculty` (float): Points claimed by faculty.

## Access Control
- Restricted to Administrators only.
