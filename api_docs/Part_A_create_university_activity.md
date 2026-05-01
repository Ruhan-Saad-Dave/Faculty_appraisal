# Create University Activity

**URL Path:** `/api/v1/part-a/university-activities`
**HTTP Method:** `POST`
**Description:** Creates a new university activity entry.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| activity | string | Activity name |
| nature_of_activity | string | Nature |
| sr_no | integer | Serial number (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** University Activity object.

## Access Control
- **Roles:** `faculty`
