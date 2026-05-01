# Delete Enclosure

**URL Path:** `/api/v1/enclosures/{enclosure_id}`

**Method:** `DELETE`

**Description:** Removes an enclosure from the system.

## Request Data
- **Parameters:**
    - `enclosure_id` (UUID, path): Unique identifier of the enclosure.

## Response Data
- **Success (204 No Content):** Enclosure successfully deleted.

## Access Control
- Only the faculty owner can delete their own enclosures.
