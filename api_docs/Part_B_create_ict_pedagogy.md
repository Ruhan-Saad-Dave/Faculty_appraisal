# Create ICT Pedagogy

**URL Path:** `/api/v1/pedagogy`
**HTTP Method:** `POST`
**Description:** Creates a new ICT pedagogy entry.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| title | string | Title |
| description | string | Description |
| pedagogy_type | string | Type |
| quadrants | integer | Number of quadrants |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** ICT Pedagogy object.

## Access Control
- **Roles:** `faculty`
