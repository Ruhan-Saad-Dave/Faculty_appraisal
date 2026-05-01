# Create Journal Publication

**URL Path:** `/api/v1/journal-publications`
**HTTP Method:** `POST`
**Description:** Creates a new journal publication entry.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| title_with_page_nos | string | Title of paper and pages |
| journal_details | string | Journal name and details |
| issn_isbn_no | string | ISSN/ISBN |
| indexing | Enum | SCOPUS, WOS, UGC_CARE, PEER_REVIEWED |
| sr_no | integer | Serial number (optional) |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Journal Publication object.

## Access Control
- **Roles:** `faculty`
