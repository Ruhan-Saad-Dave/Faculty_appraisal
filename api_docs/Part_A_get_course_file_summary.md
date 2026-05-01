# Get Course File Summary

**URL Path:** `/api/v1/part-a/course-files/summary/{faculty_id}`
**HTTP Method:** `GET`
**Description:** Gets total score for course files.

## Request Data
- **Type:** N/A

## Response Data
- **Success Status Code:** 200 OK
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| totalScore | float | Total score |

## Access Control
- **Roles:** Faculty (self), HOD, Director, Dean, VC, Admin.
