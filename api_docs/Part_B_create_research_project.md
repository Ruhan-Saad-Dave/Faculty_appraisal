# Create Research Project

**URL Path:** `/api/v1/research-projects`
**HTTP Method:** `POST`
**Description:** Creates a new research project entry.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| project_name | string | Name of project |
| funding_agency | string | Funding agency |
| date_of_sanction | date | Date of sanction |
| funding_amount | float | Amount |
| role | string | PI / Co-PI |
| project_status | string | Completed / Ongoing |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Research Project object.

## Access Control
- **Roles:** `faculty`
