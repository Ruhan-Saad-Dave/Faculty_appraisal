# Get All Research Guidance Entries

**URL Path:** `/api/v1/research-guidance`

**Method:** `GET`

**Description:** Retrieves all Research Guidance entries across the institution.

## Request Data
- **Parameters:**
    - `skip` (int, query): Number of records to skip (default: 0).
    - `limit` (int, query): Maximum number of records to return (default: 100).

## Response Data
- **Success (200 OK):** A list of all research guidance entries.

## Access Control
- Restricted to Administrators only.
