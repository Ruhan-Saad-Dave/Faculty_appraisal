# Create Enclosure

**URL Path:** `/api/v1/enclosures`

**Method:** `POST`

**Description:** Adds a new enclosure (document or text) to the appraisal. Supports file uploads for supporting evidence.

## Request Data
- **Body (Form Data):**
    - `enclosure_text` (str): Description or text of the enclosure.
    - `file` (UploadFile, optional): PDF document of the enclosure.

## Response Data
- **Success (201 Created):**
    - `id` (UUID): Unique identifier of the enclosure.
    - `faculty_id` (UUID): ID of the faculty owner.
    - `enclosure_text` (str): The provided text.
    - `document` (str): Path to the uploaded file.

## Access Control
- Any faculty member can add enclosures to their own appraisal.
