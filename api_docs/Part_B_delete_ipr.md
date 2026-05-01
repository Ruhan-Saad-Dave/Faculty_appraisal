# Delete IPR Entry

**URL Path:** `/api/v1/ipr/{ipr_id}`

**Method:** `DELETE`

**Description:** Removes an Intellectual Property Rights (IPR) entry from the system.

## Request Data
- **Parameters:**
    - `ipr_id` (UUID, path): Unique identifier of the IPR entry.

## Response Data
- **Success (204 No Content):** Entry successfully deleted.
- **Error (404 Not Found):** If the IPR entry does not exist.

## Access Control
- Faculty can delete their own entries.
- Administrators can delete any entry.
