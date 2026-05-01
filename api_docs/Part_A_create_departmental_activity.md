# Create Departmental Activity

**URL Path:** `/api/v1/part-a/department-activities`
**HTTP Method:** `POST`
**Description:** Creates a new departmental activity entry.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| activity | string | Activity name |
| nature_of_activity | string | Nature of activity |
| sr_no | integer | Serial number (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| id | string (UUID) | Unique ID |
| faculty_id | string (UUID) | Faculty ID |
| sr_no | integer | Serial number |
| activity | string | Activity name |
| nature_of_activity | string | Nature |
| department | string | Department |
| document | string | Path to document |
| api_score_faculty | float | Faculty score |
| api_score_hod | float | HOD score |
| api_score_director | float | Director score |

## Access Control
- **Roles:** `faculty`
