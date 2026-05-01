# Delete Research Award

**Endpoint Name:** Delete Research Award  
**URL Path:** `/api/v1/part-b/research-awards/{award_id}`  
**Method:** `DELETE`

## Description
Deletes a research award record.

## Access Control
- **Faculty:** Own records.
- **Admin:** Any record.

## Request Data
- **Path Parameters:**
  - `award_id` (UUID string).

## Response Data
- **Code:** `204 No Content`
