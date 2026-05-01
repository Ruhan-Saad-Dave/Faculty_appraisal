# Get Research Projects by Faculty

**URL Path:** `/api/v1/research-projects/faculty/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves all Research Projects for a specific faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.
    - `skip` (int, query): Number of records to skip (default: 0).
    - `limit` (int, query): Maximum number of records to return (default: 100).

## Response Data
- **Success (200 OK):** A list of research project entries.
    - `id` (UUID): Unique identifier of the entry.
    - `project_name` (str): Title of the project.
    - `funding_agency` (str): Agency providing the funds.
    - `date_of_sanction` (date): Date project was sanctioned.
    - `funding_amount` (float): Total amount sanctioned.
    - `role` (str): PI / Co-PI.
    - `project_status` (str): Ongoing / Completed.
    - `api_score_faculty` (int): Points claimed by faculty.
    - `api_score_hod` (float): Points approved by HOD.
    - `api_score_director` (float): Points approved by Director.
    - `document` (str): Link to the uploaded proof.

## Access Control
- Faculty can view their own entries.
- Higher authorities can view subordinates' entries.
- Administrators can view any entry.
