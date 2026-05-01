# Get My Profile

**URL Path:** `/api/v1/profile`

**Method:** `GET`

**Description:** Retrieves the profile details of the currently logged-in user.

## Response Data
- **Success (200 OK):**
    - `id` (UUID): User ID.
    - `email` (str): User email.
    - `role` (str): User role.
    - `employee_id` (str): Official employee ID.
    - `name` (str): Full name.
    - `designation` (str): Job title.
    - `qualification` (str): Educational qualification.
    - `department` (str): Assigned department.
    - `experience` (int): Total years of experience.
    - `phone` (str): Contact number.
    - `school_id` (UUID): ID of the school.

## Access Control
- Any logged-in user can view their own profile.
