# Get All Research Projects

**URL Path:** `/api/v1/research-projects`

**Method:** `GET`

**Description:** Retrieves all Research Projects across the institution.

## Request Data
- **Parameters:**
    - `skip` (int, query): Number of records to skip (default: 0).
    - `limit` (int, query): Maximum number of records to return (default: 100).

## Response Data
- **Success (200 OK):** A list of all research project entries.

## Access Control
- Restricted to Administrators only.
