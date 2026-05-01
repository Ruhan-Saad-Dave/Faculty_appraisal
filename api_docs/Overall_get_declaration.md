# Get Declaration

**URL Path:** `/api/v1/declaration/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves the final declaration for a specific faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.

## Response Data
- **Success (200 OK):** The declaration object.
- **Error (404 Not Found):** If no declaration has been submitted yet.

## Access Control
- Faculty can view their own declaration.
- Higher authorities can view declarations of their subordinates.
- Administrators have full access.
