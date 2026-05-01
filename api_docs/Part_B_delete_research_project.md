# Delete Research Project

**URL Path:** `/api/v1/research-projects/{project_id}`

**Method:** `DELETE`

**Description:** Removes a Research Project from the system.

## Request Data
- **Parameters:**
    - `project_id` (UUID, path): Unique identifier of the project.

## Response Data
- **Success (204 No Content):** Project successfully deleted.

## Access Control
- Faculty can delete their own projects.
- Administrators can delete any project.
