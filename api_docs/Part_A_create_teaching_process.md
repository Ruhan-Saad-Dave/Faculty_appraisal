# Create Teaching Process

**URL Path:** `/api/v1/part-a/teaching-process`
**HTTP Method:** `POST`
**Description:** Creates a new teaching process entry (Lectures/Practicals).

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| semester | string | Academic semester |
| course_code_name | string | Course identifier |
| planned_classes | integer | Classes planned |
| conducted_classes | integer | Classes conducted |
| sr_no | integer | Serial number (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Teaching Process object.

## Access Control
- **Roles:** `faculty`
