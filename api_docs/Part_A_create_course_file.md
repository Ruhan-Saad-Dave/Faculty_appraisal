# Create Course File Entry

**URL Path:** `/api/v1/part-a/course-files`
**HTTP Method:** `POST`
**Description:** Creates a new Course File entry. Used by faculty to document their course files.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| course_paper | string | Course/Paper name |
| title | string | Title |
| sr_no | integer | Serial number (optional) |
| details_proof | boolean | Whether proof is provided |
| department | string | Department name (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| id | string (UUID) | Unique ID |
| faculty_id | string (UUID) | ID of the faculty member |
| sr_no | integer | Serial number |
| course_paper | string | Course/Paper name |
| title | string | Title |
| details_proof | boolean | Proof provided |
| department | string | Department |
| document | string | Path to document |
| api_score_faculty | float | Self-assigned score |
| api_score_hod | float | HOD-assigned score |
| signature | boolean | Signature status |

## Access Control
- **Roles:** `faculty` only.
