# Delete Research Guidance Entry

**URL Path:** `/api/v1/research-guidance/{guidance_id}`

**Method:** `DELETE`

**Description:** Removes a Research Guidance entry from the system.

## Request Data
- **Parameters:**
    - `guidance_id` (UUID, path): Unique identifier of the guidance entry.

## Response Data
- **Success (204 No Content):** Entry successfully deleted.

## Access Control
- Faculty can delete their own entries.
- Administrators can delete any entry.
