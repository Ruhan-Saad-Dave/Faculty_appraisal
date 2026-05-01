# Delete Journal Publication

**Endpoint Name:** Delete Journal Publication  
**URL Path:** `/api/v1/part-b/journal-publications/{publication_id}`  
**Method:** `DELETE`

## Description
Deletes a specific journal publication record and its associated data.

## Access Control
- **Faculty:** Can delete their own records.
- **Higher Authorities:** Can delete records of subordinates (if authorized).

## Request Data
- **Path Parameters:**
  - `publication_id` (UUID string): The unique identifier of the publication record.

## Response Data
- **Code:** `204 No Content`
- **Fields:** None.
