# Create Project (Part A)

**URL Path:** `/api/v1/part-a/projects`
**HTTP Method:** `POST`
**Description:** Creates a new project entry for Part A.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| project_type | string | Type of project |
| sr_no | integer | Serial number (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Project (Part A) object.

## Access Control
- **Roles:** `faculty`
