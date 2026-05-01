# Update Book Publication

**Endpoint Name:** Update Book Publication  
**URL Path:** `/api/v1/part-b/book-publications/{publication_id}`  
**Method:** `PUT`

## Description
Updates an existing book publication record.

## Access Control
- **Faculty:** Update fields.
- **HOD/Director:** Update respective API scores.

## Request Data
- **Path Parameters:**
  - `publication_id` (UUID string).
- **Body (JSON):**
  - `title_and_pages`, `book_title_editor`, `issn_isbn`, `publisher_type`, `co_authors_count`, `is_first_author`, `api_score_hod`, `api_score_director`.

## Response Data
- **Code:** `200 OK`
- Updated Book Publication object.
