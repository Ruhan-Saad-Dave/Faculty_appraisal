# Create ACR Entry

**URL Path:** `/api/v1/part-a/acr`
**HTTP Method:** `POST`
**Description:** Creates a new ACR (Annual Confidential Report) entry. Typically used by admin to pre-create rows for faculty.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| faculty_id | string (UUID) | ID of the faculty member |
| subject | string | Subject/Title of the ACR |
| sr_no | integer | Serial number (optional) |
| department | string | Department name (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| id | string (UUID) | Unique ID of the entry |
| faculty_id | string (UUID) | ID of the faculty member |
| sr_no | integer | Serial number |
| subject | string | Subject/Title |
| department | string | Department |
| document | string | Path to the uploaded document |
| api_score_hod | float | Score assigned by HOD |
| api_score_director | float | Score assigned by Director |
| signature | boolean | Signature status |

## Access Control
- **Roles:** `admin` only (as per current implementation)
