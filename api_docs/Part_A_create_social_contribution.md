# Create Social Contribution

**URL Path:** `/api/v1/part-a/social-contributions`
**HTTP Method:** `POST`
**Description:** Creates a new social contribution entry.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| activity_type | string | Type of activity |
| details_of_activity | string | Details |
| sr_no | integer | Serial number (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Social Contribution object.

## Access Control
- **Roles:** `faculty`
