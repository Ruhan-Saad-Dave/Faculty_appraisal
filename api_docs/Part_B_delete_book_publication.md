# Delete Book Publication

**Endpoint Name:** Delete Book Publication  
**URL Path:** `/api/v1/part-b/book-publications/{publication_id}`  
**Method:** `DELETE`

## Description
Deletes a specific book publication record.

## Access Control
- **Faculty:** Own records.
- **Admin:** Any record.

## Request Data
- **Path Parameters:**
  - `publication_id` (UUID string).

## Response Data
- **Code:** `204 No Content`
