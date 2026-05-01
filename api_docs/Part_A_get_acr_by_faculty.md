# Get ACR by Faculty

**URL Path:** `/api/v1/part-a/acr/faculty/{faculty_id}`
**HTTP Method:** `GET`
**Description:** Retrieves all ACR entries for a specific faculty member.

## Request Data
- **Type:** N/A (Path Parameter)
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| faculty_id | string (UUID) | ID of the faculty member |

## Response Data
- **Success Status Code:** 200 OK
- **Fields:** List of ACR objects.

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
- **Roles:** Faculty (self), HOD (department), Director, Dean, VC, Admin.
- **Hierarchy:** Higher authorities can see subordinates' data.
