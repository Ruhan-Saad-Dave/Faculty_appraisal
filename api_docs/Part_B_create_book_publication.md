# Create Book Publication

**URL Path:** `/api/v1/book-publications`
**HTTP Method:** `POST`
**Description:** Creates a new book or chapter publication entry.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| title_and_pages | string | Title and pages |
| book_title_editor | string | Book title and editor |
| issn_isbn | string | ISSN/ISBN |
| publisher_type | string | National/International |
| co_authors_count | integer | Number of co-authors |
| is_first_author | boolean | Is first author |
| department | string | Department (optional) |
| file | file (PDF) | Proof document (optional) |

## Response Data
- **Success Status Code:** 201 Created
- **Fields:** Book Publication object.

## Access Control
- **Roles:** `faculty`
