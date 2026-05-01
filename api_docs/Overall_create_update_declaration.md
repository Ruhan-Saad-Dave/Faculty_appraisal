# Create or Update Declaration

**URL Path:** `/api/v1/declaration`

**Method:** `POST`

**Description:** Creates or updates the final declaration (Place and Designation) for the appraisal.

## Request Data
- **Body (JSON):**
    - `place` (str): Location of signing.
    - `designation` (str): Current designation.

## Response Data
- **Success (200 OK):**
    - `id` (UUID): Unique identifier of the declaration.
    - `faculty_id` (UUID): ID of the faculty owner.
    - `place` (str): The provided place.
    - `designation` (str): The provided designation.
    - `submission_date` (date): Date when the declaration was recorded.

## Access Control
- Only the faculty owner can create/update their declaration.
