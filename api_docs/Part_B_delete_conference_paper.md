# Delete Conference Paper

**Endpoint Name:** Delete Conference Paper  
**URL Path:** `/api/v1/part-b/conferences/{paper_id}`  
**Method:** `DELETE`

## Description
Deletes a conference paper record.

## Access Control
- **Faculty:** Own records.
- **Admin:** Any record.

## Request Data
- **Path Parameters:**
  - `paper_id` (UUID string).

## Response Data
- **Code:** `204 No Content`
