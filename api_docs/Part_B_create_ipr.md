# Create IPR Entry

**URL Path:** `/api/v1/ipr`
**HTTP Method:** `POST`
**Description:** Creates a new IPR entry (Patent/Design).

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| title | string | Title |
| scope | string | National / International |
| filing_date | date | Date of filing |
| status | string | Published / Granted |
| patent_file_no | string | Patent file number |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** IPR object.

## Access Control
- **Roles:** `faculty`
