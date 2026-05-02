# Retrieve Popular Writings by Faculty

**URL Path:** `/api/v1/part-b/popular-writings/faculty/{faculty_id}`
**HTTP Method:** `GET`
**Description:** Retrieves all popular writing entries for a specific faculty member.

## Request Data
- **Type:** N/A (Path Parameter)
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| faculty_id | string (UUID) | ID of the faculty member |

## Response Data
- **Success Status Code:** 200 OK
- **Fields:** List of Popular Writing objects.

## Access Control
- **Roles:** Faculty (self), HOD (same dept), Director (same school), Dean, VC, Admin.
