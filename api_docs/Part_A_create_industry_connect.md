# Create Industry Connect

**URL Path:** `/api/v1/part-a/industry-connect`
**HTTP Method:** `POST`
**Description:** Creates a new industry connect entry.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| industry_name | string | Name of industry |
| details_of_activity | string | Details |
| sr_no | integer | Serial number (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Industry Connect object.

## Access Control
- **Roles:** `faculty`
