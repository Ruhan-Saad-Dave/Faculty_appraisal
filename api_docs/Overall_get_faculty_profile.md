# Get Faculty Profile

**URL Path:** `/api/v1/profile/{faculty_id}`

**Method:** `GET`

**Description:** Retrieves the profile details of a specific faculty member.

## Request Data
- **Parameters:**
    - `faculty_id` (UUID, path): Unique identifier of the faculty member.

## Response Data
- **Success (200 OK):** Faculty profile object.

## Access Control
- Higher authorities (HOD, Director, Dean, VC) can view profiles of their subordinates.
- Administrators can view any profile.
