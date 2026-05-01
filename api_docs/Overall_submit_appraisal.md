# Submit Appraisal

**URL Path:** `/api/v1/appraisal-summary/submit`

**Method:** `POST`

**Description:** Finalizes the appraisal for the current academic year and changes its status to `SUBMITTED`.

## Request Data
- **Body (JSON):**
    - `academic_year` (str): The year of appraisal (e.g., "2025-26").

## Response Data
- **Success (200 OK):**
    - `faculty_id` (UUID): ID of the submitting faculty.
    - `status` (str): "SUBMITTED".
    - `overall_score` (float): The final score at the time of submission.
    - `academic_year` (str): The academic year.
    - `message` (str): "Appraisal submitted successfully".

## Access Control
- Only the faculty owner can submit their appraisal.
