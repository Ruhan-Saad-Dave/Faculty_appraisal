# Get Enclosures

**URL Path:** `/api/v1/enclosures/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves all enclosures for a specific faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.

## Response Data
- **Success (200 OK):** A list of enclosure objects.

## Access Control
- Faculty can view their own enclosures.
- Higher authorities can view enclosures of their subordinates.
- Administrators have full access.
