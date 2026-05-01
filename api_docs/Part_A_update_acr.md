# Update ACR Entry

**URL Path:** `/api/v1/part-a/acr/{id}`
**HTTP Method:** `PUT`
**Description:** Updates an existing ACR entry. Different roles (HOD, Director) update different fields.

## Request Data
- **Type:** `application/json`
- **Fields (HOD/Admin):**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| api_score_hod | float | Score assigned by HOD |
| department | string | Department name (optional) |

- **Fields (Director):**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| api_score_director | float | Score assigned by Director |
| signature | boolean | Signature status (optional) |

## Response Data
- **Success Status Code:** 200 OK
- **Fields:** ACR object (same as GET).

## Access Control
- **Roles:** HOD, Director, Admin.
- **Rules:** HOD can only update scores for their department faculty. Director/Admin have broader access.
