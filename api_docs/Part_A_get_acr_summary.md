# Get ACR Summary

**URL Path:** `/api/v1/part-a/acr/summary/{faculty_id}`
**HTTP Method:** `GET`
**Description:** Calculates the total ACR score for a faculty member, capped at 25 points.

## Request Data
- **Type:** N/A (Path Parameter)
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| faculty_id | string (UUID) | ID of the faculty member |

## Response Data
- **Success Status Code:** 200 OK
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| totalScore | float | Aggregated ACR score (max 25) |

## Access Control
- **Roles:** Faculty (self), HOD, Director, Dean, VC, Admin.
