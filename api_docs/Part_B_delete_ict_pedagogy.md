# Delete ICT Pedagogy

**Endpoint Name:** Delete ICT Pedagogy  
**URL Path:** `/api/v1/part-b/pedagogy/{pedagogy_id}`  
**Method:** `DELETE`

## Description
Deletes an ICT pedagogy record.

## Access Control
- **Faculty:** Own records.
- **Admin:** Any record.

## Request Data
- **Path Parameters:**
  - `pedagogy_id` (UUID string).

## Response Data
- **Code:** `204 No Content`
