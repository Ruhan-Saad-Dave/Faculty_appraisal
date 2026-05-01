# Update Course File Entry

**URL Path:** `/api/v1/part-a/course-files/{id}`
**HTTP Method:** `PUT`
**Description:** Updates an existing course file entry. Faculty can update content; HOD can update scores.

## Request Data
- **Type:** `application/json`
- **Fields (Faculty):**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| course_paper | string | Course/Paper name |
| title | string | Title |
| details_proof | boolean | Proof status |
| department | string | Department |

- **Fields (HOD):**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| api_score_hod | float | Score assigned by HOD |
| signature | boolean | Signature status |

## Response Data
- **Success Status Code:** 200 OK
- **Fields:** Course File object.

## Access Control
- **Roles:** Faculty (owner), HOD, Admin.
