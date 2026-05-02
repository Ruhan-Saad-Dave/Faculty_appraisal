# Create Popular Writing Entry

**URL Path:** `/api/v1/part-b/popular-writings`
**HTTP Method:** `POST`
**Description:** Creates a new popular writing, film, or documentary entry. (Primarily for SOMCS/Type 2)

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| title | string | Title of the work |
| writing_type | string | Popular Writing / Film / Documentary |
| date | date | Date of publication/release |
| publisher_agency | string | Publisher or Agency (optional) |
| sr_no | integer | Serial number (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Popular Writing object.

## Access Control
- **Roles:** `faculty`
