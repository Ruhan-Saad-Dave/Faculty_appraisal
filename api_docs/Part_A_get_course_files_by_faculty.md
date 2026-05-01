# Get Course Files by Faculty

**URL Path:** `/api/v1/part-a/course-files/faculty/{faculty_id}`
**HTTP Method:** `GET`
**Description:** Retrieves all course file entries for a specific faculty member.

## Request Data
- **Type:** N/A (Path Parameter)
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| faculty_id | string (UUID) | ID of the faculty member |

## Response Data
- **Success Status Code:** 200 OK
- **Fields:** List of Course File objects.

## Access Control
- **Roles:** Faculty (self), HOD, Director, Dean, VC, Admin.
