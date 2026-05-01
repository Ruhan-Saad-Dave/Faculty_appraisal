# Update My Profile

**URL Path:** `/api/v1/profile`

**Method:** `PUT`

**Description:** Updates the profile details of the currently logged-in user.

## Request Data
- **Body (JSON):**
    - `employee_id`, `name`, `designation`, `qualification`, `department`, `experience`, `phone`, `academic_year`.

## Response Data
- **Success (200 OK):** The updated faculty profile object.

## Access Control
- Any logged-in user can update their own profile details.
