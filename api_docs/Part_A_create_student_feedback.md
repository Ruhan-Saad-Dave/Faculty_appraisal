# Create Student Feedback

**URL Path:** `/api/v1/part-a/student-feedback`
**HTTP Method:** `POST`
**Description:** Creates a new student feedback entry.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| course_code_name | string | Course identifier |
| first_feedback | float | First feedback score (0-5) |
| second_feedback | float | Second feedback score (0-5) |
| sr_no | integer | Serial number (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Student Feedback object.

## Access Control
- **Roles:** `faculty`
