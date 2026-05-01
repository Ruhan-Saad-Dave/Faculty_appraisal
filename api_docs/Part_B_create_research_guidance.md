# Create Research Guidance

**URL Path:** `/api/v1/research-guidance`
**HTTP Method:** `POST`
**Description:** Creates a new research guidance entry (ME/PhD).

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| degree | string | ME / PhD |
| student_name | string | Name of student |
| submission_status | string | Submitted / Awarded |
| award_date | date | Date of award (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Research Guidance object.

## Access Control
- **Roles:** `faculty`
