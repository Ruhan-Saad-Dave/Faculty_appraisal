# Create Qualification Enhancement

**URL Path:** `/api/v1/part-a/qualification-enhancement`
**HTTP Method:** `POST`
**Description:** Creates a new qualification enhancement entry.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| qualification_type | string | Type of qualification |
| sr_no | integer | Serial number (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Qualification Enhancement object.

## Access Control
- **Roles:** `faculty`
