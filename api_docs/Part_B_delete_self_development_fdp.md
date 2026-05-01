# Delete Self-Development FDP

**Endpoint Name:** Delete Self-Development FDP  
**URL Path:** `/api/v1/part-b/self-development/{fdp_id}`  
**Method:** `DELETE`

## Description
Deletes an FDP participation record.

## Access Control
- **Faculty:** Own records.
- **Admin:** Any record.

## Request Data
- **Path Parameters:**
  - `fdp_id` (UUID string).

## Response Data
- **Code:** `204 No Content`
