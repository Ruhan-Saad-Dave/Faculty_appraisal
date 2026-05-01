# Get Research Guidance Entries by Faculty

**URL Path:** `/api/v1/research-guidance/faculty/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves all Research Guidance entries for a specific faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.
    - `skip` (int, query): Number of records to skip (default: 0).
    - `limit` (int, query): Maximum number of records to return (default: 100).

## Response Data
- **Success (200 OK):** A list of research guidance entries.
    - `id` (UUID): Unique identifier of the entry.
    - `degree` (str): M.E. / Ph.D.
    - `student_name` (str): Name of the student guided.
    - `submission_status` (str): Submitted / Awarded.
    - `award_date` (date): Date of award (optional).
    - `api_score_faculty` (int): Points claimed by faculty.
    - `api_score_hod` (float): Points approved by HOD.
    - `api_score_director` (float): Points approved by Director.
    - `document` (str): Link to the uploaded proof.

## Access Control
- Faculty can view their own entries.
- Higher authorities can view subordinates' entries.
- Administrators can view any entry.
